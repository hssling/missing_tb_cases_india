"""
Automated PubMed search for TB under-reporting / detection studies in India.

Usage:
    python scripts/00_lit_search.py --query "custom terms" --retmax 300

Environment variables:
    NCBI_API_KEY   Optional API key for higher rate limits.
    PUBMED_EMAIL   Optional email passed to Entrez (for courtesy logging).
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Iterable, List

import requests


ROOT = Path(__file__).resolve().parents[1]
LIT_DIR = ROOT / "lit"
LIT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = LIT_DIR / "lit_db.csv"

DEFAULT_QUERY = (
    '(tuberculosis[MeSH Terms] OR TB[Title/Abstract]) AND '
    '(India[Title/Abstract] OR "South-East Asia"[Title/Abstract]) AND '
    '("under-reporting"[Title/Abstract] OR underreporting[Title/Abstract] OR '
    '"case detection"[Title/Abstract] OR "inventory study"[Title/Abstract] OR '
    '"capture recapture"[Title/Abstract] OR "care cascade"[Title/Abstract])'
)
ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Query PubMed for TB missed-case literature.")
    parser.add_argument("--query", default=DEFAULT_QUERY, help="PubMed query string.")
    parser.add_argument("--retmax", type=int, default=250, help="Maximum number of records to pull.")
    parser.add_argument("--chunk-size", type=int, default=100, help="Batch size for efetch calls.")
    return parser.parse_args()


def pubmed_search(query: str, retmax: int) -> List[str]:
    """Return a list of PubMed IDs for the given query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "retmode": "json",
        "sort": "pub date",
    }
    email = os.environ.get("PUBMED_EMAIL")
    if email:
        params["email"] = email
    api_key = os.environ.get("NCBI_API_KEY")
    if api_key:
        params["api_key"] = api_key

    print(f"[00_lit_search] Querying PubMed for up to {retmax} records...")
    response = requests.get(ESEARCH_URL, params=params, timeout=30)
    response.raise_for_status()
    ids = response.json().get("esearchresult", {}).get("idlist", [])
    print(f"[00_lit_search] Retrieved {len(ids)} PubMed IDs.")
    return ids


def fetch_pubmed_records(id_batch: Iterable[str]) -> List[Dict[str, str]]:
    """Fetch article metadata for a batch of PubMed IDs."""
    ids = ",".join(id_batch)
    if not ids:
        return []

    params = {
        "db": "pubmed",
        "id": ids,
        "retmode": "xml",
    }
    api_key = os.environ.get("NCBI_API_KEY")
    if api_key:
        params["api_key"] = api_key

    response = requests.get(EFETCH_URL, params=params, timeout=60)
    response.raise_for_status()

    records: List[Dict[str, str]] = []
    root = ET.fromstring(response.text)
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID", default="").strip()
        title = article.findtext(".//ArticleTitle", default="").strip().replace("\n", " ")
        abstract = " ".join(
            elem.text.strip()
            for elem in article.findall(".//Abstract/AbstractText")
            if elem.text
        )
        journal = article.findtext(".//Journal/Title", default="").strip()
        year = article.findtext(".//Article/Journal/JournalIssue/PubDate/Year", default="")
        if not year:
            medline_date = article.findtext(".//Article/Journal/JournalIssue/PubDate/MedlineDate", default="")
            year = medline_date[:4]

        records.append(
            {
                "pmid": pmid,
                "title": title,
                "journal": journal,
                "year": year,
                "abstract": abstract,
            }
        )
    return records


def iter_batches(items: List[str], batch_size: int) -> Iterable[List[str]]:
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]


def main() -> None:
    args = parse_args()
    pmids = pubmed_search(args.query, args.retmax)
    if not pmids:
        print("[00_lit_search] No PubMed IDs returned. Exiting without writing file.")
        return

    rows: List[Dict[str, str]] = []
    for batch in iter_batches(pmids, args.chunk_size):
        print(f"[00_lit_search] Fetching metadata for IDs {batch[0]}–{batch[-1]}...")
        rows.extend(fetch_pubmed_records(batch))
        time.sleep(0.34)  # respect API rate limits

    if not rows:
        print("[00_lit_search] No metadata retrieved; skipping file write.")
        return

    print(f"[00_lit_search] Writing {len(rows)} records to {OUTPUT_PATH.relative_to(ROOT)}")
    fieldnames = ["pmid", "title", "journal", "year", "abstract"]
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":
    try:
        main()
    except requests.HTTPError as exc:
        print(f"[00_lit_search] HTTP error: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:  # pragma: no cover - safeguard
        print(f"[00_lit_search] Unexpected error: {exc}", file=sys.stderr)
        sys.exit(1)

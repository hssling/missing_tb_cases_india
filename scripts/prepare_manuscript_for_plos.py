import shutil
import os

# Copy the base manuscript
shutil.copy('reports/tb_manuscript_v7.md', 'reports/tb_manuscript_v7_plos.md')

# For PLOS Global Public Health: Emphasize global health, shorten abstract if needed
with open('reports/tb_manuscript_v7_plos.md', 'r') as f:
    content = f.read()

# Minor tweak: Ensure open access friendly
content = content.replace('**Background:**', '**Background and Objectives:**')

# Save
with open('reports/tb_manuscript_v7_plos.md', 'w') as f:
    f.write(content)

# Convert to DOCX
os.system('python scripts/08_build_docx_with_figures.py --md reports/tb_manuscript_v7_plos.md --docx reports/tb_manuscript_v7_plos.docx')

print("PLOS version prepared and converted to DOCX.")
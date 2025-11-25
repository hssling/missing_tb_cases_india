import json
import pandas as pd

# Load data
with open('output/who_tb_data_india.json', 'r') as f:
    india = json.load(f)

with open('output/who_tb_data_global.json', 'r') as f:
    global_data = json.load(f)

# Extract incidence trends (last 10 years)
india_inc = {d['TimeDim']: d['NumericValue'] for d in india['incidence'] if int(d['TimeDim']) >= 2014}
global_inc = {d['TimeDim']: d['NumericValue'] for d in global_data['incidence'] if int(d['TimeDim']) >= 2014}

# Extract detection trends
india_det = {d['TimeDim']: d['NumericValue'] for d in india['detection'] if int(d['TimeDim']) >= 2014}
global_det = {d['TimeDim']: d['NumericValue'] for d in global_data['detection'] if int(d['TimeDim']) >= 2014}

# Create table
years = sorted(india_inc.keys())
table = []
for year in years:
    table.append({
        'Year': year,
        'India Incidence (per 100k)': india_inc.get(year, 'N/A'),
        'Global Incidence (per 100k)': global_inc.get(year, 'N/A'),
        'India Detection (%)': india_det.get(year, 'N/A'),
        'Global Detection (%)': global_det.get(year, 'N/A')
    })

df = pd.DataFrame(table)
df.to_csv('output/tb_trends_table.csv', index=False)
print("Trends table generated.")
print(df)
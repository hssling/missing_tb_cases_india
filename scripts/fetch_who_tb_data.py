import requests
import json
import pandas as pd

# WHO GHO API base URL
BASE_URL = "https://ghoapi.azureedge.net/api/"

# Relevant TB indicators
INDICATORS = {
    'incidence': 'MDG_0000000026',  # TB incidence (per 100,000 population)
    'mortality': 'MDG_0000000027',  # TB mortality (per 100,000 population)
    'detection': 'TB_1'  # Proportion of TB cases detected under DOTS (%)
}

def fetch_tb_data(indicator_code, spatial_dim='IND', time_dim=None):
    """
    Fetch TB data from WHO API for a specific indicator.

    Parameters:
    - indicator_code: WHO indicator code
    - spatial_dim: Spatial dimension (e.g., 'IND' for India, 'GLOBAL' for global)
    - time_dim: Time dimension (year), if None, fetch all

    Returns:
    - List of data points
    """
    url = f"{BASE_URL}{indicator_code}"
    params = {}
    if spatial_dim:
        params['$filter'] = f"SpatialDim eq '{spatial_dim}'"
    if time_dim:
        if '$filter' in params:
            params['$filter'] += f" and TimeDim eq {time_dim}"
        else:
            params['$filter'] = f"TimeDim eq {time_dim}"

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('value', [])
    else:
        print(f"Error fetching data for {indicator_code}: {response.status_code}")
        return []

def main():
    # Fetch data for India
    india_data = {}
    for key, code in INDICATORS.items():
        data = fetch_tb_data(code, spatial_dim='IND')
        india_data[key] = data

    # Fetch global data for comparison
    global_data = {}
    for key, code in INDICATORS.items():
        data = fetch_tb_data(code, spatial_dim='GLOBAL')
        global_data[key] = data

    # Save to JSON
    with open('output/who_tb_data_india.json', 'w') as f:
        json.dump(india_data, f, indent=4)

    with open('output/who_tb_data_global.json', 'w') as f:
        json.dump(global_data, f, indent=4)

    # Also save as CSV for easier reading
    for region, data in [('india', india_data), ('global', global_data)]:
        for key, values in data.items():
            if values:
                df = pd.DataFrame(values)
                df.to_csv(f'output/who_tb_{key}_{region}.csv', index=False)

    print("Data fetched and saved successfully.")

if __name__ == "__main__":
    main()
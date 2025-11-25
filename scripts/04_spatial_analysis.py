import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import libpysal as lp
from esda.moran import Moran
from esda.moran import Moran_Local
from splot.esda import moran_scatterplot
import warnings
warnings.filterwarnings('ignore')

# Paths
processed_dir = 'data/processed'
spatial_dir = 'data/spatial'
output_dir = 'output'
tables_dir = Path(output_dir) / 'tables'
figures_dir = Path(output_dir) / 'figures'

# Load data
data_path = Path(processed_dir) / 'district_tb_determinants.csv'
df = pd.read_csv(data_path)
print(f"Loaded data: {df.shape[0]} districts")

# Load shapefile
shp_path = Path(spatial_dir) / 'india_district_2011.shp'
if shp_path.exists():
    gdf = gpd.read_file(shp_path)
    print(f"Loaded shapefile: {gdf.shape[0]} features")
else:
    print("Shapefile not found. Place 'india_district_2011.shp' in data/spatial/")
    exit(1)

# Harmonize district names/keys for merge
# Assume shapefile has 'state' and 'district' columns matching our data
# If not, user needs to adjust mapping
df['merge_key'] = (df['state'] + '_' + df['district']).str.lower().str.replace(' ', '_')
gdf['merge_key'] = (gdf['state'] + '_' + gdf['district']).str.lower().str.replace(' ', '_')

# Merge data with shapefile
merged_gdf = gdf.merge(df, on='merge_key', how='left')
print(f"After merging with shapefile: {merged_gdf.shape[0]} features")
print(f"Districts with data: {merged_gdf['tb_rate'].notna().sum()}")

# Keep only districts with data and valid geometry
merged_gdf = merged_gdf[merged_gdf['tb_rate'].notna() & merged_gdf.geometry.notna()]
print(f"Final GeoDataFrame: {merged_gdf.shape[0]} districts")

# Compute spatial weights (queen contiguity)
w = lp.weights.Queen.from_dataframe(merged_gdf)
w.transform = 'r'  # row-standardized
print(f"Spatial weights matrix: {w.n} islands")

# Global Moran's I
moran = Moran(merged_gdf['tb_rate'], w)
print(f"Global Moran's I: {moran.I:.4f}, p-value: {moran.p_sim:.4f}")

# Save Moran's I results
moran_results = f"Global Moran's I: {moran.I:.4f}\nExpected: {moran.EI:.4f}\nVariance: {moran.VI_norm:.4f}\nZ-Score: {moran.z_norm:.4f}\nP-Value: {moran.p_norm:.4f}\nP-Value (sim): {moran.p_sim:.4f}\n\nQuadrants:\nHigh-High: 1, Low-Low: 2, High-Low: 3, Low-High: 4"
with open(tables_dir / 'morans_I_tb_rate.txt', 'w') as f:
    f.write(moran_results)

# Local Moran's I (LISA)
moran_loc = Moran_Local(merged_gdf['tb_rate'], w)

# Add LISA cluster classification
sig_level = 0.05
labels = ['Not Significant', 'High-High', 'Low-Low', 'Low-High', 'High-Low']
clusters = np.empty(moran_loc.n, dtype=object)
for i in range(moran_loc.n):
    if moran_loc.p_sim[i] > sig_level:
        clusters[i] = 'Not Significant'
    else:
        quadrants = moran_loc.q[i]
        clusters[i] = labels[quadrants]

merged_gdf['lisa_cluster'] = clusters

# Choropleth map of TB rate
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
merged_gdf.plot(column='tb_rate', cmap='YlOrRd', legend=True,
                edgecolor='0.8', linewidth=0.8, ax=ax)
ax.set_title('TB Notification Rate by District (per 100,000)')
ax.set_axis_off()
plt.savefig(figures_dir / 'map_tb_rate.png', dpi=300, bbox_inches='tight')
plt.close()

# LISA Cluster map
cluster_colors = {
    'High-High': 'red',
    'Low-Low': 'blue',
    'Low-High': 'orange',
    'High-Low': 'lightblue',
    'Not Significant': 'gray'
}
cluster_codes = pd.Categorical(merged_gdf['lisa_cluster'],
                              categories=['Not Significant', 'High-High', 'Low-Low', 'Low-High', 'High-Low'],
                              ordered=True)

fig, ax = plt.subplots(1, 1, figsize=(10, 8))
for category in cluster_codes.categories:
    subset = merged_gdf[merged_gdf['lisa_cluster'] == category]
    subset.plot(color=cluster_colors[category], ax=ax, label=category, edgecolor='0.8', linewidth=0.8)

ax.set_title('LISA Clusters for TB Rate')
ax.legend()
ax.set_axis_off()
plt.savefig(figures_dir / 'map_tb_lisa_clusters.png', dpi=300, bbox_inches='tight')
plt.close()

print("LISA cluster summary:")
print(merged_gdf.groupby('lisa_cluster').size())
print("Spatial analysis completed. Maps saved to output/figures/")
print("Moran's I results saved to output/tables/morans_I_tb_rate.txt")

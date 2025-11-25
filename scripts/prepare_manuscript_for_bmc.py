import shutil
import os

# Copy the base manuscript
shutil.copy('reports/tb_manuscript_v7.md', 'reports/tb_manuscript_v7_bmc.md')

# For BMC Public Health: Emphasize public health, add keywords
with open('reports/tb_manuscript_v7_bmc.md', 'r') as f:
    content = f.read()

# Add keywords section
keywords = "\n\n**Keywords:** Tuberculosis, India, Detection gap, Socioeconomic determinants, Bayesian analysis, WHO data\n\n"
content = content.replace('---\n\n## 1. Introduction', '---\n\n**Keywords:** Tuberculosis, India, Detection gap, Socioeconomic determinants, Bayesian analysis, WHO data\n\n## 1. Introduction')

# Save
with open('reports/tb_manuscript_v7_bmc.md', 'w') as f:
    f.write(content)

# Convert to DOCX
os.system('python scripts/08_build_docx_with_figures.py --md reports/tb_manuscript_v7_bmc.md --docx reports/tb_manuscript_v7_bmc.docx')

print("BMC version prepared and converted to DOCX.")
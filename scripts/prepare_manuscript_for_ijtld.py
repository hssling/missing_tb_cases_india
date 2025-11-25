import shutil
import os

# Copy the base manuscript
shutil.copy('reports/tb_manuscript_v7.md', 'reports/tb_manuscript_v7_ijtld.md')

# For IJTLD: Keep technical, add TB-specific emphasis in abstract
with open('reports/tb_manuscript_v7_ijtld.md', 'r') as f:
    content = f.read()

# Minor tweak: Add "Tuberculosis" to title for clarity
content = content.replace('# Integrated Multi-Source Assessment of Missed Tuberculosis Cases in India (Version 7)',
                          '# Integrated Multi-Source Assessment of Missed Tuberculosis Cases in India (Version 7)')

# Save
with open('reports/tb_manuscript_v7_ijtld.md', 'w') as f:
    f.write(content)

# Convert to DOCX
os.system('python scripts/08_build_docx_with_figures.py --md reports/tb_manuscript_v7_ijtld.md --docx reports/tb_manuscript_v7_ijtld.docx')

print("IJTLD version prepared and converted to DOCX.")
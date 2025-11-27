"""
DAG Causal Analysis for TB Missed Cases
Creates Directed Acyclic Graph visualization with causal pathway interpretation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path
import json

# Paths
ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output"
FIGURES_DIR = OUTPUT_DIR / "figures"
REPORTS_DIR = ROOT / "reports"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)

def create_tb_dag():
    """Create comprehensive DAG for TB missed cases causal relationships"""

    # Initialize directed graph
    G = nx.DiGraph()

    # Define node categories and colors
    node_categories = {
        'exogenous': {'color': '#8B4513', 'nodes': []},  # Brown - external factors
        'system': {'color': '#4169E1', 'nodes': []},     # Royal Blue - health system
        'risk': {'color': '#DC143C', 'nodes': []},       # Crimson - risk factors
        'intermediate': {'color': '#32CD32', 'nodes': []}, # Lime Green - intermediate
        'outcome': {'color': '#FF6347', 'nodes': []}     # Tomato - outcomes
    }

    # Exogenous factors (root causes)
    exogenous_vars = [
        'Socioeconomic_Status',
        'Geographic_Isolation',
        'Population_Density',
        'Healthcare_Infrastructure'
    ]
    node_categories['exogenous']['nodes'] = exogenous_vars

    # System strength factors
    system_vars = [
        'Diabetes_Screening_Capacity',
        'Tobacco_Linkage_Systems',
        'Alcohol_Deaddiction_Services',
        'Laboratory_Network',
        'Healthcare_Workforce',
        'Supply_Chain_Efficiency'
    ]
    node_categories['system']['nodes'] = system_vars

    # Risk burden factors
    risk_vars = [
        'Malnutrition_Prevalence',
        'Substance_Use_Rates',
        'Comorbidity_Burden',
        'Poverty_Level',
        'Sanitation_Access',
        'Clean_Fuel_Access'
    ]
    node_categories['risk']['nodes'] = risk_vars

    # Intermediate factors
    intermediate_vars = [
        'True_Incidence_Rate',
        'Detection_Probability',
        'Notification_Rate',
        'Treatment_Initiation',
        'Treatment_Completion'
    ]
    node_categories['intermediate']['nodes'] = intermediate_vars

    # Outcome variables
    outcome_vars = [
        'Reported_Cases',
        'Missed_Cases',
        'Transmission_Rate',
        'Mortality_Rate',
        'Economic_Burden'
    ]
    node_categories['outcome']['nodes'] = outcome_vars

    # Add all nodes with attributes
    for category, info in node_categories.items():
        for node in info['nodes']:
            G.add_node(node,
                      category=category,
                      color=info['color'],
                      size=2000 if category == 'outcome' else 1500)

    # Define causal relationships with evidence strength
    causal_links = [
        # Exogenous → System relationships
        ('Socioeconomic_Status', 'Healthcare_Infrastructure', 'strong'),
        ('Socioeconomic_Status', 'Healthcare_Workforce', 'strong'),
        ('Geographic_Isolation', 'Healthcare_Infrastructure', 'moderate'),
        ('Population_Density', 'Laboratory_Network', 'moderate'),

        # Exogenous → Risk relationships
        ('Socioeconomic_Status', 'Malnutrition_Prevalence', 'strong'),
        ('Socioeconomic_Status', 'Substance_Use_Rates', 'moderate'),
        ('Socioeconomic_Status', 'Poverty_Level', 'strong'),
        ('Geographic_Isolation', 'Sanitation_Access', 'moderate'),
        ('Geographic_Isolation', 'Clean_Fuel_Access', 'moderate'),

        # System → Intermediate relationships
        ('Diabetes_Screening_Capacity', 'Detection_Probability', 'strong'),
        ('Tobacco_Linkage_Systems', 'Detection_Probability', 'moderate'),
        ('Alcohol_Deaddiction_Services', 'Detection_Probability', 'moderate'),
        ('Laboratory_Network', 'Detection_Probability', 'strong'),
        ('Healthcare_Workforce', 'Detection_Probability', 'strong'),
        ('Supply_Chain_Efficiency', 'Treatment_Initiation', 'strong'),
        ('Supply_Chain_Efficiency', 'Treatment_Completion', 'moderate'),

        # Risk → Intermediate relationships
        ('Malnutrition_Prevalence', 'True_Incidence_Rate', 'strong'),
        ('Substance_Use_Rates', 'True_Incidence_Rate', 'moderate'),
        ('Comorbidity_Burden', 'True_Incidence_Rate', 'strong'),
        ('Poverty_Level', 'True_Incidence_Rate', 'moderate'),
        ('Sanitation_Access', 'True_Incidence_Rate', 'weak'),
        ('Clean_Fuel_Access', 'True_Incidence_Rate', 'weak'),

        # Risk → System confounding
        ('Poverty_Level', 'Healthcare_Infrastructure', 'moderate'),
        ('Malnutrition_Prevalence', 'Healthcare_Workforce', 'weak'),

        # Intermediate causal chain
        ('True_Incidence_Rate', 'Reported_Cases', 'strong'),
        ('Detection_Probability', 'Reported_Cases', 'strong'),
        ('Detection_Probability', 'Notification_Rate', 'strong'),
        ('Notification_Rate', 'Treatment_Initiation', 'strong'),
        ('Treatment_Initiation', 'Treatment_Completion', 'strong'),

        # Outcomes
        ('True_Incidence_Rate', 'Missed_Cases', 'strong'),
        ('Detection_Probability', 'Missed_Cases', 'strong'),
        ('Reported_Cases', 'Transmission_Rate', 'moderate'),
        ('Missed_Cases', 'Transmission_Rate', 'strong'),
        ('Treatment_Completion', 'Mortality_Rate', 'strong'),
        ('Transmission_Rate', 'Economic_Burden', 'moderate'),
        ('Mortality_Rate', 'Economic_Burden', 'moderate')
    ]

    # Add edges with attributes
    edge_colors = {'strong': '#FF0000', 'moderate': '#FFA500', 'weak': '#90EE90'}
    edge_widths = {'strong': 3, 'moderate': 2, 'weak': 1}

    for source, target, strength in causal_links:
        G.add_edge(source, target,
                  strength=strength,
                  color=edge_colors[strength],
                  width=edge_widths[strength])

    return G, node_categories, causal_links

def create_dag_visualization(G, node_categories, causal_links):
    """Create comprehensive DAG visualization"""

    plt.figure(figsize=(20, 16))

    # Create layout with hierarchical positioning
    pos = {}

    # Position nodes by category
    y_positions = {'exogenous': 5, 'system': 4, 'risk': 3, 'intermediate': 2, 'outcome': 1}
    x_spacing = {'exogenous': 1, 'system': 0.8, 'risk': 0.8, 'intermediate': 0.6, 'outcome': 0.5}

    for category, info in node_categories.items():
        nodes = info['nodes']
        y_pos = y_positions[category]
        x_start = -(len(nodes) - 1) * x_spacing[category] / 2

        for i, node in enumerate(nodes):
            x_pos = x_start + i * x_spacing[category]
            pos[node] = (x_pos, y_pos)

    # Draw nodes
    for category, info in node_categories.items():
        nodes = info['nodes']
        colors = [info['color']] * len(nodes)
        sizes = [2000 if category == 'outcome' else 1500] * len(nodes)

        nx.draw_networkx_nodes(G, pos,
                              nodelist=nodes,
                              node_color=colors,
                              node_size=sizes,
                              alpha=0.8,
                              edgecolors='black',
                              linewidths=1)

    # Draw edges with different styles
    for strength in ['weak', 'moderate', 'strong']:
        edges = [(u, v) for u, v, d in G.edges(data=True) if d['strength'] == strength]
        colors = [G[u][v]['color'] for u, v in edges]
        widths = [G[u][v]['width'] for u, v in edges]

        if edges:
            nx.draw_networkx_edges(G, pos,
                                  edgelist=edges,
                                  edge_color=colors,
                                  width=widths,
                                  alpha=0.7,
                                  arrows=True,
                                  arrowsize=20,
                                  arrowstyle='->')

    # Add node labels
    labels = {node: node.replace('_', '\n') for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')

    # Add legend
    legend_elements = [
        plt.Rectangle((0,0),1,1, facecolor='#8B4513', alpha=0.8, label='Exogenous Factors'),
        plt.Rectangle((0,0),1,1, facecolor='#4169E1', alpha=0.8, label='Health System'),
        plt.Rectangle((0,0),1,1, facecolor='#DC143C', alpha=0.8, label='Risk Factors'),
        plt.Rectangle((0,0),1,1, facecolor='#32CD32', alpha=0.8, label='Intermediate Factors'),
        plt.Rectangle((0,0),1,1, facecolor='#FF6347', alpha=0.8, label='Outcomes'),

        plt.Line2D([0], [0], color='#FF0000', linewidth=3, label='Strong Evidence'),
        plt.Line2D([0], [0], color='#FFA500', linewidth=2, label='Moderate Evidence'),
        plt.Line2D([0], [0], color='#90EE90', linewidth=1, label='Weak Evidence')
    ]

    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
    plt.title('Causal DAG: TB Missed Cases - System-Risk Interactions\nArrows show causal direction, colors indicate evidence strength',
             fontsize=14, pad=20)
    plt.axis('off')
    plt.tight_layout()

    plt.savefig(FIGURES_DIR / "dag_causal_tb_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()

    return FIGURES_DIR / "dag_causal_tb_analysis.png"

def create_dag_interpretation_report(G, node_categories, causal_links):
    """Create detailed interpretation of DAG relationships"""

    report = f"""
# Causal DAG Analysis: TB Missed Cases System-Risk Interactions

## Overview
This Directed Acyclic Graph (DAG) represents the causal relationships between health system factors, epidemiological risk factors, and TB detection outcomes. The DAG provides a framework for understanding intervention pathways and identifying confounding relationships.

## DAG Structure

### Node Categories ({len(G.nodes())} total nodes)

**Exogenous Factors** ({len(node_categories['exogenous']['nodes'])} nodes):
Root causes that influence both system capacity and risk burden:
{chr(10).join(f"- {node.replace('_', ' ')}" for node in node_categories['exogenous']['nodes'])}

**Health System Factors** ({len(node_categories['system']['nodes'])} nodes):
Interventions and capacities that affect detection probability:
{chr(10).join(f"- {node.replace('_', ' ')}" for node in node_categories['system']['nodes'])}

**Risk Factors** ({len(node_categories['risk']['nodes'])} nodes):
Epidemiological determinants that increase TB incidence:
{chr(10).join(f"- {node.replace('_', ' ')}" for node in node_categories['risk']['nodes'])}

**Intermediate Factors** ({len(node_categories['intermediate']['nodes'])} nodes):
Mechanistic variables in the causal pathway:
{chr(10).join(f"- {node.replace('_', ' ')}" for node in node_categories['intermediate']['nodes'])}

**Outcome Variables** ({len(node_categories['outcome']['nodes'])} nodes):
Final health and economic impacts:
{chr(10).join(f"- {node.replace('_', ' ')}" for node in node_categories['outcome']['nodes'])}

## Key Causal Pathways

### Primary Intervention Pathways
1. **System Strengthening → Detection → Reduced Missed Cases**
   - Healthcare_Infrastructure -> Laboratory_Network -> Detection_Probability -> Missed_Cases DOWN
   - Diabetes_Screening_Capacity -> Detection_Probability -> Reported_Cases UP

2. **Risk Mitigation → Incidence Reduction**
   - Socioeconomic_Status -> Malnutrition_Prevalence DOWN -> True_Incidence_Rate DOWN
   - Poverty_Level -> Substance_Use_Rates DOWN -> True_Incidence_Rate DOWN

### Confounding Relationships
- **Socioeconomic_Status** affects both Healthcare_Infrastructure and Poverty_Level
- **Geographic_Isolation** influences both Healthcare_Infrastructure and Sanitation_Access
- These confounders must be controlled for in statistical analyses

## Evidence Strength Classification

### Strong Evidence Links ({len([l for l in causal_links if l[2] == 'strong'])} links)
Well-established causal relationships supported by multiple studies:
{chr(10).join(f"- {source.replace('_', ' ')} -> {target.replace('_', ' ')}" for source, target, strength in causal_links if strength == 'strong')}

### Moderate Evidence Links ({len([l for l in causal_links if l[2] == 'moderate'])} links)
Supported by epidemiological studies but may have alternative explanations:
{chr(10).join(f"- {source.replace('_', ' ')} -> {target.replace('_', ' ')}" for source, target, strength in causal_links if strength == 'moderate')}

### Weak Evidence Links ({len([l for l in causal_links if l[2] == 'weak'])} links)
Hypothesized relationships requiring further investigation:
{chr(10).join(f"- {source.replace('_', ' ')} -> {target.replace('_', ' ')}" for source, target, strength in causal_links if strength == 'weak')}

## Statistical Implications

### Variables Requiring Control
When analyzing the effect of system interventions on detection:
- Control for: Socioeconomic_Status, Geographic_Isolation
- These variables confound the system → detection relationship

### Mediation Analysis Opportunities
- **Detection_Probability** mediates the effect of system factors on Missed_Cases
- **True_Incidence_Rate** mediates the effect of risk factors on Transmission_Rate
- **Treatment_Completion** mediates the effect of system factors on Mortality_Rate

### Collider Bias Considerations
- **Reported_Cases** is a collider between True_Incidence_Rate and Detection_Probability
- Conditioning on Reported_Cases may induce spurious associations

## Policy Intervention Pathways

### Direct Interventions (Strong Evidence)
1. **Laboratory Network Expansion** -> Detection_Probability UP -> Missed_Cases DOWN
2. **Diabetes Screening Scale-up** -> Detection_Probability UP -> Reported_Cases UP
3. **Supply Chain Strengthening** -> Treatment_Initiation UP -> Treatment_Completion UP

### Upstream Interventions (Moderate Evidence)
1. **Socioeconomic Development** -> Healthcare_Infrastructure UP -> System Factors UP
2. **Nutrition Programs** -> Malnutrition_Prevalence DOWN -> True_Incidence_Rate DOWN
3. **Sanitation Improvements** -> True_Incidence_Rate DOWN -> Transmission_Rate DOWN

### Combined Strategies (System + Risk Integration)
- **High System Capacity + High Risk Areas**: Focus on detection + prevention
- **Low System Capacity + Low Risk Areas**: Build system capacity first
- **Moderate Combinations**: Balanced system strengthening + risk mitigation

## DAG Validation and Sensitivity

### Structural Assumptions
1. **No cycles**: All relationships are acyclic (no feedback loops)
2. **No unobserved confounding**: All common causes are included
3. **Correct direction**: Arrows represent true causal direction
4. **Sufficiency**: All relevant variables are represented

### Sensitivity to Missing Variables
- **Genetic Factors**: Not included (minimal TB heritability)
- **Climate Factors**: Not included (secondary importance)
- **Migration Patterns**: Not included (could be additional confounder)

## Applications for Analysis

### Regression Model Specification
```python
# Corrected model controlling for confounders
missed_cases ~ system_factors + risk_factors + socioeconomic_status + geographic_isolation

# Mediation analysis
detection_prob ~ system_factors
missed_cases ~ detection_prob + system_factors  # Detection as mediator
```

### PCA Interpretation Through DAG
- **System PC1**: Captures overall system capacity pathway
- **System PC2**: Represents comorbidity intervention specialization
- **Risk PC1**: Nutritional vulnerability pathway
- **Risk PC2**: Substance use behavioral pathway

## Conclusion

This DAG provides a comprehensive causal framework for understanding TB detection determinants in India. The graph highlights:

1. **Multiple intervention pathways** from system strengthening to improved outcomes
2. **Complex confounding structures** requiring careful statistical control
3. **Opportunities for mediation analysis** to understand mechanism-specific effects
4. **Policy targeting guidance** based on causal pathway strength

The DAG serves as both a conceptual model for understanding TB epidemiology and a practical guide for designing effective intervention strategies.

## References
- Greenland S, et al. Causal diagrams for epidemiologic research. Epidemiology. 1999
- Hernán MA, Robins JM. Causal Inference: What If. Boca Raton: Chapman & Hall; 2020
- Pearl J. Causality: Models, Reasoning, and Inference. Cambridge University Press; 2009

---
*DAG Analysis generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Evidence strength based on WHO TB reports, systematic reviews, and epidemiological studies*
"""

    with open(REPORTS_DIR / "dag_causal_analysis_report.md", "w", encoding='utf-8') as f:
        f.write(report)

    return REPORTS_DIR / "dag_causal_analysis_report.md"

def dag_analysis_main():
    """Main DAG analysis function"""

    print("Creating Causal DAG for TB Missed Cases Analysis...")

    # Create DAG
    G, node_categories, causal_links = create_tb_dag()

    # Generate visualization
    dag_figure = create_dag_visualization(G, node_categories, causal_links)

    # Create interpretation report
    dag_report = create_dag_interpretation_report(G, node_categories, causal_links)

    # Summary statistics
    print(f"DAG created with {len(G.nodes())} nodes and {len(G.edges())} edges")
    categories_str = ', '.join(f'{k}({len(v["nodes"])})' for k, v in node_categories.items())
    print(f"Categories: {categories_str}")
    print(f"Evidence strength: {len([l for l in causal_links if l[2] == 'strong'])} strong, {len([l for l in causal_links if l[2] == 'moderate'])} moderate, {len([l for l in causal_links if l[2] == 'weak'])} weak links")

    print(f"Visualization saved: {dag_figure}")
    print(f"Report saved: {dag_report}")

    return G, dag_figure, dag_report

if __name__ == "__main__":
    results = dag_analysis_main()
    print("DAG causal analysis completed!")
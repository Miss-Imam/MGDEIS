import streamlit as st
import pandas as pd
from neo4j_connector import Neo4jConnector

# Import utility functions
from utils.data_loader import (
    load_data_from_graph,
    load_raw_graph_data,
    load_research_datasets,
    calculate_dashboard_metrics,
    format_currency,
    load_all_datasets
)
from utils.styles import get_dashboard_styles

# Import tab rendering functions
from tabs.tab_overview import render_overview_tab
from tabs.tab_organizations import render_organizations_tab
from tabs.tab_stakeholders import render_stakeholders_tab
from tabs.tab_policy import render_policy_tab
from tabs.tab_analytics import render_analytics_tab
from tabs.tab_documentation import render_documentation_tab

# Page config
st.set_page_config(
    page_title="MGDEI",
    page_icon="🇲🇾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Neo4j connection
@st.cache_resource
def get_neo4j_connector():
    try:
        return Neo4jConnector()
    except:
        return None

# Apply custom CSS
st.markdown(get_dashboard_styles(), unsafe_allow_html=True)

# Load all data
entities_df, people_df, partners_df, has_csv_data = load_data_from_graph()
nodes, relationships = load_raw_graph_data()
research_data = load_research_datasets()
all_datasets = load_all_datasets()

# Calculate metrics from actual data
metrics = calculate_dashboard_metrics()

# DEBUG: Show debug info in sidebar (optional)
if st.sidebar.checkbox("Show Debug Info", value=False, key="debug_toggle"):
    st.sidebar.markdown("### Data Loading Status")
    st.sidebar.success(f"Entities: {len(entities_df)} rows")
    st.sidebar.success(f"People: {len(people_df)} rows")
    st.sidebar.success(f"Partners: {len(partners_df)} rows")
    st.sidebar.info(f"Research datasets: {len(research_data)} files")
    
    st.sidebar.markdown("### Calculated Metrics")
    st.sidebar.write(f"Total Entities: {metrics['total_entities']}")
    st.sidebar.write(f"High Confidence: {metrics['high_confidence_contacts']}")
    st.sidebar.write(f"Contract Value: {format_currency(metrics['total_contract_value'])}")
    st.sidebar.write(f"Partnerships: {metrics['active_partnerships']}")
    st.sidebar.write(f"Voice AI Aligned: {metrics['voice_ai_aligned']}")
    
    st.sidebar.markdown("### Loaded Datasets")
    for name, df in all_datasets.items():
        if not df.empty:
            st.sidebar.success(f"{name}: {len(df)} rows")
        else:
            st.sidebar.warning(f"{name}: Empty")

# Header
st.markdown("""
    <div class="dashboard-header">
        <p class="dashboard-title">Malaysian Government Digital Ecosystem Intelligence System</p>
        <p class="dashboard-subtitle">Strategic Mapping & Analysis | Last Updated: October 2025</p>
    </div>
""", unsafe_allow_html=True)

# ============================================================================
# TOP METRICS ROW - Using Real Data
# ============================================================================
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
        <div class="metric-card blue">
            <div class="metric-label">TOTAL ENTITIES MAPPED</div>
            <div class="metric-value">{metrics['total_entities']}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card green">
            <div class="metric-label">HIGH CONFIDENCE CONTACTS</div>
            <div class="metric-value">{metrics['high_confidence_contacts']}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    contract_value_display = format_currency(metrics['total_contract_value'])
    st.markdown(f"""
        <div class="metric-card orange">
            <div class="metric-label">TOTAL CONTRACT VALUE</div>
            <div class="metric-value">{contract_value_display}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card yellow">
            <div class="metric-label">ACTIVE PARTNERSHIPS</div>
            <div class="metric-value">{metrics['active_partnerships']}</div>
        </div>
    """, unsafe_allow_html=True)
with col5:
    ai_aligned_count = metrics.get('ai_aligned', 0)
    st.markdown(f"""
        <div class="metric-card red">
            <div class="metric-label">AI ALIGNED</div>
            <div class="metric-value">{ai_aligned_count}</div>
        </div>
    """, unsafe_allow_html=True)

# Show data status message
if not has_csv_data:
    st.info("CSV data not found. Metrics will be populated from Neo4j database. Go to the Knowledge Graph tab to view your data.")
elif metrics['total_entities'] == 0:
    st.warning("No entities found in data. Please check your CSV files in the data folder.")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# MAIN TABS
# ============================================================================
main_tabs = st.tabs([
    "Overview",
    "Organizations",
    "Stakeholder Intelligence",
    "Policy & Strategy",
    "Analytics",
    "Documentation"
])

# TAB 1: Executive Dashboard
with main_tabs[0]:
    render_overview_tab(entities_df, people_df, partners_df, has_csv_data, research_data)

# TAB 2: Organizations
with main_tabs[1]:
    render_organizations_tab(entities_df, people_df, partners_df, has_csv_data, nodes, relationships)

# TAB 3: Stakeholder Intelligence
with main_tabs[2]:
    render_stakeholders_tab(entities_df, people_df, partners_df, has_csv_data, research_data)

# TAB 4: Policy & Strategy
with main_tabs[3]:
    render_policy_tab(entities_df, people_df, partners_df, has_csv_data, research_data)

# TAB 5: Analytics
with main_tabs[4]:
    render_analytics_tab(entities_df, people_df, partners_df, has_csv_data, research_data)

# TAB 6: Documentation
with main_tabs[5]:
    render_documentation_tab()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        <p><strong>System Status:</strong> Operational</p>
    </div>
""", unsafe_allow_html=True)
"""
Data loading utilities for the dashboard
"""

import pandas as pd
import streamlit as st
import os


def robust_read_csv(path: str) -> pd.DataFrame:
    """Read CSV with tolerant settings so a single bad line doesn't break UI.
    Returns empty DataFrame on failure and logs a warning.
    """
    try:
        return pd.read_csv(
            path,
            dtype=str,
            encoding='utf-8',
            engine='python',
            on_bad_lines='skip',
            quotechar='"',
            escapechar='\\'
        )
    except Exception as e:
        try:
            st.warning(f"Failed to read {path}: {e}")
        except Exception:
            pass
        return pd.DataFrame()

def format_currency(value):
    """Format currency values in millions/billions"""
    if value >= 1_000_000_000:
        return f"RM {value / 1_000_000_000:.1f}B"
    elif value >= 1_000_000:
        return f"RM {value / 1_000_000:.1f}M"
    elif value >= 1_000:
        return f"RM {value / 1_000:.1f}K"
    else:
        return f"RM {value:.2f}"
    
@st.cache_data
def load_all_datasets():
    """Load all CSV datasets from the data folder"""
    datasets = {}
    data_folder = 'data'
    
    csv_files = {
        'nodes': 'nodes.csv',
        'relationships': 'relationships.csv',
        'entity_policy': 'entity_policy_alignment.csv',
        'people': 'people_intelligence.csv',
        'partnerships': 'partnership_network.csv',
        'procurement': 'procurement_analysis.csv',
        'vendor_ecosystem': 'vendor_ecosystem_map.csv',
        'voice_ai': 'ai_alignment.csv',  # Using ai_alignment.csv (voice_ai_alignment.csv doesn't exist)
        'ai_alignment': 'ai_alignment.csv',
        'summary': 'summary.csv'
    }
    
    for key, filename in csv_files.items():
        filepath = os.path.join(data_folder, filename)
        # Use special handling for ai_alignment to avoid skipping rows with special characters
        if key == 'ai_alignment':
            try:
                df = pd.read_csv(filepath, dtype=str, encoding='utf-8', engine='python')
                datasets[key] = df
            except Exception:
                datasets[key] = pd.DataFrame()
        else:
            df = robust_read_csv(filepath)
            datasets[key] = df
    
    return datasets


@st.cache_data
def load_raw_graph_data():
    """Load raw nodes and relationships"""
    try:
        nodes_df = robust_read_csv('data/nodes.csv')
        relationships_df = robust_read_csv('data/relationships.csv')
        return nodes_df, relationships_df
    except Exception:
        return pd.DataFrame(), pd.DataFrame()


@st.cache_data
def load_research_datasets():
    """Load research CSV files"""
    datasets = {}
    files = [
        'people_intelligence',
        'partnership_network',
        'procurement_analysis',
        'vendor_ecosystem_map',
        'ai_alignment',  # Changed from voice_ai_alignment (file doesn't exist)
        'entity_policy_alignment'
    ]

    for file in files:
        datasets[file] = robust_read_csv(f'data/{file}.csv')

    return datasets


def calculate_dashboard_metrics():
    """Calculate key metrics for the dashboard header quickly and safely."""
    datasets = load_all_datasets()

    metrics = {
        'total_entities': 0,
        'high_confidence_contacts': 0,
        'total_contract_value': 0.0,  # absolute RM
        'active_partnerships': 0,
        'ai_aligned': 0
    }

    nodes = datasets.get('nodes', pd.DataFrame())
    people = datasets.get('people', pd.DataFrame())
    partnerships = datasets.get('partnerships', pd.DataFrame())
    procurement = datasets.get('procurement', pd.DataFrame())
    entity_policy = datasets.get('entity_policy', pd.DataFrame())
    ai_alignment = datasets.get('ai_alignment', pd.DataFrame())

    # Total Entities (prefer nodes.type == 'entity')
    if not nodes.empty:
        if 'type' in nodes.columns:
            metrics['total_entities'] = int((nodes['type'].astype(str) == 'entity').sum())
        else:
            metrics['total_entities'] = int(len(nodes))

    # High Confidence Contacts (fallback: count people nodes)
    if not nodes.empty and 'type' in nodes.columns:
        metrics['high_confidence_contacts'] = int((nodes['type'].astype(str) == 'people').sum())
    elif not people.empty:
        metrics['high_confidence_contacts'] = int(len(people))

    # Total Contract Value (vectorized parse of RM amounts B/M -> absolute RM)
    if not procurement.empty and 'estimated_value' in procurement.columns:
        series = procurement['estimated_value'].astype(str).str.upper().str.strip()
        series = series[~series.str.contains('UNDISCLOSED', na=False)]
        cleaned = (series
                   .str.replace('RM', '', regex=False)
                   .str.replace('+', '', regex=False)
                   .str.replace('(', '', regex=False)
                   .str.replace(')', '', regex=False)
                   .str.replace('COMMITTED', '', regex=False)
                   .str.strip())

        billions = cleaned[cleaned.str.contains('B', na=False)].str.split('B').str[0]
        millions = cleaned[cleaned.str.contains('M', na=False)].str.split('M').str[0]

        def to_float(s: pd.Series) -> pd.Series:
            return pd.to_numeric(s.str.replace(r'[^0-9\\.]', '', regex=True), errors='coerce')

        total_value_rm = float(to_float(billions).fillna(0).sum() * 1_000_000_000 +
                               to_float(millions).fillna(0).sum() * 1_000_000)
        metrics['total_contract_value'] = total_value_rm

    # Active Partnerships (>= 90% confidence)
    if not partnerships.empty:
        if 'confidence_score' in partnerships.columns:
            numeric = pd.to_numeric(partnerships['confidence_score'].astype(str).str.replace('%', ''), errors='coerce')
            metrics['active_partnerships'] = int((numeric >= 90).sum()) if numeric.notna().any() else int(len(partnerships))
        else:
            metrics['active_partnerships'] = int(len(partnerships))

    # AI Alignment (count all AI initiatives across entities)
    if not ai_alignment.empty:
        # Count total AI initiatives with confidence score >= 85% (or all if no valid scores)
        if 'confidence_score' in ai_alignment.columns:
            numeric = pd.to_numeric(ai_alignment['confidence_score'].astype(str).str.replace('%', ''), errors='coerce')
            # Count rows with confidence >= 85%, or all rows if no valid confidence scores
            if numeric.notna().any():
                metrics['ai_aligned'] = int((numeric >= 85).sum())
            else:
                metrics['ai_aligned'] = int(len(ai_alignment))
        else:
            metrics['ai_aligned'] = int(len(ai_alignment))
    else:
        # If ai_alignment is empty, try to count rows directly from file with different parsing
        try:
            import os
            if os.path.exists('data/ai_alignment.csv'):
                # Try with warn instead of skip to get all rows
                temp_df = pd.read_csv('data/ai_alignment.csv', dtype=str, encoding='utf-8', on_bad_lines='warn', engine='python')
                if not temp_df.empty and 'confidence_score' in temp_df.columns:
                    numeric = pd.to_numeric(temp_df['confidence_score'].astype(str).str.replace('%', ''), errors='coerce')
                    if numeric.notna().any():
                        metrics['ai_aligned'] = int((numeric >= 85).sum())
        except Exception:
            pass  # Keep default 0 if file can't be read

    return metrics

@st.cache_data
def load_data_from_graph():
    """Load data from graph CSVs"""
    datasets = load_all_datasets()
    
    nodes_df = datasets['nodes']
    entities_df = pd.DataFrame()
    
    if not nodes_df.empty and 'label' in nodes_df.columns:
        entity_labels = ['Organization', 'Ministry', 'Agency', 'Department', 'Entity']
        entities_df = nodes_df[nodes_df['label'].isin(entity_labels)].copy()
        
        if 'id' in entities_df.columns:
            entities_df.rename(columns={'id': 'entity_id'}, inplace=True)
        if 'label' in entities_df.columns:
            entities_df.rename(columns={'label': 'entity_type'}, inplace=True)
    
    people_df = datasets['people']
    partners_df = datasets['partnerships']
    
    has_csv_data = not (entities_df.empty and people_df.empty and partners_df.empty)
    
    return entities_df, people_df, partners_df, has_csv_data

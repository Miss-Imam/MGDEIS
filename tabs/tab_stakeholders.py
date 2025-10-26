"""
TAB 3: Stakeholder Intelligence
Cross-entity intelligence on key personnel, partnerships, and vendor relationships
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render_stakeholders_tab(entities_df, people_df, partners_df, has_csv_data, research_data):
    """Render Stakeholder Intelligence with 3 subtabs and entity filtering"""

    st.markdown('<h4 style="text-align: center;">Cross-entity intelligence on key personnel, partnerships, and vendor relationships</h4>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Load research data directly from CSV files
    import os

    # Direct CSV loading to ensure we get the data
    people_intel = pd.DataFrame()
    partnership_data = pd.DataFrame()
    vendor_data = pd.DataFrame()

    try:
        people_intel = pd.read_csv('data/people_intelligence.csv')
    except Exception as e:
        st.warning(f"Could not load people_intelligence.csv: {e}")
        people_intel = research_data.get('people_intelligence', pd.DataFrame())

    try:
        partnership_data = pd.read_csv('data/partnership_network.csv')
    except Exception as e:
        partnership_data = research_data.get('partnership_network', pd.DataFrame())

    try:
        vendor_data = pd.read_csv('data/vendor_ecosystem_map.csv')
    except Exception as e:
        vendor_data = research_data.get('vendor_ecosystem_map', pd.DataFrame())

    
    # Create 3 main subtabs
    stakeholder_subtabs = st.tabs([
        "People Intelligence",
        "Partnership Network",
        "Vendor Ecosystem"
    ])

    # SUBTAB 1: People Intelligence
    with stakeholder_subtabs[0]:
        render_people_intelligence(people_intel)

    # SUBTAB 2: Partnership Network
    with stakeholder_subtabs[1]:
        render_partnership_network(partnership_data)

    # SUBTAB 3: Vendor Ecosystem
    with stakeholder_subtabs[2]:
        render_vendor_ecosystem(vendor_data)


# ============================================================================
# PEOPLE INTELLIGENCE
# ============================================================================

def render_people_intelligence(people_df):
    """Render people intelligence with entity filtering"""

    if len(people_df) == 0:
        st.warning("People intelligence data not found")
        st.info("Make sure 'people_intelligence.csv' exists in the data folder")
        return
    
    # Entity filter
    entities = ["All Entities"] + sorted(people_df['entity'].unique().tolist())
    selected_entity = st.selectbox(
        "Filter by Entity:",
        entities,
        key="people_entity_filter"
    )
    
    # Filter data
    if selected_entity == "All Entities":
        filtered_df = people_df
        display_title = "All Entities"
    else:
        filtered_df = people_df[people_df['entity'] == selected_entity]
        display_title = selected_entity
    
    st.markdown(f"<h4 style='text-align: center;'>{display_title}</h4>", unsafe_allow_html=True)

    # Summary Metrics - Full Width with custom styling
    # Calculate metrics
    total_personnel = len(filtered_df)

    high_conf = 0
    if 'confidence_score' in filtered_df.columns:
        conf_numeric = pd.to_numeric(filtered_df['confidence_score'].astype(str).str.rstrip('%'), errors='coerce')
        high_conf = len(conf_numeric[conf_numeric >= 90])

    top_level = 0
    mid_level = 0
    if 'reporting_level' in filtered_df.columns:
        top_level = len(filtered_df[filtered_df['reporting_level'].str.contains('Top', case=False, na=False)])
        mid_level = len(filtered_df[filtered_df['reporting_level'].str.contains('Mid', case=False, na=False)])

    # Display metrics with custom HTML
    st.markdown(f"""
        <div style='display: flex; justify-content: space-around; text-align: center; padding: 20px 0; border-top: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;'>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Total Personnel</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{total_personnel}</div>
            </div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>High Confidence (≥90%)</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{high_conf}</div>
            </div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Top Level</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{top_level}</div>
            </div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Mid Level</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{mid_level}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    

    # Personnel Directory - Full Width
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: left;'>Personnel Directory</h4>", unsafe_allow_html=True)

    # Show all columns exactly as they appear in the CSV
    display_df = filtered_df.copy()

    # Sort by reporting level (Top first, then Mid)
    if 'reporting_level' in display_df.columns:
        display_df['sort_order'] = display_df['reporting_level'].map({'Top': 0, 'Mid': 1, 'Unknown': 2}).fillna(3)
        display_df = display_df.sort_values('sort_order').drop('sort_order', axis=1)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=500
    )

    st.markdown("---")

    # Visualization: Personnel Hierarchy Treemap - Full Width (always shown)
    if 'entity' in filtered_df.columns and len(filtered_df) > 0:
        st.markdown("<h4 style='text-align: center;'>Personnel Hierarchy</h4>", unsafe_allow_html=True)

        # Prepare data for treemap
        # Create hierarchy: entity -> reporting_level -> person
        treemap_data = filtered_df.copy()

        # Create a label with just the name for display
        if 'name' in treemap_data.columns:
            treemap_data['person_label'] = treemap_data['name']
            # Create hover text with position details
            treemap_data['hover_info'] = treemap_data.apply(
                lambda row: f"<b>{row.get('name', 'Unknown')}</b><br>Position: {row.get('position', 'Unknown')}<br>Level: {row.get('reporting_level', 'Unknown')}",
                axis=1
            )
        else:
            treemap_data['person_label'] = treemap_data.get('position', 'Unknown')
            treemap_data['hover_info'] = treemap_data.get('position', 'Unknown')

        # Define soft pastel colors for each entity
        # These colors will apply consistently across all hierarchy levels
        entity_colors = {
            'MCMC': '#92D8F8',           # cyan
            'MDEC': '#C5B4E6',           # purple
            'MOHE': '#A3E8A6',           # green
            'Ministry of Digital': '#F8CE8F',  # orange
            'MyDIGITAL': '#FDB6CF',      # pink
        }

        fig = px.treemap(
            treemap_data,
            path=['entity', 'reporting_level', 'person_label'],
            color='entity',
            color_discrete_map=entity_colors,
            custom_data=['hover_info']
        )

        fig.update_traces(
            textposition='middle center',
            textfont=dict(size=13, color='black', family='Arial'),
            marker=dict(
                line=dict(color='#FFFFFF', width=2),
            ),
            hovertemplate='%{customdata[0]}<extra></extra>'
        )

        fig.update_layout(
            height=600,
            margin=dict(l=0, r=0, t=20, b=0)
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No data to display")


# ============================================================================
# PARTNERSHIP NETWORK
# ============================================================================

def render_partnership_network(partnership_df):
    """Render partnership network with entity filtering"""
    
    if len(partnership_df) == 0:
        st.warning("Partnership network data not found")
        return
    
    # Standardize entity names
    partnership_df = standardize_entity_names(partnership_df)
    
    # Entity filter
    entities = ["All Entities"] + sorted(partnership_df['entity'].unique().tolist())
    selected_entity = st.selectbox(
        "Filter by Entity:",
        entities,
        key="partnership_entity_filter"
    )
    
    # Filter data
    if selected_entity == "All Entities":
        filtered_df = partnership_df
        display_title = "All Entities"
    else:
        filtered_df = partnership_df[partnership_df['entity'] == selected_entity]
        display_title = selected_entity
    
    st.markdown(f"<h4 style='text-align: center;'>{display_title} - Partnership Network</h4>", unsafe_allow_html=True)

    # Debug: Uncomment to verify data is loading correctly
    # st.info(f"DEBUG: Total partnerships loaded: {len(partnership_df)}, Filtered: {len(filtered_df)}")
    # if 'partner_type' in filtered_df.columns:
    #     st.write("Partner Type Counts:", filtered_df['partner_type'].value_counts().to_dict())

    # Summary Metrics - Calculate values
    total_partnerships = len(filtered_df)

    unique_types = "N/A"
    if 'partner_type' in filtered_df.columns:
        unique_types = filtered_df['partner_type'].nunique()

    high_conf = "N/A"
    if 'confidence_score' in filtered_df.columns:
        filtered_df['conf_pct'] = filtered_df['confidence_score'].str.rstrip('%').astype(float)
        high_conf = len(filtered_df[filtered_df['conf_pct'] >= 90])

    unique_partners = "N/A"
    if 'partner_name' in filtered_df.columns:
        unique_partners = filtered_df['partner_name'].nunique()

    # Display metrics with custom HTML
    st.markdown(f"""
        <div style='display: flex; justify-content: space-around; text-align: center; padding: 20px 0; border-top: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;'>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Total Partnerships</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{total_partnerships}</div>
            </div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Partner Types</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{unique_types}</div>
            </div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>High Confidence (≥90%)</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{high_conf}</div>
            </div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Unique Partners</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{unique_partners}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    
    # Partnership Directory
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: left;'>Partnership Directory</h4>", unsafe_allow_html=True)
    
    if selected_entity == "All Entities":
        display_cols = [col for col in ['entity', 'partner_type', 'partner_name', 'relationship_description', 'confidence_score'] 
                       if col in filtered_df.columns]
    else:
        display_cols = [col for col in ['partner_type', 'partner_name', 'relationship_description', 'confidence_score'] 
                       if col in filtered_df.columns]
    
    display_df = filtered_df[display_cols].copy() if display_cols else filtered_df.copy()
    
    # Sort by confidence score if available
    if 'conf_pct' in filtered_df.columns:
        sorted_indices = filtered_df['conf_pct'].sort_values(ascending=False).index
        display_df = display_df.loc[sorted_indices]
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Visualization 1: Partnerships by Type - Packed Bubble Chart
    if 'partner_type' in filtered_df.columns and len(filtered_df) > 0:
        st.markdown("<h4 style='text-align: center;'>Partnerships by Type</h4>", unsafe_allow_html=True)

        type_counts = filtered_df['partner_type'].value_counts().reset_index()
        type_counts.columns = ['Partner Type', 'Count']

        # Calculate percentage
        total = type_counts['Count'].sum()
        type_counts['Percentage'] = (type_counts['Count'] / total * 100).round(1)

        # Assign unique colors to each partner type
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
                  '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739']
        type_counts['Color'] = [colors[i % len(colors)] for i in range(len(type_counts))]

        # Create a packed treemap
        fig = px.treemap(
            type_counts,
            path=['Partner Type'],
            values='Count',
            color='Partner Type',
            color_discrete_sequence=colors,
            custom_data=['Count', 'Percentage']
        )

        fig.update_traces(
            textposition='middle center',
            texttemplate='<b>%{label}</b><br>%{customdata[0]}',
            textfont=dict(size=13, color='white', family='Arial'),
            marker=dict(
                line=dict(color='white', width=4),
                cornerradius=15
            ),
            hovertemplate='<b>%{label}</b><br>Count: %{customdata[0]}<br>Percentage: %{customdata[1]:.1f}%<extra></extra>'
        )

        fig.update_layout(
            height=500,
            margin=dict(l=10, r=10, t=40, b=10),
            font=dict(family="Arial, sans-serif"),
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No partnership type data to display")

    st.markdown("---")

    # Visualization 2: Partnership Treemap by Entity
    if 'entity' in filtered_df.columns and 'partner_type' in filtered_df.columns and len(filtered_df) > 0:
        st.markdown("<h4 style='text-align: center;'>Partnerships by Entity</h4>", unsafe_allow_html=True)

        # Create hierarchy: entity -> partner_type -> partner_name
        treemap_data = filtered_df.copy()

        # Add hover information
        if 'relationship_description' in treemap_data.columns:
            treemap_data['hover_text'] = treemap_data.apply(
                lambda row: f"<b>{row.get('partner_name', 'Unknown')}</b><br>Type: {row.get('partner_type', 'Unknown')}<br>Entity: {row.get('entity', 'Unknown')}<br>Relationship: {row.get('relationship_description', 'N/A')}",
                axis=1
            )
        else:
            treemap_data['hover_text'] = treemap_data.apply(
                lambda row: f"<b>{row.get('partner_name', 'Unknown')}</b><br>Type: {row.get('partner_type', 'Unknown')}<br>Entity: {row.get('entity', 'Unknown')}",
                axis=1
            )

        # Create treemap chart
        fig = px.treemap(
            treemap_data,
            path=['entity', 'partner_type', 'partner_name'],
            color='partner_type',
            color_discrete_sequence=px.colors.qualitative.Set3,
            custom_data=['hover_text']
        )

        fig.update_traces(
            textposition='middle center',
            hovertemplate='%{customdata[0]}<extra></extra>',
            marker=dict(line=dict(width=2, color='white'))
        )

        fig.update_layout(
            height=600,
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No partnership hierarchy data to display")


# ============================================================================
# VENDOR ECOSYSTEM
# ============================================================================

def render_vendor_ecosystem(vendor_df):
    """Render vendor ecosystem with entity filtering"""
    
    if len(vendor_df) == 0:
        st.warning("Vendor ecosystem data not found")
        render_generic_vendor_structure()
        return
    
    # Standardize entity names
    vendor_df = standardize_entity_names(vendor_df)
    
    # Entity filter
    entities = ["All Entities"] + sorted(vendor_df['entity'].unique().tolist())
    selected_entity = st.selectbox(
        "Filter by Entity:",
        entities,
        key="vendor_entity_filter"
    )
    
    # Filter data
    if selected_entity == "All Entities":
        filtered_df = vendor_df
        display_title = "All Entities"
    else:
        filtered_df = vendor_df[vendor_df['entity'] == selected_entity]
        display_title = selected_entity
    
    st.markdown(f"<h4 style='text-align: center;'>{display_title}</h4>", unsafe_allow_html=True)

    # Summary Metrics - Calculate values
    total_vendors = len(filtered_df)

    unique_sectors = "N/A"
    if 'sector' in filtered_df.columns:
        unique_sectors = filtered_df['sector'].nunique()

    high_conf = "N/A"
    if 'confidence_score' in filtered_df.columns:
        filtered_df['conf_pct'] = filtered_df['confidence_score'].str.rstrip('%').astype(float)
        high_conf = len(filtered_df[filtered_df['conf_pct'] >= 90])

    unique_rels = "N/A"
    if 'relationship' in filtered_df.columns:
        unique_rels = filtered_df['relationship'].nunique()

    # Display metrics with custom HTML
    st.markdown(f"""
        <div style='display: flex; justify-content: space-around; text-align: center; padding: 20px 0; border-top: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;'>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Total Vendors</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{total_vendors}</div>
            </div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Sectors</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{unique_sectors}</div>
            </div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>High Confidence (≥90%)</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{high_conf}</div>
            </div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Relationship Types</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{unique_rels}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    
    # Vendor Directory
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: left;'>Vendor Directory</h4>", unsafe_allow_html=True)
    
    if selected_entity == "All Entities":
        display_cols = [col for col in ['entity', 'sector', 'vendor', 'relationship', 'confidence_score'] 
                       if col in filtered_df.columns]
    else:
        display_cols = [col for col in ['sector', 'vendor', 'relationship', 'confidence_score'] 
                       if col in filtered_df.columns]
    
    display_df = filtered_df[display_cols].copy() if display_cols else filtered_df.copy()
    
    # Sort by confidence
    if 'conf_pct' in filtered_df.columns:
        sorted_indices = filtered_df['conf_pct'].sort_values(ascending=False).index
        display_df = display_df.loc[sorted_indices]
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=300
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Visualization: Vendor Ecosystem by Sector - Treemap (Full Width)
    if 'sector' in filtered_df.columns and 'vendor' in filtered_df.columns and len(filtered_df) > 0:
        st.markdown("<h4 style='text-align: center;'>Vendor Ecosystem by Sector</h4>", unsafe_allow_html=True)

        vendor_treemap_data = filtered_df.copy()

        # Vibrant color palette for sectors
        sector_colors = ['#FF6B6B', '#4ECDC4', '#AFA9DC', '#FFA07A', '#9DD8AD',
                        '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#E74C3C']

        fig = px.treemap(
            vendor_treemap_data,
            path=['sector', 'vendor'],
            color='sector',
            color_discrete_sequence=sector_colors
        )

        fig.update_traces(
            textposition='middle center',
            textfont=dict(size=13, color='black', family='Arial'),
            marker=dict(
                line=dict(color='white', width=4),
            ),
            hovertemplate='<b>%{label}</b><extra></extra>'
        )

        fig.update_layout(
            height=500,
            margin=dict(l=0, r=0, t=20, b=0)
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("---")
        
    # Vendor Tier Structure (expandable for context)
    render_vendor_tier_context(filtered_df, selected_entity)


def render_vendor_tier_context(vendor_df, selected_entity):
    """Render contextual vendor tier information"""
    
    with st.expander("Vendor Ecosystem Tiers"):
        
        if len(vendor_df) > 0 and 'vendor' in vendor_df.columns:
            # Categorize vendors from data
            tier1_data = []
            tier2_data = []

            global_giants = ['Microsoft', 'Google', 'AWS', 'Amazon', 'Huawei', 'Nvidia', 'Oracle', 'IBM', 'SAP']

            for _, row in vendor_df.iterrows():
                vendor_name = str(row['vendor'])
                entity = row.get('entity', 'Unknown')
                sector = row.get('sector', 'Unknown')

                # Check tier classification
                if any(giant in vendor_name for giant in global_giants):
                    tier1_data.append({
                        'Vendor': vendor_name,
                        'Entity': entity,
                        'Sector': sector
                    })
                else:
                    tier2_data.append({
                        'Vendor': vendor_name,
                        'Entity': entity,
                        'Sector': sector
                    })

            # Display as tables
            col1, col2 = st.columns(2)

            with col1:
                st.markdown('<h5 style="text-align: center;">Tier 1: Global Giants</h5>', unsafe_allow_html=True)

                if tier1_data:
                    tier1_df = pd.DataFrame(tier1_data)
                    st.dataframe(
                        tier1_df,
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("None in current view")

            with col2:
                st.markdown('<h5 style="text-align: center;">Tier 2: Specialized</h5>', unsafe_allow_html=True)

                if tier2_data:
                    tier2_df = pd.DataFrame(tier2_data)
                    st.dataframe(
                        tier2_df,
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("None in current view")
        
def standardize_entity_names(df):
    """Standardize entity names to match nodes.csv format"""
    if 'entity' not in df.columns:
        return df
    
    # Mapping from various formats to standardized names
    entity_mapping = {
        'MyDIGITAL': 'MyDIGITAL Corp',
        'Ministry of Digital': 'MOD',
        'MOHE': 'MOHE',
        'MDEC': 'MDEC',
        'MCMC': 'MCMC'
    }
    
    df['entity'] = df['entity'].map(entity_mapping).fillna(df['entity'])
    return df
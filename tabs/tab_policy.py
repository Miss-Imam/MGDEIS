"""
TAB 4: Policy & Strategy
National Policies, Cross-Entity Matrix, and AI Alignment
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx


def render_policy_tab(entities_df, people_df, partners_df, has_csv_data, research_data):
    """Render Policy & Strategy with 3 subtabs and entity filtering"""

    st.markdown('<h4 style="text-align: center;">Policy frameworks, alignments, and strategic fits</h4>', unsafe_allow_html=True)
    st.markdown("---")

    # Load datasets directly from CSV
    def load_csv(path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(path, dtype=str, encoding="utf-8", engine="python")
        except Exception:
            return pd.DataFrame()

    policy_align_df = load_csv("data/entity_policy_alignment.csv")
    ai_alignment_df = load_csv("data/ai_alignment.csv")

    # Create subtabs
    policy_subtabs = st.tabs([
        "National Policies",
        "Cross-Entity Policy Matrix",
        "AI Alignment"
    ])


# ============================================================================
# National Policies
# ============================================================================

    with policy_subtabs[0]:
        render_national_policies(policy_align_df)

    # SUBTAB 2: Cross-Entity Policy Matrix
    with policy_subtabs[1]:
        render_cross_entity_matrix(policy_align_df)

    # SUBTAB 3: AI Alignment
    with policy_subtabs[2]:
        render_ai_alignment(ai_alignment_df)


def standardize_entity_names(df):
    """Standardize entity names across datasets"""
    if 'entity' in df.columns:
        df = df.copy()
        df['entity'] = df['entity'].replace({
            'MyDIGITAL Corporation': 'MyDIGITAL',
            'Ministry of Digital': 'MOD',
            'Malaysian Communications and Multimedia Commission': 'MCMC',
            'Malaysia Digital Economy Corporation': 'MDEC',
            'Ministry of Higher Education': 'MOHE'
        })
    return df


def render_national_policies(policy_df):
    """Render national policy alignment dashboard with entity filtering"""

    if policy_df.empty:
        st.warning("No policy alignment data found")
        return

    # Standardize entity names
    policy_df = standardize_entity_names(policy_df)

    # Entity filter
    entities = ["All Entities"] + sorted(policy_df['entity'].unique().tolist())
    selected_entity = st.selectbox(
        "Filter by Entity:",
        entities,
        key="policy_entity_filter"
    )

    # Filter data
    if selected_entity == "All Entities":
        filtered_df = policy_df
        display_title = "All Entities"
    else:
        filtered_df = policy_df[policy_df['entity'] == selected_entity]
        display_title = selected_entity

    st.markdown(f"<h4 style='text-align: center;'>{display_title}</h4>", unsafe_allow_html=True)

    # Summary Metrics - Full Width with custom styling
    # Calculate metrics
    total_policies = len(filtered_df)
    active_policies = len(filtered_df[filtered_df['status'].str.contains('Active', na=False)])
    in_dev_policies = len(filtered_df[filtered_df['status'].str.contains('Development', na=False)])

    avg_confidence = 0
    if 'confidence_score' in filtered_df.columns:
        avg_confidence = pd.to_numeric(
            filtered_df['confidence_score'].astype(str).str.replace('%', ''),
            errors='coerce'
        ).mean()

    # Display metrics with custom HTML
    st.markdown(f"""
        <div style='display: flex; justify-content: space-around; text-align: center; padding: 20px 0; border-top: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;'>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Total Policies</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{total_policies}</div>
            </div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Active Policies</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{active_policies}</div>
            </div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>In Development</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{in_dev_policies}</div>
            </div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Avg Confidence</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{avg_confidence:.1f}%</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    
    # Key Policies Table
    st.markdown("<h4 style='text-align: left;'>Policy Details</h4>", unsafe_allow_html=True)

    display_cols = [col for col in ['entity', 'policy_name', 'launch_date', 'status',
                                     'alignment_description', 'confidence_score', 'source']
                    if col in filtered_df.columns]

    display_df = filtered_df[display_cols].copy() if display_cols else filtered_df.copy()

    # Sort by confidence score if available
    if 'confidence_score' in filtered_df.columns:
        filtered_df['conf_numeric'] = pd.to_numeric(
            filtered_df['confidence_score'].astype(str).str.replace('%', ''),
            errors='coerce'
        )
        sorted_indices = filtered_df['conf_numeric'].sort_values(ascending=False).index
        display_df = display_df.loc[sorted_indices]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=400
    )

    st.markdown("---")

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        # Policy Status Distribution - Horizontal Bar Chart
        if 'status' in filtered_df.columns and len(filtered_df) > 0:
            st.markdown("<h4 style='text-align: center;'>Policy Status Distribution</h4>", unsafe_allow_html=True)

            # Get status counts directly from the column
            status_counts = filtered_df['status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']

            # Ensure counts are integers
            status_counts['Count'] = status_counts['Count'].astype(int)

            # Sort by count ascending for better display (smallest at bottom)
            status_counts = status_counts.sort_values('Count', ascending=True)

            colors = {'Active': '#4caf50', 'In Development': '#ff9800', 'Completed': '#2196f3'}
            color_list = [colors.get(status, '#9e9e9e') for status in status_counts['Status']]

            fig = go.Figure(data=[go.Bar(
                x=status_counts['Count'].tolist(),
                y=status_counts['Status'].tolist(),
                orientation='h',
                marker_color=color_list,
                text=status_counts['Count'].tolist(),
                textposition='outside',
                textfont=dict(size=14)
            )])

            fig.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=40, b=40),
                xaxis_title='Number of Policies',
                yaxis_title='',
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    gridcolor='#e0e0e0',
                    range=[0, max(status_counts['Count']) * 1.15]
                )
            )

            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        # Policy Launch Timeline - Vertical Bar Chart
        if 'launch_date' in filtered_df.columns and len(filtered_df) > 0:
            st.markdown("<h4 style='text-align: center;'>Policy Launch Timeline</h4>", unsafe_allow_html=True)

            # Create a copy to avoid SettingWithCopyWarning
            timeline_df = filtered_df.copy()

            # Extract year from launch_date
            timeline_df['launch_year'] = timeline_df['launch_date'].astype(str).str.extract(r'(\d{4})')[0]

            # Remove NaN values and convert to int
            timeline_df = timeline_df[timeline_df['launch_year'].notna()].copy()
            if len(timeline_df) > 0:
                timeline_df['launch_year'] = timeline_df['launch_year'].astype(int)

                # Count policies per year
                year_counts = timeline_df['launch_year'].value_counts().sort_index().reset_index()
                year_counts.columns = ['Year', 'Count']

                # Ensure counts are integers
                year_counts['Count'] = year_counts['Count'].astype(int)

                fig = go.Figure(data=[go.Bar(
                    x=year_counts['Year'].tolist(),
                    y=year_counts['Count'].tolist(),
                    marker_color='#2196f3',
                    text=year_counts['Count'].tolist(),
                    textposition='outside',
                    textfont=dict(size=14)
                )])

                fig.update_layout(
                    height=350,
                    margin=dict(l=20, r=20, t=40, b=40),
                    xaxis_title='Year',
                    yaxis_title='Number of Policies',
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(
                        gridcolor='#e0e0e0',
                        type='category'
                    ),
                    yaxis=dict(
                        gridcolor='#e0e0e0',
                        range=[0, max(year_counts['Count']) * 1.15]
                    )
                )

                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ============================================================================
# Cross-Entity Policy Matrix
# ============================================================================

def render_cross_entity_matrix(policy_df):
    """Render cross-entity policy framework matrix with network visualization"""

    if policy_df.empty:
        st.warning("No policy alignment data found")
        return

    # Standardize entity names
    policy_df = standardize_entity_names(policy_df)

    st.markdown("<h4 style='text-align: left;'>Cross-Entity Policy Matrix</h4>", unsafe_allow_html=True)

    # Ownership Matrix Table
    # Create collaboration matrix showing which policies are shared
    if 'policy_name' in policy_df.columns and 'entity' in policy_df.columns:
        # Group by policy to find shared policies
        policy_groups = policy_df.groupby('policy_name')['entity'].apply(list).reset_index()
        policy_groups['entity_count'] = policy_groups['entity'].apply(len)
        policy_groups['entities_involved'] = policy_groups['entity'].apply(lambda x: ', '.join(x))

        # Convert confidence_score to numeric for aggregation
        policy_df_copy = policy_df.copy()
        if 'confidence_score' in policy_df_copy.columns:
            policy_df_copy['confidence_score'] = pd.to_numeric(
                policy_df_copy['confidence_score'].astype(str).str.replace('%', ''),
                errors='coerce'
            )

        # Get additional details for each policy
        policy_details = policy_df_copy.groupby('policy_name').agg({
            'status': 'first',
            'launch_date': 'first',
            'confidence_score': 'mean'
        }).reset_index()

        # Merge
        matrix_df = policy_groups.merge(policy_details, on='policy_name', how='left')
        matrix_df = matrix_df[['policy_name', 'entity_count', 'entities_involved', 'status', 'launch_date', 'confidence_score']]
        matrix_df.columns = ['Policy/Framework', 'Entities Involved', 'Entity Names', 'Status', 'Launch Date', 'Avg Confidence']

        # Format confidence
        if 'Avg Confidence' in matrix_df.columns:
            matrix_df['Avg Confidence'] = matrix_df['Avg Confidence'].apply(
                lambda x: f"{float(str(x).replace('%', '')):.1f}%" if pd.notna(x) else "N/A"
            )

        # Sort by entity count descending (most collaborative first)
        matrix_df = matrix_df.sort_values('Entities Involved', ascending=False)

        st.dataframe(matrix_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Network Graph Visualization
    st.markdown("<h4 style='text-align: center;'>Policy Collaboration Network</h4>", unsafe_allow_html=True)

    if 'policy_name' in policy_df.columns and 'entity' in policy_df.columns and len(policy_df) > 0:
        try:
            import networkx as nx

            # Create network graph
            G = nx.Graph()

            # Add all entities as nodes
            all_entities = policy_df['entity'].unique()
            for entity in all_entities:
                G.add_node(entity, node_type='entity')

            # Group by policy to find collaborations
            policy_groups = policy_df.groupby('policy_name')['entity'].apply(list).to_dict()

            # Count shared policies between entities
            collaboration_counts = {}
            shared_policies = {}

            for policy, entities in policy_groups.items():
                if len(entities) > 1:
                    # Create pairs of collaborating entities
                    for i in range(len(entities)):
                        for j in range(i + 1, len(entities)):
                            entity1, entity2 = sorted([entities[i], entities[j]])
                            pair = (entity1, entity2)

                            if pair not in collaboration_counts:
                                collaboration_counts[pair] = 0
                                shared_policies[pair] = []

                            collaboration_counts[pair] += 1
                            shared_policies[pair].append(policy)

            # Add edges for collaborations
            for (entity1, entity2), count in collaboration_counts.items():
                G.add_edge(entity1, entity2, weight=count, policies=shared_policies[(entity1, entity2)])

            if len(G.edges()) > 0:
                # Get positions using spring layout
                pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

                # Create edge traces
                edge_traces = []
                for edge in G.edges(data=True):
                    x0, y0 = pos[edge[0]]
                    x1, y1 = pos[edge[1]]
                    weight = edge[2]['weight']
                    policies = edge[2]['policies']

                    # Line width based on number of shared policies
                    line_width = 2 + (weight * 3)

                    edge_trace = go.Scatter(
                        x=[x0, x1, None],
                        y=[y0, y1, None],
                        mode='lines',
                        line=dict(width=line_width, color='#94A3B8'),
                        hovertemplate=f'{edge[0]} ↔ {edge[1]}<br>{weight} shared policies<br>' + '<br>'.join(policies[:3]) + '<extra></extra>',
                        showlegend=False
                    )
                    edge_traces.append(edge_trace)

                # Create node trace
                node_x = []
                node_y = []
                node_text = []
                node_colors = []
                node_sizes = []

                # Color palette for entities
                entity_colors = {
                    'MOHE': '#8B5CF6',
                    'MyDIGITAL': '#EC4899',
                    'MDEC': '#F59E0B',
                    'MOD': '#10B981',
                    'Ministry of Digital': '#10B981',
                    'MCMC': '#3B82F6'
                }

                for node in G.nodes():
                    x, y = pos[node]
                    node_x.append(x)
                    node_y.append(y)

                    # Count connections
                    num_connections = G.degree(node)
                    node_text.append(f'{node}<br>{num_connections} collaboration(s)')

                    # Color by entity
                    node_colors.append(entity_colors.get(node, '#6B7280'))

                    # Size based on number of policies
                    node_policies = len(policy_df[policy_df['entity'] == node])
                    node_sizes.append(20 + (node_policies * 5))

                node_trace = go.Scatter(
                    x=node_x,
                    y=node_y,
                    mode='markers+text',
                    marker=dict(
                        size=node_sizes,
                        color=node_colors,
                        line=dict(width=2, color='white')
                    ),
                    text=[node for node in G.nodes()],
                    textposition='top center',
                    textfont=dict(size=12, color='#1F2937'),
                    hovertext=node_text,
                    hoverinfo='text',
                    showlegend=False
                )

                # Create figure
                fig = go.Figure(data=edge_traces + [node_trace])

                fig.update_layout(
                    height=400,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=0, l=0, r=0, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )

                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

                # Collaboration insights - horizontal layout
                total_entities = len(all_entities)
                collaborative_policies = sum(1 for policies in policy_groups.values() if len(policies) > 1)
                total_connections = len(collaboration_counts)
                most_collab_pair = max(collaboration_counts.items(), key=lambda x: x[1])[0] if collaboration_counts else 'N/A'

                st.markdown(f"""
                <div style='text-align: center;'>
                <strong>Network Insights:</strong> Total Entities: {total_entities} ⎮ Collaborative Policies: {collaborative_policies} ⎮ Total Connections: {total_connections} ⎮ Most Collaborative Pair: {most_collab_pair}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("No policy collaborations found between entities")

        except Exception as e:
            st.error(f"Error creating network visualization: {e}")
            st.info("Network visualization requires shared policies between entities")


# ============================================================================
# AI Alignment
# ============================================================================

def render_ai_alignment(ai_df):
    """Render AI alignment analysis with entity filtering"""

    if ai_df.empty:
        st.warning("No AI alignment data found")
        return

    # Standardize entity names
    ai_df = standardize_entity_names(ai_df)

    # Entity filter
    entities = ["All Entities"] + sorted(ai_df['entity'].unique().tolist())
    selected_entity = st.selectbox(
        "Filter by Entity:",
        entities,
        key="ai_entity_filter"
    )

    # Filter data
    if selected_entity == "All Entities":
        filtered_df = ai_df
        display_title = "All Entities"
    else:
        filtered_df = ai_df[ai_df['entity'] == selected_entity]
        display_title = selected_entity

    st.markdown(f"<h4 style='text-align: center;'>{display_title}</h4>", unsafe_allow_html=True)

    # Summary Metrics - Full Width with custom styling
    # Calculate metrics
    total_initiatives = len(filtered_df)

    policy_count = 0
    agency_count = 0
    if 'type' in filtered_df.columns:
        policy_count = len(filtered_df[filtered_df['type'] == 'Policy'])
        agency_count = len(filtered_df[filtered_df['type'] == 'Agency'])

    avg_confidence = 0
    if 'confidence_score' in filtered_df.columns:
        avg_confidence = pd.to_numeric(
            filtered_df['confidence_score'].astype(str).str.replace('%', ''),
            errors='coerce'
        ).mean()

    # Display metrics with custom HTML
    st.markdown(f"""
        <div style='display: flex; justify-content: space-around; text-align: center; padding: 20px 0; border-top: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;'>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>AI Alignments</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{total_initiatives}</div>
            </div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Policies</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{policy_count}</div>
            </div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Agencies</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{agency_count}</div>
            </div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Avg Confidence</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{avg_confidence:.1f}%</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    
    # AI Alignment Table
    st.markdown("<h4 style='text-align: left;'>AI Alignment Details</h4>", unsafe_allow_html=True)

    display_cols = [col for col in ['entity', 'focus_area', 'type', 'ai_alignment',
                                     'confidence_score', 'source']
                    if col in filtered_df.columns]

    display_df = filtered_df[display_cols].copy() if display_cols else filtered_df.copy()

    # Sort by confidence score
    if 'confidence_score' in filtered_df.columns:
        filtered_df['conf_numeric'] = pd.to_numeric(
            filtered_df['confidence_score'].astype(str).str.replace('%', ''),
            errors='coerce'
        )
        sorted_indices = filtered_df['conf_numeric'].sort_values(ascending=False).index
        display_df = display_df.loc[sorted_indices]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=400
    )

    st.markdown("---")

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        # AI Alignment Types - Vertical Bar Chart
        if 'type' in filtered_df.columns and len(filtered_df) > 0:
            st.markdown("<h4 style='text-align: center;'>AI Alignment Types</h4>", unsafe_allow_html=True)

            type_counts = filtered_df['type'].value_counts().reset_index()
            type_counts.columns = ['Type', 'Count']

            # Ensure counts are integers
            type_counts['Count'] = type_counts['Count'].astype(int)
            type_counts = type_counts.sort_values('Count', ascending=False)

            colors = ['#8B5CF6', '#EC4899', '#F59E0B', '#10B981', '#3B82F6', '#F97316']

            fig = go.Figure(data=[go.Bar(
                x=type_counts['Type'].tolist(),
                y=type_counts['Count'].tolist(),
                marker_color=colors[:len(type_counts)],
                text=type_counts['Count'].tolist(),
                textposition='outside',
                textfont=dict(size=14)
            )])

            fig.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=40, b=40),
                xaxis_title='Type',
                yaxis_title='Number of Alignments',
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(
                    gridcolor='#e0e0e0',
                    range=[0, max(type_counts['Count']) * 1.15]
                )
            )

            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        # AI Alignment by Entity (if showing all)
        if selected_entity == "All Entities" and 'entity' in filtered_df.columns and len(filtered_df) > 0:
            st.markdown("<h4 style='text-align: center;'>AI Alignment by Entity</h4>", unsafe_allow_html=True)

            entity_counts = filtered_df['entity'].value_counts().reset_index()
            entity_counts.columns = ['Entity', 'Count']

            # Ensure counts are integers
            entity_counts['Count'] = entity_counts['Count'].astype(int)
            entity_counts = entity_counts.sort_values('Count', ascending=True)

            # Use gradient colors for entities
            entity_colors = ['#90CAF9', '#64B5F6', '#42A5F5', '#2196F3', '#1E88E5']

            fig = go.Figure(data=[go.Bar(
                x=entity_counts['Count'].tolist(),
                y=entity_counts['Entity'].tolist(),
                orientation='h',
                marker_color=entity_colors[:len(entity_counts)],
                text=entity_counts['Count'].tolist(),
                textposition='outside',
                textfont=dict(size=14)
            )])

            fig.update_layout(
                height=350,
                showlegend=False,
                xaxis_title="Number of Alignments",
                yaxis_title="",
                margin=dict(l=20, r=20, t=40, b=40),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    gridcolor='#e0e0e0',
                    range=[0, max(entity_counts['Count']) * 1.15]
                )
            )

            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

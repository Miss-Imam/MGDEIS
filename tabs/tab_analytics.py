"""
TAB 5: Analytics
Procurement Analysis and Knowledge Graph
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from neo4j_connector import Neo4jConnector


def render_analytics_tab(entities_df, people_df, partners_df, has_csv_data, research_data):
    """Render Analytics with 2 subtabs"""

    st.markdown('<h4 style="text-align: center;">Procurement Insights and Network Graph</h4>', unsafe_allow_html=True)
    st.markdown("---")

    # Load procurement data directly from CSV
    def load_csv(path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(path, dtype=str, encoding="utf-8", engine="python")
        except Exception:
            return pd.DataFrame()

    procurement_df = load_csv("data/procurement_analysis.csv")

    # Create subtabs
    ops_subtabs = st.tabs([
        "Procurement Analysis",
        "Knowledge Graph"
    ])

# ============================================================================
# Procurement Analysis
# ============================================================================

    with ops_subtabs[0]:
        render_procurement_analysis(procurement_df)

    # SUBTAB 2: Knowledge Graph
    with ops_subtabs[1]:
        render_knowledge_graph()


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


def render_procurement_analysis(procurement_df):
    """Render procurement analysis with entity filtering"""

    if procurement_df.empty:
        st.warning("No procurement data found")
        return

    # Standardize entity names
    procurement_df = standardize_entity_names(procurement_df)

    # Entity filter
    entities = ["All Entities"] + sorted(procurement_df['entity'].unique().tolist())
    selected_entity = st.selectbox(
        "Filter by Entity:",
        entities,
        key="procurement_entity_filter"
    )

    # Filter data
    if selected_entity == "All Entities":
        filtered_df = procurement_df
        display_title = "All Entities"
    else:
        filtered_df = procurement_df[procurement_df['entity'] == selected_entity]
        display_title = f"{selected_entity}"

    st.markdown(f"<h4 style='text-align: center;'>{display_title}</h4>", unsafe_allow_html=True)

    # Summary Metrics 
    # Calculate metrics
    total_items = len(filtered_df)

    categories = 0
    if 'procurement_category' in filtered_df.columns:
        categories = filtered_df['procurement_category'].nunique()

    active_contracts = 0
    if 'status' in filtered_df.columns:
        active_contracts = len(filtered_df[filtered_df['status'].str.contains('ACTIVE', case=False, na=False)])

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
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Total Contracts</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{total_items}</div>
            </div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Categories</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{categories}</div>
            </div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Active Contracts</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{active_contracts}</div>
            </div>
            <div style='flex: 1;'>
                <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Avg Confidence</div>
                <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{avg_confidence:.1f}%</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    
    # Directory Table
    st.markdown("<h4 style='text-align: left;'>Procurement Directory</h4>", unsafe_allow_html=True)

    display_cols = [col for col in ['entity', 'procurement_category', 'known_vendors', 'estimated_value', 'status']
                   if col in filtered_df.columns]

    display_df = filtered_df[display_cols].copy() if display_cols else filtered_df.copy()

    # Rename columns for better display
    column_rename = {
        'entity': 'Entity',
        'procurement_category': 'Category',
        'known_vendors': 'Known Vendors',
        'estimated_value': 'Value',
        'status': 'Status'
    }
    display_df = display_df.rename(columns={k: v for k, v in column_rename.items() if k in display_df.columns})

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
        # Procurement by Category - Horizontal Bar Chart
        if 'procurement_category' in filtered_df.columns and len(filtered_df) > 0:
            st.markdown("<h4 style='text-align: center;'>Procurement by Category</h4>", unsafe_allow_html=True)

            category_counts = filtered_df['procurement_category'].value_counts().reset_index()
            category_counts.columns = ['Category', 'Count']
            category_counts['Count'] = category_counts['Count'].astype(int)
            category_counts = category_counts.sort_values('Count', ascending=True)

            fig = go.Figure(data=[go.Bar(
                x=category_counts['Count'].tolist(),
                y=category_counts['Category'].tolist(),
                orientation='h',
                marker_color='#2196f3',
                text=category_counts['Count'].tolist(),
                textposition='outside',
                textfont=dict(size=14)
            )])

            fig.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=40, b=40),
                xaxis_title='Number of Procurements',
                yaxis_title='',
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    gridcolor='#e0e0e0',
                    range=[0, max(category_counts['Count']) * 1.15]
                ),
                yaxis=dict(
                    tickfont=dict(size=10)
                )
            )

            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        # Procurement by Entity (if showing all entities)
        if selected_entity == "All Entities" and 'entity' in filtered_df.columns and len(filtered_df) > 0:
            st.markdown("<h4 style='text-align: center;'>Procurement by Entity</h4>", unsafe_allow_html=True)

            entity_counts = filtered_df['entity'].value_counts().reset_index()
            entity_counts.columns = ['Entity', 'Count']
            entity_counts['Count'] = entity_counts['Count'].astype(int)
            entity_counts = entity_counts.sort_values('Count', ascending=False)

            colors = ['#8B5CF6', '#EC4899', '#F59E0B', '#10B981', '#3B82F6']

            fig = go.Figure(data=[go.Bar(
                x=entity_counts['Entity'].tolist(),
                y=entity_counts['Count'].tolist(),
                marker_color=colors[:len(entity_counts)],
                text=entity_counts['Count'].tolist(),
                textposition='outside',
                textfont=dict(size=14)
            )])

            fig.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=40, b=40),
                xaxis_title='Entity',
                yaxis_title='Number of Procurements',
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(
                    gridcolor='#e0e0e0',
                    range=[0, max(entity_counts['Count']) * 1.15]
                )
            )

            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ============================================================================
# Knowledge Graph
# ============================================================================

def render_knowledge_graph():
    """Render Interactive Knowledge Graph from Neo4j Aura with advanced features"""

    st.markdown("<h4 style='text-align: center;'>Knowledge Graph Network</h4>", unsafe_allow_html=True)

    try:
        connector = Neo4jConnector()

        # Filters Section
        st.markdown("### Filters")
        filter_cols = st.columns(8)

        with filter_cols[0]:
            filter_entity = st.checkbox("Entity", value=True)
        with filter_cols[1]:
            filter_department = st.checkbox("Department", value=True)
        with filter_cols[2]:
            filter_agency = st.checkbox("Agency", value=True)
        with filter_cols[3]:
            filter_company = st.checkbox("Company", value=True)
        with filter_cols[4]:
            filter_partner = st.checkbox("Partner", value=True)
        with filter_cols[5]:
            filter_initiative = st.checkbox("Initiative", value=True)
        with filter_cols[6]:
            filter_policy = st.checkbox("Policy", value=True)
        with filter_cols[7]:
            filter_people = st.checkbox("People", value=True)

        # Build filter query based on selections
        filter_labels = []
        if filter_entity: filter_labels.append("Entity")
        if filter_department: filter_labels.append("Department")
        if filter_agency: filter_labels.append("Agency")
        if filter_company: filter_labels.append("Company")
        if filter_partner: filter_labels.append("Partner")
        if filter_initiative: filter_labels.append("Initiative")
        if filter_policy: filter_labels.append("Policy")
        if filter_people: filter_labels.append("People")

        st.markdown("---")

        # Query Builder
        st.markdown("<h4 style='text-align: center;'>Query Builder</h4>", unsafe_allow_html=True)

        query_cols = st.columns([3, 1.5, 1.5, 1])

        with query_cols[0]:
            query_template = st.selectbox(
                "Query Template",
                [
                    "All Nodes (Limited)",
                    "People & Organizations",
                    "Partnerships",
                    "Policy Alignments",
                    "Hierarchical Structure",
                    "Custom Cypher"
                ]
            )

        with query_cols[1]:
            limit = st.number_input("Limit", min_value=10, max_value=500, value=150, step=10)

        with query_cols[2]:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Execute Query", use_container_width=True, type="primary"):
                st.rerun()

        with query_cols[3]:
            st.markdown("<br>", unsafe_allow_html=True)
            show_help = st.toggle("Help")

        # Generate Cypher query
        if query_template == "All Nodes (Limited)":
            label_filter = f":{':'.join(filter_labels)}" if filter_labels else ""
            cypher_query = f"MATCH (n{label_filter})-[r]->(m) RETURN n,r,m LIMIT {limit}"
        elif query_template == "People & Organizations":
            cypher_query = f"MATCH (p:Person)-[r]->(o:Organization) RETURN p,r,o LIMIT {limit}"
        elif query_template == "Partnerships":
            cypher_query = f"MATCH (c:Company)-[r:PARTNERS_WITH]->(o:Organization) RETURN c,r,o LIMIT {limit}"
        elif query_template == "Policy Alignments":
            cypher_query = f"MATCH (o:Organization)-[r:ALIGNED_WITH]->(p:Policy) RETURN o,r,p LIMIT {limit}"
        elif query_template == "Hierarchical Structure":
            cypher_query = f"MATCH (o:Organization)-[r:REPORTS_TO]->(m:Ministry) RETURN o,r,m LIMIT {limit}"
        else:
            cypher_query = st.text_area(
                "Custom Cypher Query",
                value="MATCH (n)-[r]->(m) RETURN n,r,m LIMIT 100",
                height=100
            )

        if show_help:
            st.info("""
            **Cypher Query Examples:**
            - `MATCH (n) RETURN n LIMIT 50` - Get all nodes
            - `MATCH (p:Person) RETURN p` - Get all people
            - `MATCH (n)-[r]->(m) RETURN n,r,m` - Get all relationships
            - `MATCH (n) WHERE n.name CONTAINS 'Digital' RETURN n` - Search by name
            - `MATCH (n:Entity)-[r]->(m:Policy) RETURN n,r,m` - Entities and policies
            """)

        st.markdown("---")

        # Retrieve graph data with filters applied
        import networkx as nx
        nodes, relationships = connector.get_full_graph_data(limit=limit, filter_labels=filter_labels if filter_labels else None)

        # Calculate statistics from actual retrieved data
        stats = {
            'total_nodes': len(nodes),
            'total_relationships': len(relationships),
            'node_types': {},
            'relationship_types': {},
            'most_connected': []
        }

        # Count node types from retrieved nodes
        for node in nodes:
            node_type = node.get('label', 'Unknown')
            stats['node_types'][node_type] = stats['node_types'].get(node_type, 0) + 1

        # Count relationship types from retrieved relationships
        for rel in relationships:
            rel_type = rel.get('relationship', 'Unknown')
            stats['relationship_types'][rel_type] = stats['relationship_types'].get(rel_type, 0) + 1

        # Calculate most connected nodes
        if nodes and relationships:
            G = nx.Graph()
            for node in nodes:
                G.add_node(node['id'], label=node['label'], name=node.get('name', 'Unknown'))
            for rel in relationships:
                G.add_edge(rel['source'], rel['target'])

            # Calculate degree (connections) for each node
            node_degrees = dict(G.degree())
            most_connected_list = []
            for node_id, degree in sorted(node_degrees.items(), key=lambda x: x[1], reverse=True)[:10]:
                if degree > 0:  # Only include connected nodes
                    node_data = next((n for n in nodes if n['id'] == node_id), None)
                    if node_data:
                        most_connected_list.append({
                            'name': node_data.get('name', 'Unknown'),
                            'type': node_data.get('label', 'Unknown'),
                            'connections': degree
                        })
            stats['most_connected'] = most_connected_list

        # Network Statistics - Horizontal layout
        st.markdown(f"""
            <div style='display: flex; justify-content: space-around; text-align: center; padding: 20px 0; border-top: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;'>
                <div style='flex: 1;'>
                    <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Total Nodes</div>
                    <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{stats['total_nodes']}</div>
                </div>
                <div style='flex: 1;'>
                    <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Total Relationships</div>
                    <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{stats['total_relationships']}</div>
                </div>
                <div style='flex: 1;'>
                    <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Node Types</div>
                    <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{len(stats['node_types'])}</div>
                </div>
                <div style='flex: 1;'>
                    <div style='font-weight: 700; font-size: 1rem; color: #333; margin-bottom: 8px;'>Relationship Types</div>
                    <div style='font-size: 1.2rem; font-weight: 400; color: #666;'>{len(stats['relationship_types'])}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Visualizations Row
        vis_col1, vis_col2 = st.columns(2)

        with vis_col1:
            st.markdown("<h4 style='text-align: center;'>Node Connections</h4>", unsafe_allow_html=True)
            if 'most_connected' in stats and stats['most_connected']:
                # Create horizontal bar chart for most connected nodes
                top_nodes = stats['most_connected'][:10]
                node_names = [f"{node['name'][:30]}..." if len(node['name']) > 30 else node['name'] for node in top_nodes]
                node_connections = [node['connections'] for node in top_nodes]

                fig = go.Figure(data=[go.Bar(
                    y=node_names[::-1],  # Reverse for top-to-bottom display
                    x=node_connections[::-1],
                    orientation='h',
                    marker_color='#4ECDC4',
                    text=node_connections[::-1],
                    textposition='outside'
                )])

                fig.update_layout(
                    height=400,
                    margin=dict(l=20, r=20, t=20, b=20),
                    xaxis_title='Connections',
                    yaxis_title='',
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(gridcolor='#e0e0e0')
                )

                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("No connection data available")

        with vis_col2:
            st.markdown("<h4 style='text-align: center;'>Node Type Distribution</h4>", unsafe_allow_html=True)
            if stats['node_types']:
                # Donut chart for node types with color mapping
                color_map = {
                    'People': '#FFE66D',
                    'Organization': '#4ECDC4',
                    'Ministry': '#FF9FF3',
                    'Entity': '#FF6B6B',
                    'Partner': '#95E1D3',
                    'Company': '#38B6FF',
                    'Policy': '#5F27CD',
                    'Department': '#00C9A7',
                    'Agency': '#FFB53D',
                    'Initiative': '#6BCF7F'
                }

                node_types = list(stats['node_types'].keys())
                node_counts = list(stats['node_types'].values())
                colors = [color_map.get(node_type, '#95E1D3') for node_type in node_types]

                fig = go.Figure(data=[go.Pie(
                    labels=node_types,
                    values=node_counts,
                    marker=dict(colors=colors, line=dict(color='white', width=2)),
                    textinfo='label+value+percent',
                    textposition='auto',
                    hole=0.3  
                )])

                fig.update_layout(
                    height=400,
                    margin=dict(l=20, r=20, t=20, b=20),
                    showlegend=True,
                    legend=dict(
                        orientation="v",
                        yanchor="middle",
                        y=0.5,
                        xanchor="left",
                        x=1.05
                    )
                )

                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown("---")

        # Interactive Graph Visualization
        st.markdown("<h4 style='text-align: center;'>Network Graph</h4>", unsafe_allow_html=True)

        # Reuse the graph G that was already created
        if nodes and relationships:
            # Re-create G with relationships for visualization (earlier G was just for degree calculation)
            G_viz = nx.Graph()
            for node in nodes:
                G_viz.add_node(node['id'], label=node['label'], name=node.get('name', 'Unknown'))
            for rel in relationships:
                G_viz.add_edge(rel['source'], rel['target'], relationship=rel['relationship'])

            # Remove disconnected nodes (isolates)
            isolates = list(nx.isolates(G_viz))
            G_viz.remove_nodes_from(isolates)

            # Only proceed if graph has nodes after removing isolates
            if len(G_viz.nodes()) == 0:
                st.info("No connected nodes found in the graph")
            else:
                # Create layout
                pos = nx.spring_layout(G_viz, k=0.5, iterations=50)

                # Create edge traces
                edge_traces = []
                for edge in G_viz.edges():
                    x0, y0 = pos[edge[0]]
                    x1, y1 = pos[edge[1]]

                    edge_trace = go.Scatter(
                        x=[x0, x1, None],
                        y=[y0, y1, None],
                        mode='lines',
                        line=dict(width=1, color='#888'),
                        hoverinfo='none',
                        showlegend=False
                    )
                    edge_traces.append(edge_trace)

                # Create node trace
                node_x = []
                node_y = []
                node_text = []
                node_colors = []

                color_map = {
                    'Person': '#FFE66D',
                    'Organization': '#4ECDC4',
                    'Ministry': '#FF9FF3',
                    'Entity': '#FF6B6B',
                    'Partner': '#95E1D3',
                    'Company': '#38B6FF',
                    'Policy': '#5F27CD',
                    'Department': '#EFAA7C',
                    'Agency': '#FFD93D',
                    'Initiative': '#6BCF7F'
                }

                for node in G_viz.nodes():
                    x, y = pos[node]
                    node_x.append(x)
                    node_y.append(y)
                    node_data = G_viz.nodes[node]
                    node_text.append(f"{node_data.get('name', 'Unknown')}<br>Type: {node_data.get('label', 'Unknown')}")
                    node_colors.append(color_map.get(node_data.get('label', ''), '#95E1D3'))

                node_trace = go.Scatter(
                    x=node_x,
                    y=node_y,
                    mode='markers+text',
                    marker=dict(
                        size=15,
                        color=node_colors,
                        line=dict(width=2, color='white')
                    ),
                    text=[G.nodes[node].get('name', '')[:15] for node in G.nodes()],
                    textposition='top center',
                    textfont=dict(size=8),
                    hovertext=node_text,
                    hoverinfo='text',
                    showlegend=False
                )

                # Create figure
                fig = go.Figure(data=edge_traces + [node_trace])

                fig.update_layout(
                    height=700,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=0, l=0, r=0, t=0),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    plot_bgcolor='#f8f9fa'
                )

                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})
        else:
            st.info("No graph data available for visualization")

        st.markdown("---")

        # Legend - Color-coded node types
        st.markdown("<h4 style='text-align: center;'>Legend: Node Types</h4>", unsafe_allow_html=True)

        color_map = {
            'Person': '#FFE66D',
            'Organization': '#4ECDC4',
            'Ministry': '#FF9FF3',
            'Entity': '#FF6B6B',
            'Partner': '#95E1D3',
            'Company': '#38B6FF',
            'Policy': '#5F27CD',
            'Department': '#EFAA7C',
            'Agency': '#FFD93D',
            'Initiative': '#6BCF7F'
        }

        # Create legend in a single row
        legend_items = list(stats['node_types'].items())
        num_items = len(legend_items)

        if num_items > 0:
            cols = st.columns(num_items)
            for col_idx, (node_type, count) in enumerate(legend_items):
                color = color_map.get(node_type, '#95E1D3')
                with cols[col_idx]:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 10px; background: white; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="width: 20px; height: 20px; border-radius: 50%; background: {color}; margin: 0 auto 5px; border: 2px solid white; box-shadow: 0 1px 2px rgba(0,0,0,0.2);"></div>
                        <div style="font-weight: 600; font-size: 0.85rem; margin-bottom: 2px;">{node_type}</div>
                        <div style="color: #666; font-size: 0.75rem;">({count})</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("---")

        # Export Options
        st.markdown("<h4 style='text-align: center;'>Export Options</h4>", unsafe_allow_html=True)

        export_cols = st.columns(2)

        with export_cols[0]:
            if st.button("Export Nodes (CSV)", use_container_width=True):
                try:
                    nodes_df = connector.export_nodes_to_df()
                    csv = nodes_df.to_csv(index=False)
                    st.download_button(
                        "Download Nodes CSV",
                        csv,
                        "knowledge_graph_nodes.csv",
                        "text/csv",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Error exporting nodes: {e}")

        with export_cols[1]:
            if st.button("Export Relationships (CSV)", use_container_width=True):
                try:
                    rels_df = connector.export_relationships_to_df()
                    csv = rels_df.to_csv(index=False)
                    st.download_button(
                        "Download Relationships CSV",
                        csv,
                        "knowledge_graph_relationships.csv",
                        "text/csv",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Error exporting relationships: {e}")

        connector.close()

    except Exception as e:
        st.error(f"Error connecting to Neo4j: {e}")
        st.info("""
        **Troubleshooting:**
        - Ensure Neo4j Aura instance is running
        - Check connection credentials in neo4j_connector.py
        - Verify network connectivity to Neo4j Aura
        """)

"""
Neo4j Graph Viewer Component using Neovis.js
"""

import streamlit.components.v1 as components
import json

def render_neo4j_graph(neo4j_uri, neo4j_user, neo4j_password, 
                       initial_cypher="MATCH (n)-[r]->(m) RETURN n,r,m LIMIT 1000",
                       node_limit=1000, height=700):
    
    # HTML with embedded Neovis.js
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            }}
            
            #viz {{
                width: 100%;
                height: {height}px;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background: #ffffff;
            }}
            
            .controls {{
                padding: 15px;
                background: #f8f9fa;
                border-radius: 8px;
                margin-bottom: 15px;
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }}
            
            .controls input {{
                flex: 1;
                min-width: 300px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }}
            
            .controls button {{
                padding: 10px 20px;
                background: #1976d2;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: 500;
                transition: background 0.2s;
            }}
            
            .controls button:hover {{
                background: #1565c0;
            }}
            
            .info {{
                padding: 10px;
                background: #e3f2fd;
                border-radius: 5px;
                margin-bottom: 10px;
                font-size: 13px;
            }}
            
            .loading {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 18px;
                color: #1976d2;
            }}
        </style>
    </head>
    <body>
        <div class="info">
            <strong>Controls:</strong> 
            Click nodes to expand • Double-click to focus • 
            Scroll to zoom • Drag to move • 
            Right-click for options
        </div>
        
        <div class="controls">
            <input type="text" id="cypherQuery" value="{initial_cypher}" 
                   placeholder="Enter Cypher query...">
            <button onclick="updateGraph()">Run Query</button>
            <button onclick="resetView()">Reset View</button>
            <button onclick="fitGraph()">Fit to Screen</button>
        </div>
        
        <div id="viz">
            <div class="loading">Loading graph data...</div>
        </div>
        
        <!-- Load Neovis.js from CDN -->
        <script src="https://unpkg.com/neovis.js@2.1.0"></script>
        
        <script>
            let viz;
            
            // Neo4j connection config
            const config = {{
                containerId: "viz",
                neo4j: {{
                    serverUrl: "{neo4j_uri}",
                    serverUser: "{neo4j_user}",
                    serverPassword: "{neo4j_password}"

                }},
                visConfig: {{
                    nodes: {{
                        shape: 'dot',
                        size: 25,
                        font: {{
                            size: 14,
                            color: '#000000'
                        }},
                        borderWidth: 2,
                        shadow: true
                    }},
                    edges: {{
                        arrows: {{
                            to: {{enabled: true, scaleFactor: 0.5}}
                        }},
                        color: {{
                            color: '#848484',
                            highlight: '#1976d2',
                            hover: '#333333'
                        }},
                        width: 2,
                        smooth: {{
                            type: 'continuous'
                        }},
                        font: {{
                            size: 11,
                            align: 'middle',
                            background: 'rgba(255,255,255,0.8)'
                        }}
                    }},
                    physics: {{
                        enabled: true,
                        stabilization: {{
                            iterations: 200,
                            fit: true
                        }},
                        barnesHut: {{
                            gravitationalConstant: -8000,
                            centralGravity: 0.3,
                            springLength: 150,
                            springConstant: 0.04,
                            damping: 0.09,
                            avoidOverlap: 0.2
                        }}
                    }},
                    interaction: {{
                        hover: true,
                        tooltipDelay: 200,
                        navigationButtons: true,
                        keyboard: true
                    }}
                }},
                labels: {{
                    "Person": {{
                        label: "name",
                        value: "connections",
                        group: "Person",
                        [NeoVis.NEOVIS_ADVANCED_CONFIG]: {{
                            static: {{
                                color: "#FFE66D",
                                font: {{color: "#000000"}}
                            }}
                        }}
                    }},
                    "Organization": {{
                        label: "name",
                        value: "connections",
                        group: "Organization",
                        [NeoVis.NEOVIS_ADVANCED_CONFIG]: {{
                            static: {{
                                color: "#4ECDC4",
                                font: {{color: "#000000"}}
                            }}
                        }}
                    }},
                    "Ministry": {{
                        label: "name",
                        value: "connections",
                        group: "Ministry",
                        [NeoVis.NEOVIS_ADVANCED_CONFIG]: {{
                            static: {{
                                color: "#FF9FF3",
                                font: {{color: "#000000"}}
                            }}
                        }}
                    }},
                    "Entity": {{
                        label: "name",
                        value: "connections",
                        group: "Entity",
                        [NeoVis.NEOVIS_ADVANCED_CONFIG]: {{
                            static: {{
                                color: "#FF6B6B",
                                font: {{color: "#000000"}}
                            }}
                        }}
                    }},
                    "Partner": {{
                        label: "name",
                        value: "connections",
                        group: "Partner",
                        [NeoVis.NEOVIS_ADVANCED_CONFIG]: {{
                            static: {{
                                color: "#95E1D3",
                                font: {{color: "#000000"}}
                            }}
                        }}
                    }},
                    "Company": {{
                        label: "name",
                        value: "connections",
                        group: "Company",
                        [NeoVis.NEOVIS_ADVANCED_CONFIG]: {{
                            static: {{
                                color: "#38B6FF",
                                font: {{color: "#000000"}}
                            }}
                        }}
                    }},
                    "Policy": {{
                        label: "name",
                        value: "connections",
                        group: "Policy",
                        [NeoVis.NEOVIS_ADVANCED_CONFIG]: {{
                            static: {{
                                color: "#5F27CD",
                                font: {{color: "#000000"}}
                            }}
                        }}
                    }}
                }},
                relationships: {{
                    "WORKS_AT": {{
                        thickness: "weight",
                        caption: true
                    }},
                    "PARTNERS_WITH": {{
                        thickness: "weight",
                        caption: true
                    }},
                    "REPORTS_TO": {{
                        thickness: "weight",
                        caption: true
                    }},
                    "MANAGES": {{
                        thickness: "weight",
                        caption: true
                    }},
                    "ALIGNED_WITH": {{
                        thickness: "weight",
                        caption: true
                    }}
                }},
                initialCypher: "{initial_cypher}"
            }};
            
            // Initialize visualization
            function initViz() {{
                viz = new NeoVis.default(config);
                viz.render();
                
                // Event handlers
                viz.registerOnEvent("completed", function(e) {{
                    console.log("Graph rendering completed");
                    document.querySelector('.loading').style.display = 'none';
                }});
                
                viz.registerOnEvent("clickNode", function(e) {{
                    console.log("Node clicked:", e);
                }});
            }}
            
            // Update graph with new query
            function updateGraph() {{
                const query = document.getElementById('cypherQuery').value;
                viz.updateWithCypher(query);
            }}
            
            // Reset view
            function resetView() {{
                viz.stabilize();
            }}
            
            // Fit graph to screen
            function fitGraph() {{
                viz.stabilize();
            }}
            
            // Initialize on load
            window.onload = initViz;
        </script>
    </body>
    </html>
    """
    
    # Render the HTML component
    components.html(html_code, height=height + 150, scrolling=False)
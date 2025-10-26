from neo4j import GraphDatabase
import pandas as pd

class Neo4jConnector:
    def __init__(self, uri="neo4j+s://8707aa85.databases.neo4j.io", user="neo4j", password="h1sc_XQWc16ERF0oT_B8y59hBhJ1KTvsZ5t91qtk-Ns"):

        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def get_full_graph_data(self, limit=200, filter_labels=None):
        """Get complete graph data for visualization with optional label filtering"""
        with self.driver.session() as session:
            # Build label filter
            label_filter = ""
            if filter_labels:
                label_filter = f"WHERE labels(n)[0] IN {filter_labels}"

            # Get all nodes
            nodes_query = f"""
            MATCH (n)
            {label_filter}
            RETURN id(n) as id,
                   labels(n)[0] as label,
                   n.name as name,
                   properties(n) as properties
            LIMIT {limit}
            """
            nodes_result = session.run(nodes_query)
            nodes = [dict(record) for record in nodes_result]

            # Get node IDs for relationship filtering
            node_ids = [node['id'] for node in nodes]

            # Get relationships only between displayed nodes
            rels_query = f"""
            MATCH (n)-[r]->(m)
            WHERE id(n) IN $node_ids AND id(m) IN $node_ids
            RETURN id(n) as source,
                   id(m) as target,
                   type(r) as relationship,
                   properties(r) as properties
            """
            rels_result = session.run(rels_query, node_ids=node_ids)
            relationships = [dict(record) for record in rels_result]

            return nodes, relationships
    
    def get_graph_statistics(self, filter_labels=None, limit=None):
        """Get graph statistics with optional filtering"""
        with self.driver.session() as session:
            stats = {}

            # Build label filter
            label_filter = ""
            if filter_labels:
                label_filter = f"WHERE labels(n)[0] IN {filter_labels}"

            # Build limit clause
            limit_clause = f"LIMIT {limit}" if limit else ""

            # Total counts
            stats['total_nodes'] = session.run(f"MATCH (n) {label_filter} RETURN count(n) as count {limit_clause}").single()['count']
            stats['total_relationships'] = session.run(f"MATCH (n)-[r]->() {label_filter} RETURN count(r) as count {limit_clause}").single()['count']

            # Node types
            node_types = session.run(f"""
                MATCH (n)
                {label_filter}
                RETURN labels(n)[0] as type, count(n) as count
                ORDER BY count DESC
            """)
            stats['node_types'] = {record['type']: record['count'] for record in node_types if record['type']}

            # Relationship types
            rel_types = session.run(f"""
                MATCH (n)-[r]->()
                {label_filter}
                RETURN type(r) as type, count(r) as count
                ORDER BY count DESC
            """)
            stats['relationship_types'] = {record['type']: record['count'] for record in rel_types}

            # Most connected nodes
            most_connected = session.run(f"""
                MATCH (n)
                {label_filter}
                OPTIONAL MATCH (n)-[r]-()
                WITH n, count(r) as connections
                WHERE connections > 0
                RETURN n.name as name, labels(n)[0] as type, connections
                ORDER BY connections DESC
                LIMIT 10
            """)
            stats['most_connected'] = [dict(record) for record in most_connected]

            return stats
    
    def export_nodes_to_df(self):
        """Export all nodes to pandas DataFrame"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n)
                RETURN id(n) as id, labels(n) as labels, properties(n) as properties
            """)
            
            data = []
            for record in result:
                row = {'id': record['id'], 'labels': '|'.join(record['labels'])}
                row.update(record['properties'])
                data.append(row)
            
            return pd.DataFrame(data)
    
    def export_relationships_to_df(self):
        """Export all relationships to pandas DataFrame"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n)-[r]->(m)
                RETURN id(n) as source_id, id(m) as target_id, 
                       type(r) as type, properties(r) as properties
            """)
            
            data = []
            for record in result:
                row = {
                    'source_id': record['source_id'],
                    'target_id': record['target_id'],
                    'type': record['type']
                }
                if record['properties']:
                    row.update(record['properties'])
                data.append(row)
            
            return pd.DataFrame(data)
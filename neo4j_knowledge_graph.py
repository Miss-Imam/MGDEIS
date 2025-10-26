"""
Neo4j Knowledge Graph Setup for Malaysian Government Mapping
Complete implementation with data import, queries, and dashboard integration
"""

from neo4j import GraphDatabase
import pandas as pd
import logging
from typing import List, Dict
import json

logging.basicConfig(level=logging.INFO)

class GovernmentKnowledgeGraph:
    """
    Manage Neo4j Knowledge Graph for Government Entities
    
    Graph Schema:
    - Nodes: Entity, Person, Company, Policy, Project
    - Relationships: REPORTS_TO, WORKS_FOR, PARTNERS_WITH, ALIGNED_TO, MANAGES
    """
    
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        logging.info("Connected to Neo4j")
    
    def close(self):
        self.driver.close()
    
    def clear_database(self):
        """Clear all data - use with caution!"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logging.info("Database cleared")
    
    def create_constraints(self):
        """Create uniqueness constraints and indexes"""
        constraints = [
            "CREATE CONSTRAINT entity_id IF NOT EXISTS FOR (e:Entity) REQUIRE e.entity_id IS UNIQUE",
            "CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.person_id IS UNIQUE",
            "CREATE CONSTRAINT company_id IF NOT EXISTS FOR (c:Company) REQUIRE c.partner_id IS UNIQUE",
            "CREATE CONSTRAINT policy_name IF NOT EXISTS FOR (pol:Policy) REQUIRE pol.name IS UNIQUE",
            
            # Indexes for common queries
            "CREATE INDEX entity_name IF NOT EXISTS FOR (e:Entity) ON (e.name)",
            "CREATE INDEX person_name IF NOT EXISTS FOR (p:Person) ON (p.name)",
            "CREATE INDEX company_name IF NOT EXISTS FOR (c:Company) ON (c.name)",
        ]
        
        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                    logging.info(f"Created: {constraint.split('FOR')[0]}")
                except Exception as e:
                    logging.warning(f"Constraint might already exist: {e}")
    
    def import_entities(self, entities_df: pd.DataFrame):
        """Import government entities as nodes"""
        logging.info(f"Importing {len(entities_df)} entities...")
        
        query = """
        UNWIND $entities AS entity
        MERGE (e:Entity {entity_id: entity.entity_id})
        SET e.name = entity.name,
            e.entity_type = entity.entity_type,
            e.mandate = entity.mandate,
            e.state = entity.state,
            e.latitude = toFloat(entity.latitude),
            e.longitude = toFloat(entity.longitude),
            e.created_at = datetime()
        
        // Create entity type-specific labels
        WITH e, entity
        CALL apoc.create.addLabels(e, [entity.entity_type]) YIELD node
        RETURN count(node) as created
        """
        
        # If APOC is not available, use simpler version:
        query_simple = """
        UNWIND $entities AS entity
        MERGE (e:Entity {entity_id: entity.entity_id})
        SET e.name = entity.name,
            e.entity_type = entity.entity_type,
            e.mandate = entity.mandate,
            e.state = entity.state,
            e.latitude = toFloat(entity.latitude),
            e.longitude = toFloat(entity.longitude),
            e.created_at = datetime()
        RETURN count(e) as created
        """
        
        entities_data = entities_df.to_dict('records')
        
        with self.driver.session() as session:
            result = session.run(query_simple, entities=entities_data)
            count = result.single()['created']
            logging.info(f"Created/updated {count} entity nodes")
        
        # Create hierarchical relationships
        self._create_entity_hierarchy(entities_df)
        
        # Create policy alignments
        self._create_policy_alignments(entities_df)
    
    def _create_entity_hierarchy(self, entities_df: pd.DataFrame):
        """Create REPORTS_TO relationships for organizational hierarchy"""
        logging.info("Creating organizational hierarchy...")
        
        query = """
        UNWIND $relationships AS rel
        MATCH (child:Entity {entity_id: rel.child_id})
        MATCH (parent:Entity {entity_id: rel.parent_id})
        MERGE (child)-[r:REPORTS_TO]->(parent)
        SET r.created_at = datetime()
        RETURN count(r) as created
        """
        
        # Filter entities with parent organizations
        hierarchical = entities_df[entities_df['parent_org'].notna()].copy()
        relationships = [
            {'child_id': row['entity_id'], 'parent_id': row['parent_org']}
            for _, row in hierarchical.iterrows()
        ]
        
        if relationships:
            with self.driver.session() as session:
                result = session.run(query, relationships=relationships)
                count = result.single()['created']
                logging.info(f"Created {count} hierarchical relationships")
    
    def _create_policy_alignments(self, entities_df: pd.DataFrame):
        """Create Policy nodes and ALIGNED_TO relationships"""
        logging.info("Creating policy alignments...")
        
        # Extract unique policies
        all_policies = set()
        for policies in entities_df['policy_alignment'].dropna():
            if isinstance(policies, str):
                all_policies.update([p.strip() for p in policies.split('|')])
        
        # Create policy nodes
        create_policy_query = """
        UNWIND $policies AS policy_name
        MERGE (p:Policy {name: policy_name})
        SET p.created_at = datetime()
        RETURN count(p) as created
        """
        
        with self.driver.session() as session:
            result = session.run(create_policy_query, policies=list(all_policies))
            logging.info(f"Created {result.single()['created']} policy nodes")
        
        # Create alignment relationships
        alignment_query = """
        UNWIND $alignments AS align
        MATCH (e:Entity {entity_id: align.entity_id})
        MATCH (p:Policy {name: align.policy_name})
        MERGE (e)-[r:ALIGNED_TO]->(p)
        SET r.created_at = datetime()
        RETURN count(r) as created
        """
        
        alignments = []
        for _, row in entities_df.iterrows():
            if pd.notna(row['policy_alignment']):
                policies = [p.strip() for p in row['policy_alignment'].split('|')]
                for policy in policies:
                    alignments.append({
                        'entity_id': row['entity_id'],
                        'policy_name': policy
                    })
        
        with self.driver.session() as session:
            result = session.run(alignment_query, alignments=alignments)
            count = result.single()['created']
            logging.info(f"Created {count} policy alignment relationships")
    
    def import_people(self, people_df: pd.DataFrame):
        """Import people as nodes and create WORKS_FOR relationships"""
        logging.info(f"Importing {len(people_df)} people...")
        
        query = """
        UNWIND $people AS person
        MERGE (p:Person {person_id: person.person_id})
        SET p.name = person.name,
            p.title = person.title,
            p.role_type = person.role_type,
            p.focus_area = person.focus_area,
            p.confidence_score = toFloat(person.confidence_score),
            p.email = person.email,
            p.source = person.source,
            p.created_at = datetime()
        RETURN count(p) as created
        """
        
        people_data = people_df.to_dict('records')
        
        with self.driver.session() as session:
            result = session.run(query, people=people_data)
            count = result.single()['created']
            logging.info(f"Created/updated {count} person nodes")
        
        # Create WORKS_FOR relationships
        works_for_query = """
        UNWIND $relationships AS rel
        MATCH (p:Person {person_id: rel.person_id})
        MATCH (e:Entity {entity_id: rel.entity_id})
        MERGE (p)-[r:WORKS_FOR]->(e)
        SET r.created_at = datetime()
        RETURN count(r) as created
        """
        
        relationships = [
            {'person_id': row['person_id'], 'entity_id': row['entity_id']}
            for _, row in people_df.iterrows()
        ]
        
        with self.driver.session() as session:
            result = session.run(works_for_query, relationships=relationships)
            count = result.single()['created']
            logging.info(f"Created {count} WORKS_FOR relationships")
    
    def import_partners(self, partners_df: pd.DataFrame):
        """Import private sector partners and create relationships"""
        logging.info(f"Importing {len(partners_df)} partners...")
        
        query = """
        UNWIND $partners AS partner
        MERGE (c:Company {partner_id: partner.partner_id})
        SET c.name = partner.company_name,
            c.focus_area = partner.focus_area,
            c.created_at = datetime()
        RETURN count(c) as created
        """
        
        partners_data = partners_df.to_dict('records')
        
        with self.driver.session() as session:
            result = session.run(query, partners=partners_data)
            count = result.single()['created']
            logging.info(f"Created/updated {count} company nodes")
        
        # Create PARTNERS_WITH relationships
        partnership_query = """
        UNWIND $relationships AS rel
        MATCH (c:Company {partner_id: rel.partner_id})
        MATCH (e:Entity {entity_id: rel.entity_id})
        MERGE (c)-[r:PARTNERS_WITH]->(e)
        SET r.relationship_type = rel.relationship_type,
            r.contract_value_rm = toInteger(rel.contract_value_rm),
            r.contract_year = toInteger(rel.contract_year),
            r.procurement_stage = rel.procurement_stage,
            r.created_at = datetime()
        RETURN count(r) as created
        """
        
        relationships = partners_df.to_dict('records')
        
        with self.driver.session() as session:
            result = session.run(partnership_query, relationships=relationships)
            count = result.single()['created']
            logging.info(f"Created {count} PARTNERS_WITH relationships")
    
    # ========================================================================
    # QUERY METHODS - Common use cases
    # ========================================================================
    
    def find_entity_by_name(self, name: str) -> List[Dict]:
        """Find entity by name (fuzzy search)"""
        query = """
        MATCH (e:Entity)
        WHERE toLower(e.name) CONTAINS toLower($name)
        RETURN e.entity_id as id, e.name as name, e.entity_type as type, 
               e.mandate as mandate
        """
        
        with self.driver.session() as session:
            result = session.run(query, name=name)
            return [dict(record) for record in result]
    
    def get_entity_hierarchy(self, entity_id: str) -> Dict:
        """Get full hierarchy for an entity (parents and children)"""
        query = """
        MATCH path = (e:Entity {entity_id: $entity_id})-[:REPORTS_TO*0..]->(parent)
        WITH e, collect(parent) as parents
        MATCH (child)-[:REPORTS_TO*0..]->(e)
        RETURN e.name as entity_name,
               [p in parents | {name: p.name, id: p.entity_id, type: p.entity_type}] as parents,
               collect({name: child.name, id: child.entity_id, type: child.entity_type}) as children
        """
        
        with self.driver.session() as session:
            result = session.run(query, entity_id=entity_id)
            return dict(result.single())
    
    def get_key_people_for_entity(self, entity_id: str) -> List[Dict]:
        """Get all people working for an entity"""
        query = """
        MATCH (p:Person)-[:WORKS_FOR]->(e:Entity {entity_id: $entity_id})
        RETURN p.name as name, p.title as title, p.role_type as role,
               p.focus_area as focus, p.email as email, p.confidence_score as confidence
        ORDER BY p.confidence_score DESC
        """
        
        with self.driver.session() as session:
            result = session.run(query, entity_id=entity_id)
            return [dict(record) for record in result]
    
    def get_partners_for_entity(self, entity_id: str) -> List[Dict]:
        """Get all private sector partners for an entity"""
        query = """
        MATCH (c:Company)-[r:PARTNERS_WITH]->(e:Entity {entity_id: $entity_id})
        RETURN c.name as company, r.relationship_type as relationship,
               r.contract_value_rm as value, r.contract_year as year,
               r.procurement_stage as stage
        ORDER BY r.contract_value_rm DESC
        """
        
        with self.driver.session() as session:
            result = session.run(query, entity_id=entity_id)
            return [dict(record) for record in result]
    
    def find_entities_by_policy(self, policy_name: str) -> List[Dict]:
        """Find all entities aligned to a specific policy"""
        query = """
        MATCH (e:Entity)-[:ALIGNED_TO]->(p:Policy {name: $policy_name})
        RETURN e.entity_id as id, e.name as name, e.entity_type as type,
               e.mandate as mandate
        ORDER BY e.entity_type, e.name
        """
        
        with self.driver.session() as session:
            result = session.run(query, policy_name=policy_name)
            return [dict(record) for record in result]
    
    def find_decision_makers_for_focus_area(self, focus_area: str) -> List[Dict]:
        """Find key decision makers in a specific focus area"""
        query = """
        MATCH (p:Person)-[:WORKS_FOR]->(e:Entity)
        WHERE toLower(p.focus_area) CONTAINS toLower($focus_area)
          AND p.role_type IN ['Political', 'Executive']
        RETURN p.name as name, p.title as title, p.focus_area as focus,
               e.name as organization, p.email as email, p.confidence_score as confidence
        ORDER BY p.confidence_score DESC
        LIMIT 20
        """
        
        with self.driver.session() as session:
            result = session.run(query, focus_area=focus_area)
            return [dict(record) for record in result]
    
    def get_company_government_network(self, company_name: str) -> Dict:
        """Get all government entities a company works with"""
        query = """
        MATCH (c:Company)-[r:PARTNERS_WITH]->(e:Entity)
        WHERE toLower(c.name) CONTAINS toLower($company_name)
        RETURN c.name as company,
               collect({
                   entity: e.name,
                   type: e.entity_type,
                   relationship: r.relationship_type,
                   value: r.contract_value_rm,
                   year: r.contract_year
               }) as partnerships
        """
        
        with self.driver.session() as session:
            result = session.run(query, company_name=company_name)
            return dict(result.single())
    
    def get_procurement_flow(self, min_value: int = 1000000) -> List[Dict]:
        """Get procurement flow for Sankey diagram"""
        query = """
        MATCH (c:Company)-[r:PARTNERS_WITH]->(e:Entity)
        WHERE r.contract_value_rm >= $min_value
        RETURN e.name as source, c.name as target, 
               r.contract_value_rm as value, r.relationship_type as type
        ORDER BY r.contract_value_rm DESC
        """
        
        with self.driver.session() as session:
            result = session.run(query, min_value=min_value)
            return [dict(record) for record in result]
    
    def get_mydigital_ecosystem(self) -> Dict:
        """Get complete MyDIGITAL ecosystem overview"""
        query = """
        MATCH (e:Entity)-[:ALIGNED_TO]->(p:Policy {name: 'MyDIGITAL'})
        OPTIONAL MATCH (person:Person)-[:WORKS_FOR]->(e)
        OPTIONAL MATCH (company:Company)-[:PARTNERS_WITH]->(e)
        RETURN e.name as entity,
               e.entity_type as type,
               count(DISTINCT person) as key_people,
               count(DISTINCT company) as partners,
               sum(CASE WHEN company IS NOT NULL THEN 1 ELSE 0 END) as total_partnerships
        ORDER BY key_people DESC, partners DESC
        """
        
        with self.driver.session() as session:
            result = session.run(query)
            return [dict(record) for record in result]
    
    def find_shortest_path_to_decision_maker(self, start_entity_id: str, target_focus: str) -> List[Dict]:
        """Find shortest path from an entity to a decision maker in a focus area"""
        query = """
        MATCH (start:Entity {entity_id: $start_entity_id})
        MATCH (target:Person)
        WHERE toLower(target.focus_area) CONTAINS toLower($target_focus)
          AND target.role_type IN ['Political', 'Executive']
        MATCH path = shortestPath((start)-[*..5]-(target))
        RETURN [node in nodes(path) | 
                CASE 
                    WHEN 'Entity' IN labels(node) THEN {type: 'Entity', name: node.name}
                    WHEN 'Person' IN labels(node) THEN {type: 'Person', name: node.name, title: node.title}
                END
               ] as path,
               length(path) as hops
        ORDER BY hops
        LIMIT 5
        """
        
        with self.driver.session() as session:
            result = session.run(query, start_entity_id=start_entity_id, target_focus=target_focus)
            return [dict(record) for record in result]
    
    def get_graph_statistics(self) -> Dict:
        """Get overall graph statistics"""
        query = """
        MATCH (e:Entity) WITH count(e) as entities
        MATCH (p:Person) WITH entities, count(p) as people
        MATCH (c:Company) WITH entities, people, count(c) as companies
        MATCH (pol:Policy) WITH entities, people, companies, count(pol) as policies
        MATCH ()-[r]->() WITH entities, people, companies, policies, count(r) as relationships
        RETURN entities, people, companies, policies, relationships
        """
        
        with self.driver.session() as session:
            result = session.run(query)
            return dict(result.single())


# ============================================================================
# STREAMLIT DASHBOARD INTEGRATION
# ============================================================================

def integrate_with_streamlit():
    """
    Example integration with Streamlit dashboard
    Add this to your dashboard.py file
    """
    
    import streamlit as st
    
    # Initialize Neo4j connection
    @st.cache_resource
    def get_neo4j_connection():
        return GovernmentKnowledgeGraph(
            uri=st.secrets.get("NEO4J_URI", "bolt://localhost:7687"),
            user=st.secrets.get("NEO4J_USER", "neo4j"),
            password=st.secrets.get("NEO4J_PASSWORD", "govtmapping2025")
        )
    
    kg = get_neo4j_connection()
    
    # Example: Add to search tab
    st.header("Knowledge Graph Search")
    
    query_type = st.selectbox(
        "Query Type",
        ["Find Entity", "Get Hierarchy", "Find Decision Makers", "Get MyDIGITAL Ecosystem"]
    )
    
    if query_type == "Find Entity":
        entity_name = st.text_input("Entity Name")
        if st.button("Search"):
            results = kg.find_entity_by_name(entity_name)
            st.write(results)
    
    elif query_type == "Find Decision Makers":
        focus_area = st.text_input("Focus Area (e.g., 'AI', 'Digital')")
        if st.button("Search"):
            results = kg.find_decision_makers_for_focus_area(focus_area)
            st.dataframe(pd.DataFrame(results))
    
    elif query_type == "Get MyDIGITAL Ecosystem":
        if st.button("Get Ecosystem"):
            results = kg.get_mydigital_ecosystem()
            st.dataframe(pd.DataFrame(results))


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Complete setup and import workflow"""
    
    # Initialize connection
    kg = GovernmentKnowledgeGraph(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="your_password"  # Change this!
    )
    
    # Create schema
    kg.create_constraints()
    
    # Load data
    entities_df = pd.read_csv('data/entities.csv')
    people_df = pd.read_csv('data/people.csv')
    partners_df = pd.read_csv('data/partners.csv')
    
    # Import data
    kg.import_entities(entities_df)
    kg.import_people(people_df)
    kg.import_partners(partners_df)
    
    # Get statistics
    stats = kg.get_graph_statistics()
    print("\n" + "="*50)
    print("Knowledge Graph Statistics:")
    print("="*50)
    print(f"Entities: {stats['entities']}")
    print(f"People: {stats['people']}")
    print(f"Companies: {stats['companies']}")
    print(f"Policies: {stats['policies']}")
    print(f"Relationships: {stats['relationships']}")
    print("="*50)
    
    # Example queries
    print("\nExample: Find entities aligned with MyDIGITAL")
    mydigital_entities = kg.find_entities_by_policy("MyDIGITAL")
    for entity in mydigital_entities:
        print(f"  - {entity['name']} ({entity['type']})")
    
    print("\nExample: Find AI decision makers")
    ai_leaders = kg.find_decision_makers_for_focus_area("AI")
    for leader in ai_leaders[:5]:
        print(f"  - {leader['name']} - {leader['title']} at {leader['organization']}")
    
    # Close connection
    kg.close()


if __name__ == "__main__":
    main()
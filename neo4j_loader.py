from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import pandas as pd
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Neo4jLoader:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
    
    def clear_database(self):
        """Clear all nodes and relationships"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.info("Database cleared")
    
    def create_constraints(self):
        """Create unique constraints"""
        constraints = [
            "CREATE CONSTRAINT entity_id IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE",
            "CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT partner_id IF NOT EXISTS FOR (p:Partner) REQUIRE p.id IS UNIQUE"
        ]
        
        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                    logger.info(f"Created constraint: {constraint}")
                except Exception as e:
                    logger.warning(f"Constraint might already exist: {e}")
    
    def load_entities(self, entities_df):
        """Load government entities"""
        with self.driver.session() as session:
            for _, row in entities_df.iterrows():
                query = """
                MERGE (e:Entity {id: $id})
                SET e.name = $name,
                    e.type = $type,
                    e.category = $category,
                    e.parent_ministry = $parent_ministry,
                    e.website = $website,
                    e.description = $description,
                    e.location = $location,
                    e.latitude = $latitude,
                    e.longitude = $longitude
                """
                session.run(query, 
                    id=str(row.get('id', '')),
                    name=str(row.get('name', '')),
                    type=str(row.get('type', '')),
                    category=str(row.get('category', '')),
                    parent_ministry=str(row.get('parent_ministry', '')),
                    website=str(row.get('website', '')),
                    description=str(row.get('description', '')),
                    location=str(row.get('location', '')),
                    latitude=float(row.get('latitude', 0)) if pd.notna(row.get('latitude')) else None,
                    longitude=float(row.get('longitude', 0)) if pd.notna(row.get('longitude')) else None
                )
            logger.info(f"Loaded {len(entities_df)} entities")
    
    def load_people(self, people_df):
        """Load key people"""
        with self.driver.session() as session:
            for _, row in people_df.iterrows():
                query = """
                MERGE (p:Person {id: $id})
                SET p.name = $name,
                    p.position = $position,
                    p.entity = $entity,
                    p.email = $email,
                    p.phone = $phone,
                    p.background = $background
                """
                session.run(query,
                    id=str(row.get('id', '')),
                    name=str(row.get('name', '')),
                    position=str(row.get('position', '')),
                    entity=str(row.get('entity', '')),
                    email=str(row.get('email', '')),
                    phone=str(row.get('phone', '')),
                    background=str(row.get('background', ''))
                )
            logger.info(f"Loaded {len(people_df)} people")
    
    def load_partners(self, partners_df):
        """Load private sector partners"""
        with self.driver.session() as session:
            for _, row in partners_df.iterrows():
                query = """
                MERGE (p:Partner {id: $id})
                SET p.company_name = $company_name,
                    p.sector = $sector,
                    p.govt_entity = $govt_entity,
                    p.project_name = $project_name,
                    p.value_rm = $value_rm,
                    p.start_date = $start_date,
                    p.status = $status
                """
                session.run(query,
                    id=str(row.get('id', '')),
                    company_name=str(row.get('company_name', '')),
                    sector=str(row.get('sector', '')),
                    govt_entity=str(row.get('govt_entity', '')),
                    project_name=str(row.get('project_name', '')),
                    value_rm=float(row.get('value_rm', 0)) if pd.notna(row.get('value_rm')) else None,
                    start_date=str(row.get('start_date', '')),
                    status=str(row.get('status', ''))
                )
            logger.info(f"Loaded {len(partners_df)} partnerships")
    
    def create_relationships(self):
        """Create relationships between entities"""
        with self.driver.session() as session:
            # Person works at Entity
            session.run("""
                MATCH (p:Person), (e:Entity)
                WHERE p.entity = e.name
                MERGE (p)-[:WORKS_AT]->(e)
            """)
            
            # Partner partners with Entity
            session.run("""
                MATCH (p:Partner), (e:Entity)
                WHERE p.govt_entity = e.name
                MERGE (p)-[:PARTNERS_WITH]->(e)
            """)
            
            logger.info("Created relationships")

def main():
    # Load credentials
    uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    user = os.getenv('NEO4J_USER', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD', 'govtmapping2025')
    
    logger.info(f"Connecting to Neo4j at {uri}")
    
    # Initialize loader
    loader = Neo4jLoader(uri, user, password)
    
    try:
        # Clear existing data
        logger.info("Clearing existing data...")
        loader.clear_database()
        
        # Create constraints
        logger.info("Creating constraints...")
        loader.create_constraints()
        
        # Load data
        logger.info("Loading entities...")
        entities = pd.read_csv('data/processed/entities.csv')
        loader.load_entities(entities)
        
        logger.info("Loading people...")
        people = pd.read_csv('data/processed/people.csv')
        loader.load_people(people)
        
        logger.info("Loading partners...")
        partners = pd.read_csv('data/processed/partners.csv')
        loader.load_partners(partners)
        
        # Create relationships
        logger.info("Creating relationships...")
        loader.create_relationships()
        
        logger.info("✅ Data loaded successfully!")
        
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise
    finally:
        loader.close()

if __name__ == "__main__":
    main()
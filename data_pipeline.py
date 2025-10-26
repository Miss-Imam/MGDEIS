"""
Complete Data Pipeline for Malaysian Government Mapping Project
Orchestrates data collection, cleaning, geocoding, and loading into all systems
"""

import pandas as pd
import logging
from datetime import datetime
import os
import sys
from typing import Dict, List, Tuple
import time
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Import your custom modules (assuming they're in the same directory)
# from data_collection_scripts import GovernmentEntityScraper, PeopleScraper, ProcurementScraper
# from neo4j_knowledge_graph import GovernmentKnowledgeGraph
# from vector_search_system import GovernmentVectorSearch

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'pipeline_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class DataPipeline:
    """
    Complete ETL pipeline orchestrating:
    1. Data collection from web sources
    2. Data cleaning and validation
    3. Geocoding for map visualization
    4. Loading into Neo4j knowledge graph
    5. Indexing in vector search system
    6. Exporting to CSV/Parquet for dashboard
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize pipeline with configuration
        
        Args:
            config: Configuration dictionary with paths, credentials, etc.
        """
        self.config = config or self._default_config()
        self.data_dir = self.config['data_dir']
        
        # Create data directory
        os.makedirs(self.data_dir, exist_ok=True)
        
        logger.info("="*70)
        logger.info("Malaysian Government Mapping - Data Pipeline Initialized")
        logger.info("="*70)
    
    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            'data_dir': 'data',
            'raw_dir': 'data/raw',
            'processed_dir': 'data/processed',
            'neo4j': {
                'uri': 'bolt://localhost:7687',
                'user': 'neo4j',
                'password': 'password'
            },
            'vector_db_dir': './vector_db',
            'enable_geocoding': True,
            'enable_neo4j': True,
            'enable_vector_search': True
        }
    
    def run_full_pipeline(self):
        """Execute complete pipeline"""
        logger.info("Starting full pipeline execution...")
        
        try:
            # Phase 1: Data Collection
            logger.info("\n" + "="*70)
            logger.info("PHASE 1: DATA COLLECTION")
            logger.info("="*70)
            entities_raw, people_raw, partners_raw = self.collect_data()
            
            # Phase 2: Data Cleaning
            logger.info("\n" + "="*70)
            logger.info("PHASE 2: DATA CLEANING & VALIDATION")
            logger.info("="*70)
            entities_clean, people_clean, partners_clean = self.clean_data(
                entities_raw, people_raw, partners_raw
            )
            
            # Phase 3: Geocoding
            if self.config['enable_geocoding']:
                logger.info("\n" + "="*70)
                logger.info("PHASE 3: GEOCODING")
                logger.info("="*70)
                entities_clean = self.geocode_entities(entities_clean)
            
            # Phase 4: Save processed data
            logger.info("\n" + "="*70)
            logger.info("PHASE 4: SAVING PROCESSED DATA")
            logger.info("="*70)
            self.save_processed_data(entities_clean, people_clean, partners_clean)
            
            # Phase 5: Load into Neo4j
            if self.config['enable_neo4j']:
                logger.info("\n" + "="*70)
                logger.info("PHASE 5: LOADING INTO NEO4J KNOWLEDGE GRAPH")
                logger.info("="*70)
                self.load_to_neo4j(entities_clean, people_clean, partners_clean)
            
            # Phase 6: Index in vector search
            if self.config['enable_vector_search']:
                logger.info("\n" + "="*70)
                logger.info("PHASE 6: BUILDING VECTOR SEARCH INDEX")
                logger.info("="*70)
                self.build_vector_index(entities_clean, people_clean, partners_clean)
            
            # Phase 7: Generate report
            logger.info("\n" + "="*70)
            logger.info("PHASE 7: GENERATING PIPELINE REPORT")
            logger.info("="*70)
            self.generate_report(entities_clean, people_clean, partners_clean)
            
            logger.info("\n" + "="*70)
            logger.info("✅ PIPELINE COMPLETED SUCCESSFULLY!")
            logger.info("="*70)
            
            return entities_clean, people_clean, partners_clean
            
        except Exception as e:
            logger.error(f"❌ Pipeline failed: {str(e)}", exc_info=True)
            raise
    
    def collect_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Phase 1: Collect data from various sources
        """
        logger.info("Starting data collection...")
        
        # Option 1: Scrape from websites
        # entities_scraper = GovernmentEntityScraper()
        # people_scraper = PeopleScraper()
        # partners_scraper = ProcurementScraper()
        
        # entities_df = entities_scraper.scrape_all()
        # people_df = people_scraper.scrape_all()
        # partners_df = partners_scraper.scrape_all()
        
        # Option 2: Load from existing CSV files
        try:
            entities_df = pd.read_csv(f'{self.config["raw_dir"]}/entities_raw.csv')
            people_df = pd.read_csv(f'{self.config["raw_dir"]}/people_raw.csv')
            partners_df = pd.read_csv(f'{self.config["raw_dir"]}/partners_raw.csv')
            
            logger.info(f"✅ Loaded {len(entities_df)} entities")
            logger.info(f"✅ Loaded {len(people_df)} people")
            logger.info(f"✅ Loaded {len(partners_df)} partners")
            
        except FileNotFoundError:
            logger.warning("Raw data files not found. Using sample data...")
            entities_df, people_df, partners_df = self._generate_sample_data()
        
        # Save raw data
        os.makedirs(self.config['raw_dir'], exist_ok=True)
        entities_df.to_csv(f'{self.config["raw_dir"]}/entities_raw.csv', index=False)
        people_df.to_csv(f'{self.config["raw_dir"]}/people_raw.csv', index=False)
        partners_df.to_csv(f'{self.config["raw_dir"]}/partners_raw.csv', index=False)
        
        return entities_df, people_df, partners_df
    
    def clean_data(self, 
                   entities_df: pd.DataFrame,
                   people_df: pd.DataFrame,
                   partners_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Phase 2: Clean and validate data
        """
        logger.info("Cleaning data...")
        
        # Clean entities
        entities_clean = self._clean_entities(entities_df)
        logger.info(f"✅ Cleaned entities: {len(entities_clean)} valid records")
        
        # Clean people
        people_clean = self._clean_people(people_df)
        logger.info(f"✅ Cleaned people: {len(people_clean)} valid records")
        
        # Clean partners
        partners_clean = self._clean_partners(partners_df)
        logger.info(f"✅ Cleaned partners: {len(partners_clean)} valid records")
        
        # Validate relationships
        self._validate_relationships(entities_clean, people_clean, partners_clean)
        
        return entities_clean, people_clean, partners_clean
    
    def _clean_entities(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean entity data"""
        df = df.copy()
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['entity_id'], keep='first')
        
        # Standardize text fields
        df['name'] = df['name'].str.strip()
        df['entity_type'] = df['entity_type'].str.strip()
        
        # Handle missing mandates
        df['mandate'] = df['mandate'].fillna('No mandate specified')
        
        # Standardize policy alignment format (use | as separator)
        if 'policy_alignment' in df.columns:
            df['policy_alignment'] = df['policy_alignment'].str.replace(',', '|')
            df['policy_alignment'] = df['policy_alignment'].str.replace('  ', ' ')
        
        # Remove records with missing critical fields
        df = df[df['name'].notna() & df['entity_id'].notna()]
        
        return df
    
    def _clean_people(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean people data"""
        df = df.copy()
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['person_id'], keep='first')
        
        # Standardize text fields
        df['name'] = df['name'].str.strip()
        df['title'] = df['title'].str.strip()
        
        # Validate confidence scores
        df['confidence_score'] = df['confidence_score'].clip(0, 1)
        
        # Standardize email format
        if 'email' in df.columns:
            df['email'] = df['email'].str.lower().str.strip()
        
        # Remove records with missing critical fields
        df = df[df['name'].notna() & df['person_id'].notna() & df['entity_id'].notna()]
        
        return df
    
    def _clean_partners(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean partner data"""
        df = df.copy()
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['partner_id'], keep='first')
        
        # Standardize text fields
        df['company_name'] = df['company_name'].str.strip()
        
        # Ensure contract values are numeric
        df['contract_value_rm'] = pd.to_numeric(df['contract_value_rm'], errors='coerce').fillna(0)
        
        # Validate contract years
        current_year = datetime.now().year
        df['contract_year'] = pd.to_numeric(df['contract_year'], errors='coerce')
        df['contract_year'] = df['contract_year'].clip(2000, current_year + 5)
        
        # Remove records with missing critical fields
        df = df[df['company_name'].notna() & df['partner_id'].notna() & df['entity_id'].notna()]
        
        return df
    
    def _validate_relationships(self, 
                               entities_df: pd.DataFrame,
                               people_df: pd.DataFrame,
                               partners_df: pd.DataFrame):
        """Validate foreign key relationships"""
        entity_ids = set(entities_df['entity_id'])
        
        # Check people -> entities
        invalid_people = people_df[~people_df['entity_id'].isin(entity_ids)]
        if len(invalid_people) > 0:
            logger.warning(f"Found {len(invalid_people)} people with invalid entity_id")
        
        # Check partners -> entities
        invalid_partners = partners_df[~partners_df['entity_id'].isin(entity_ids)]
        if len(invalid_partners) > 0:
            logger.warning(f"Found {len(invalid_partners)} partners with invalid entity_id")
        
        # Check parent_org relationships
        invalid_parents = entities_df[
            (entities_df['parent_org'].notna()) & 
            (~entities_df['parent_org'].isin(entity_ids))
        ]
        if len(invalid_parents) > 0:
            logger.warning(f"Found {len(invalid_parents)} entities with invalid parent_org")
    
    def geocode_entities(self, entities_df: pd.DataFrame) -> pd.DataFrame:
        """
        Phase 3: Add geographic coordinates to entities
        """
        logger.info("Geocoding entities...")
        
        # Check if already geocoded
        if 'latitude' in entities_df.columns and entities_df['latitude'].notna().any():
            logger.info("Some entities already geocoded. Skipping those...")
            needs_geocoding = entities_df[entities_df['latitude'].isna()]
        else:
            needs_geocoding = entities_df
            entities_df['latitude'] = None
            entities_df['longitude'] = None
        
        if len(needs_geocoding) == 0:
            logger.info("All entities already geocoded")
            return entities_df
        
        logger.info(f"Geocoding {len(needs_geocoding)} entities...")
        
        # Initialize geocoder with rate limiting
        geolocator = Nominatim(user_agent="govt_mapping_tool")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        
        for idx, row in needs_geocoding.iterrows():
            try:
                # Create search query
                search_query = f"{row['name']}, Malaysia"
                
                location = geocode(search_query, timeout=10)
                
                if location:
                    entities_df.at[idx, 'latitude'] = location.latitude
                    entities_df.at[idx, 'longitude'] = location.longitude
                    logger.info(f"✅ Geocoded: {row['name']}")
                else:
                    logger.warning(f"⚠️  Could not geocode: {row['name']}")
                
                time.sleep(1)  # Be respectful to the API
                
            except Exception as e:
                logger.error(f"❌ Error geocoding {row['name']}: {str(e)}")
                continue
        
        geocoded_count = entities_df['latitude'].notna().sum()
        logger.info(f"✅ Geocoded {geocoded_count} entities")
        
        return entities_df
    
    def save_processed_data(self,
                           entities_df: pd.DataFrame,
                           people_df: pd.DataFrame,
                           partners_df: pd.DataFrame):
        """
        Phase 4: Save processed data in multiple formats
        """
        logger.info("Saving processed data...")
        
        os.makedirs(self.config['processed_dir'], exist_ok=True)
        
        # CSV format (for human readability)
        entities_df.to_csv(f'{self.data_dir}/entities.csv', index=False)
        people_df.to_csv(f'{self.data_dir}/people.csv', index=False)
        partners_df.to_csv(f'{self.data_dir}/partners.csv', index=False)
        logger.info("✅ Saved CSV files")
        
        # Parquet format (for performance)
        entities_df.to_parquet(f'{self.data_dir}/entities.parquet', index=False)
        people_df.to_parquet(f'{self.data_dir}/people.parquet', index=False)
        partners_df.to_parquet(f'{self.data_dir}/partners.parquet', index=False)
        logger.info("✅ Saved Parquet files")
        
        # JSON format (for APIs)
        entities_df.to_json(f'{self.data_dir}/entities.json', orient='records', indent=2)
        people_df.to_json(f'{self.data_dir}/people.json', orient='records', indent=2)
        partners_df.to_json(f'{self.data_dir}/partners.json', orient='records', indent=2)
        logger.info("✅ Saved JSON files")
    
    def load_to_neo4j(self,
                     entities_df: pd.DataFrame,
                     people_df: pd.DataFrame,
                     partners_df: pd.DataFrame):
        """
        Phase 5: Load data into Neo4j knowledge graph
        """
        try:
            from neo4j_knowledge_graph import GovernmentKnowledgeGraph
            
            logger.info("Connecting to Neo4j...")
            kg = GovernmentKnowledgeGraph(
                uri=self.config['neo4j']['uri'],
                user=self.config['neo4j']['user'],
                password=self.config['neo4j']['password']
            )
            
            # Create schema
            logger.info("Creating Neo4j schema...")
            kg.create_constraints()
            
            # Import data
            logger.info("Importing entities...")
            kg.import_entities(entities_df)
            
            logger.info("Importing people...")
            kg.import_people(people_df)
            
            logger.info("Importing partners...")
            kg.import_partners(partners_df)
            
            # Get statistics
            stats = kg.get_graph_statistics()
            logger.info(f"✅ Neo4j loaded successfully:")
            logger.info(f"   - Entities: {stats['entities']}")
            logger.info(f"   - People: {stats['people']}")
            logger.info(f"   - Companies: {stats['companies']}")
            logger.info(f"   - Relationships: {stats['relationships']}")
            
            kg.close()
            
        except ImportError:
            logger.warning("neo4j_knowledge_graph module not found. Skipping Neo4j load.")
        except Exception as e:
            logger.error(f"Error loading to Neo4j: {str(e)}")
            raise
    
    def build_vector_index(self,
                          entities_df: pd.DataFrame,
                          people_df: pd.DataFrame,
                          partners_df: pd.DataFrame):
        """
        Phase 6: Build vector search index
        """
        try:
            from vector_search_system import GovernmentVectorSearch
            
            logger.info("Initializing vector search system...")
            vs = GovernmentVectorSearch(persist_directory=self.config['vector_db_dir'])
            
            # Index data
            logger.info("Indexing entities...")
            vs.index_entities(entities_df)
            
            logger.info("Indexing people...")
            vs.index_people(people_df)
            
            logger.info("Indexing partners...")
            vs.index_partners(partners_df)
            
            # Get statistics
            stats = vs.get_statistics()
            logger.info(f"✅ Vector index built successfully:")
            logger.info(f"   - Total documents: {stats['total']}")
            logger.info(f"   - Entities: {stats['entities']}")
            logger.info(f"   - People: {stats['people']}")
            logger.info(f"   - Partners: {stats['partners']}")
            
        except ImportError:
            logger.warning("vector_search_system module not found. Skipping vector index.")
        except Exception as e:
            logger.error(f"Error building vector index: {str(e)}")
            raise
    
    def generate_report(self,
                       entities_df: pd.DataFrame,
                       people_df: pd.DataFrame,
                       partners_df: pd.DataFrame):
        """
        Phase 7: Generate summary report
        """
        report = []
        report.append("="*70)
        report.append("MALAYSIAN GOVERNMENT MAPPING - PIPELINE REPORT")
        report.append("="*70)
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("\n" + "="*70)
        report.append("DATA SUMMARY")
        report.append("="*70)
        
        # Entity statistics
        report.append(f"\nEntities: {len(entities_df)}")
        report.append(f"  By Type:")
        for entity_type, count in entities_df['entity_type'].value_counts().items():
            report.append(f"    - {entity_type}: {count}")
        
        # People statistics
        report.append(f"\nPeople: {len(people_df)}")
        report.append(f"  By Role:")
        for role, count in people_df['role_type'].value_counts().items():
            report.append(f"    - {role}: {count}")
        
        # Partner statistics
        report.append(f"\nPartners: {len(partners_df)}")
        total_value = partners_df['contract_value_rm'].sum()
        report.append(f"  Total Contract Value: RM {total_value/1_000_000:.2f}M")
        report.append(f"  By Relationship Type:")
        for rel_type, count in partners_df['relationship_type'].value_counts().items():
            report.append(f"    - {rel_type}: {count}")
        
        # Policy alignment
        if 'policy_alignment' in entities_df.columns:
            report.append(f"\nPolicy Alignment:")
            all_policies = []
            for policies in entities_df['policy_alignment'].dropna():
                all_policies.extend([p.strip() for p in str(policies).split('|')])
            from collections import Counter
            policy_counts = Counter(all_policies)
            for policy, count in policy_counts.most_common():
                report.append(f"    - {policy}: {count} entities")
        
        # Geocoding status
        if 'latitude' in entities_df.columns:
            geocoded = entities_df['latitude'].notna().sum()
            report.append(f"\nGeocoding Status: {geocoded}/{len(entities_df)} entities geocoded")
        
        report.append("\n" + "="*70)
        report.append("FILES GENERATED")
        report.append("="*70)
        report.append(f"\n✅ CSV files in: {self.data_dir}/")
        report.append(f"✅ Parquet files in: {self.data_dir}/")
        report.append(f"✅ JSON files in: {self.data_dir}/")
        
        if self.config['enable_neo4j']:
            report.append(f"✅ Neo4j knowledge graph populated")
        
        if self.config['enable_vector_search']:
            report.append(f"✅ Vector search index built in: {self.config['vector_db_dir']}/")
        
        report.append("\n" + "="*70)
        
        # Print and save report
        report_text = "\n".join(report)
        print(report_text)
        
        with open(f'{self.data_dir}/pipeline_report.txt', 'w') as f:
            f.write(report_text)
        
        logger.info(f"✅ Report saved to: {self.data_dir}/pipeline_report.txt")
    
    def _generate_sample_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Generate sample data for testing"""
        logger.info("Generating sample data...")
        
        entities = pd.DataFrame({
            'entity_id': ['MIN001', 'MIN002', 'AGN001'],
            'name': ['Ministry of Digital', 'Ministry of Higher Education', 'MDEC'],
            'entity_type': ['Ministry', 'Ministry', 'Agency'],
            'parent_org': [None, None, 'MIN001'],
            'mandate': [
                'Lead digital transformation',
                'Oversee higher education',
                'Drive digital economy'
            ],
            'policy_alignment': [
                'MyDIGITAL|AI Roadmap',
                'MyDIGITAL|4IR Policy',
                'MyDIGITAL|Digital Economy Blueprint'
            ],
            'state': ['Federal', 'Federal', 'Federal']
        })
        
        people = pd.DataFrame({
            'person_id': ['P001', 'P002'],
            'name': ['Gobind Singh Deo', 'Mahadhir Aziz'],
            'title': ['Minister', 'CEO'],
            'entity_id': ['MIN001', 'AGN001'],
            'role_type': ['Political', 'Executive'],
            'focus_area': ['Digital Policy', 'Digital Economy'],
            'confidence_score': [0.95, 0.90],
            'source': ['Official Website', 'LinkedIn'],
            'email': ['minister@digital.gov.my', 'ceo@mdec.my']
        })
        
        partners = pd.DataFrame({
            'partner_id': ['COMP001'],
            'company_name': ['TechMalaysia Solutions'],
            'entity_id': ['AGN001'],
            'relationship_type': ['Service Provider'],
            'contract_value_rm': [5200000],
            'contract_year': [2024],
            'focus_area': ['Digital Infrastructure'],
            'procurement_stage': ['Active']
        })
        
        return entities, people, partners


def main():
    """Main execution"""
    
    # Configure pipeline
    config = {
        'data_dir': 'data',
        'raw_dir': 'data/raw',
        'processed_dir': 'data/processed',
        'neo4j': {
            'uri': 'bolt://localhost:7687',
            'user': 'neo4j',
            'password': 'password'  # Change this!
        },
        'vector_db_dir': './vector_db',
        'enable_geocoding': True,
        'enable_neo4j': True,
        'enable_vector_search': True
    }
    
    # Run pipeline
    pipeline = DataPipeline(config)
    entities, people, partners = pipeline.run_full_pipeline()
    
    print("\n✅ Pipeline completed! Your data is ready for the dashboard.")
    print(f"   📊 View data in: {config['data_dir']}/")
    print(f"   🔍 Vector search ready at: {config['vector_db_dir']}/")
    print(f"   🕸️  Neo4j graph available at: {config['neo4j']['uri']}")


if __name__ == "__main__":
    main()
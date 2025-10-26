"""
Vector Search System for Malaysian Government Mapping
Implements semantic search across entities, people, and partners
"""

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)


class GovernmentVectorSearch:
    """
    Semantic search system for government entities, people, and partners
    Uses sentence transformers for embeddings and ChromaDB for vector storage
    """
    
    def __init__(self, 
                 model_name: str = 'all-MiniLM-L6-v2',
                 persist_directory: str = './vector_db'):
        """
        Initialize vector search system
        
        Args:
            model_name: HuggingFace model name for embeddings
            persist_directory: Directory to persist vector database
        """
        logging.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        
        logging.info(f"Initializing ChromaDB at: {persist_directory}")
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Create collections for different entity types
        self.entities_collection = self.client.get_or_create_collection(
            name="entities",
            metadata={"description": "Government entities and organizations"}
        )
        
        self.people_collection = self.client.get_or_create_collection(
            name="people",
            metadata={"description": "Key personnel and decision makers"}
        )
        
        self.partners_collection = self.client.get_or_create_collection(
            name="partners",
            metadata={"description": "Private sector partners and contractors"}
        )
        
        logging.info("Vector search system initialized")
    
    def index_entities(self, entities_df: pd.DataFrame):
        """
        Index government entities for semantic search
        
        Args:
            entities_df: DataFrame with entity data
        """
        logging.info(f"Indexing {len(entities_df)} entities...")
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, row in entities_df.iterrows():
            # Create rich text document for embedding
            doc = self._create_entity_document(row)
            documents.append(doc)
            
            # Store metadata for retrieval
            metadata = {
                'entity_id': str(row['entity_id']),
                'name': str(row['name']),
                'entity_type': str(row['entity_type']),
                'parent_org': str(row.get('parent_org', '')),
                'policy_alignment': str(row.get('policy_alignment', '')),
                'state': str(row.get('state', '')),
                'indexed_at': datetime.now().isoformat()
            }
            metadatas.append(metadata)
            ids.append(f"entity_{row['entity_id']}")
        
        # Add to collection
        self.entities_collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        logging.info(f"✅ Indexed {len(documents)} entities")
    
    def index_people(self, people_df: pd.DataFrame):
        """
        Index people for semantic search
        
        Args:
            people_df: DataFrame with people data
        """
        logging.info(f"Indexing {len(people_df)} people...")
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, row in people_df.iterrows():
            doc = self._create_person_document(row)
            documents.append(doc)
            
            metadata = {
                'person_id': str(row['person_id']),
                'name': str(row['name']),
                'title': str(row['title']),
                'entity_id': str(row['entity_id']),
                'role_type': str(row['role_type']),
                'focus_area': str(row['focus_area']),
                'confidence_score': float(row.get('confidence_score', 0.5)),
                'email': str(row.get('email', '')),
                'indexed_at': datetime.now().isoformat()
            }
            metadatas.append(metadata)
            ids.append(f"person_{row['person_id']}")
        
        self.people_collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        logging.info(f"✅ Indexed {len(documents)} people")
    
    def index_partners(self, partners_df: pd.DataFrame):
        """
        Index private sector partners for semantic search
        
        Args:
            partners_df: DataFrame with partner data
        """
        logging.info(f"Indexing {len(partners_df)} partners...")
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, row in partners_df.iterrows():
            doc = self._create_partner_document(row)
            documents.append(doc)
            
            metadata = {
                'partner_id': str(row['partner_id']),
                'company_name': str(row['company_name']),
                'entity_id': str(row['entity_id']),
                'relationship_type': str(row['relationship_type']),
                'contract_value_rm': int(row.get('contract_value_rm', 0)),
                'contract_year': int(row.get('contract_year', 0)),
                'focus_area': str(row['focus_area']),
                'indexed_at': datetime.now().isoformat()
            }
            metadatas.append(metadata)
            ids.append(f"partner_{row['partner_id']}")
        
        self.partners_collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        logging.info(f"✅ Indexed {len(documents)} partners")
    
    def _create_entity_document(self, row: pd.Series) -> str:
        """Create rich text document for entity embedding"""
        parts = [
            f"Entity: {row['name']}",
            f"Type: {row['entity_type']}",
            f"Mandate: {row.get('mandate', 'N/A')}",
        ]
        
        if pd.notna(row.get('policy_alignment')):
            policies = row['policy_alignment'].replace('|', ', ')
            parts.append(f"Policy Alignment: {policies}")
        
        if pd.notna(row.get('parent_org')):
            parts.append(f"Reports to: {row['parent_org']}")
        
        return ". ".join(parts)
    
    def _create_person_document(self, row: pd.Series) -> str:
        """Create rich text document for person embedding"""
        parts = [
            f"Person: {row['name']}",
            f"Title: {row['title']}",
            f"Role: {row['role_type']}",
            f"Focus Area: {row['focus_area']}",
            f"Works at entity: {row['entity_id']}"
        ]
        
        return ". ".join(parts)
    
    def _create_partner_document(self, row: pd.Series) -> str:
        """Create rich text document for partner embedding"""
        parts = [
            f"Company: {row['company_name']}",
            f"Relationship: {row['relationship_type']}",
            f"Focus Area: {row['focus_area']}",
            f"Partners with: {row['entity_id']}"
        ]
        
        if row.get('contract_value_rm', 0) > 0:
            value_m = row['contract_value_rm'] / 1_000_000
            parts.append(f"Contract Value: RM {value_m:.1f}M")
        
        return ". ".join(parts)
    
    def search_entities(self, 
                       query: str, 
                       n_results: int = 10,
                       entity_type: str = None) -> List[Dict]:
        """
        Search entities using semantic similarity
        
        Args:
            query: Natural language search query
            n_results: Number of results to return
            entity_type: Filter by entity type (Ministry, Agency, Department)
        
        Returns:
            List of matching entities with metadata and relevance scores
        """
        where_filter = None
        if entity_type:
            where_filter = {"entity_type": entity_type}
        
        results = self.entities_collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter
        )
        
        return self._format_results(results)
    
    def search_people(self, 
                     query: str, 
                     n_results: int = 10,
                     role_type: str = None,
                     min_confidence: float = 0.0) -> List[Dict]:
        """
        Search people using semantic similarity
        
        Args:
            query: Natural language search query
            n_results: Number of results to return
            role_type: Filter by role type (Political, Executive, etc.)
            min_confidence: Minimum confidence score
        
        Returns:
            List of matching people with metadata and relevance scores
        """
        where_filter = {}
        if role_type:
            where_filter["role_type"] = role_type
        if min_confidence > 0:
            where_filter["confidence_score"] = {"$gte": min_confidence}
        
        results = self.people_collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter if where_filter else None
        )
        
        return self._format_results(results)
    
    def search_partners(self, 
                       query: str, 
                       n_results: int = 10,
                       relationship_type: str = None) -> List[Dict]:
        """
        Search partners using semantic similarity
        
        Args:
            query: Natural language search query
            n_results: Number of results to return
            relationship_type: Filter by relationship type
        
        Returns:
            List of matching partners with metadata and relevance scores
        """
        where_filter = None
        if relationship_type:
            where_filter = {"relationship_type": relationship_type}
        
        results = self.partners_collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter
        )
        
        return self._format_results(results)
    
    def search_all(self, query: str, n_results: int = 5) -> Dict:
        """
        Search across all collections and return combined results
        
        Args:
            query: Natural language search query
            n_results: Number of results per collection
        
        Returns:
            Dictionary with results from all collections
        """
        return {
            'entities': self.search_entities(query, n_results),
            'people': self.search_people(query, n_results),
            'partners': self.search_partners(query, n_results)
        }
    
    def _format_results(self, results: Dict) -> List[Dict]:
        """Format ChromaDB results into clean list of dicts"""
        formatted = []
        
        for idx in range(len(results['ids'][0])):
            result = {
                'id': results['ids'][0][idx],
                'metadata': results['metadatas'][0][idx],
                'document': results['documents'][0][idx],
                'distance': results['distances'][0][idx],
                'relevance_score': 1 - results['distances'][0][idx]  # Convert distance to similarity
            }
            formatted.append(result)
        
        return formatted
    
    def answer_question(self, question: str) -> Dict:
        """
        Answer natural language questions about the government ecosystem
        
        Args:
            question: Natural language question
        
        Returns:
            Dictionary with answer and supporting evidence
        """
        question_lower = question.lower()
        
        # Determine query intent
        if any(word in question_lower for word in ['who', 'person', 'people', 'minister', 'director']):
            results = self.search_people(question, n_results=5)
            category = 'people'
        
        elif any(word in question_lower for word in ['company', 'partner', 'vendor', 'contractor']):
            results = self.search_partners(question, n_results=5)
            category = 'partners'
        
        elif any(word in question_lower for word in ['ministry', 'agency', 'department', 'organization']):
            results = self.search_entities(question, n_results=5)
            category = 'entities'
        
        else:
            # Search all collections
            all_results = self.search_all(question, n_results=3)
            return {
                'question': question,
                'answer': self._generate_answer(all_results),
                'sources': all_results
            }
        
        return {
            'question': question,
            'category': category,
            'results': results,
            'answer': self._generate_simple_answer(results, category)
        }
    
    def _generate_answer(self, all_results: Dict) -> str:
        """Generate natural language answer from search results"""
        entities = all_results['entities']
        people = all_results['people']
        partners = all_results['partners']
        
        answer_parts = []
        
        if entities:
            top_entity = entities[0]['metadata']
            answer_parts.append(f"Found entity: {top_entity['name']} ({top_entity['entity_type']})")
        
        if people:
            top_person = people[0]['metadata']
            answer_parts.append(f"Key person: {top_person['name']} - {top_person['title']}")
        
        if partners:
            top_partner = partners[0]['metadata']
            answer_parts.append(f"Related partner: {top_partner['company_name']}")
        
        return ". ".join(answer_parts) if answer_parts else "No direct matches found."
    
    def _generate_simple_answer(self, results: List[Dict], category: str) -> str:
        """Generate simple answer for single-category results"""
        if not results:
            return "No matches found."
        
        top_result = results[0]
        metadata = top_result['metadata']
        relevance = top_result['relevance_score']
        
        if category == 'people':
            return f"Found: {metadata['name']}, {metadata['title']} (Relevance: {relevance:.2%})"
        elif category == 'entities':
            return f"Found: {metadata['name']}, {metadata['entity_type']} (Relevance: {relevance:.2%})"
        elif category == 'partners':
            return f"Found: {metadata['company_name']}, {metadata['relationship_type']} (Relevance: {relevance:.2%})"
        
        return "Found matches in database."
    
    def get_statistics(self) -> Dict:
        """Get statistics about indexed documents"""
        return {
            'entities': self.entities_collection.count(),
            'people': self.people_collection.count(),
            'partners': self.partners_collection.count(),
            'total': (self.entities_collection.count() + 
                     self.people_collection.count() + 
                     self.partners_collection.count())
        }


# ============================================================================
# ADVANCED SEARCH FEATURES
# ============================================================================

class AdvancedSearch(GovernmentVectorSearch):
    """Extended search capabilities with hybrid search and ranking"""
    
    def hybrid_search(self, 
                     query: str, 
                     keyword_boost: float = 0.3,
                     n_results: int = 10) -> List[Dict]:
        """
        Hybrid search combining semantic and keyword matching
        
        Args:
            query: Search query
            keyword_boost: Weight for keyword matching (0-1)
            n_results: Number of results
        
        Returns:
            Reranked results combining both methods
        """
        # Get semantic results
        semantic_results = self.search_all(query, n_results=n_results)
        
        # Simple keyword scoring (in production, use BM25 or similar)
        query_terms = set(query.lower().split())
        
        all_results = []
        for category in ['entities', 'people', 'partners']:
            for result in semantic_results[category]:
                # Calculate keyword score
                doc_terms = set(result['document'].lower().split())
                keyword_score = len(query_terms & doc_terms) / len(query_terms)
                
                # Combine scores
                semantic_score = result['relevance_score']
                hybrid_score = (1 - keyword_boost) * semantic_score + keyword_boost * keyword_score
                
                result['hybrid_score'] = hybrid_score
                result['category'] = category
                all_results.append(result)
        
        # Sort by hybrid score
        all_results.sort(key=lambda x: x['hybrid_score'], reverse=True)
        return all_results[:n_results]
    
    def find_similar_entities(self, entity_id: str, n_results: int = 5) -> List[Dict]:
        """Find entities similar to a given entity"""
        # Get the entity's document
        entity_result = self.entities_collection.get(ids=[f"entity_{entity_id}"])
        
        if not entity_result['documents']:
            return []
        
        entity_doc = entity_result['documents'][0]
        
        # Search for similar entities
        results = self.entities_collection.query(
            query_texts=[entity_doc],
            n_results=n_results + 1  # +1 to exclude self
        )
        
        formatted = self._format_results(results)
        
        # Remove the original entity from results
        return [r for r in formatted if r['id'] != f"entity_{entity_id}"]


# ============================================================================
# EXAMPLE USAGE & TESTING
# ============================================================================

def main():
    """Example usage and testing"""
    
    # Initialize vector search
    vs = GovernmentVectorSearch()
    
    # Load data
    entities_df = pd.read_csv('data/entities.csv')
    people_df = pd.read_csv('data/people.csv')
    partners_df = pd.read_csv('data/partners.csv')
    
    # Index all data
    print("Building vector search index...")
    vs.index_entities(entities_df)
    vs.index_people(people_df)
    vs.index_partners(partners_df)
    
    # Get statistics
    stats = vs.get_statistics()
    print("\n" + "="*50)
    print("Vector Search Statistics")
    print("="*50)
    print(f"Total indexed documents: {stats['total']}")
    print(f"  - Entities: {stats['entities']}")
    print(f"  - People: {stats['people']}")
    print(f"  - Partners: {stats['partners']}")
    print("="*50)
    
    # Example searches
    print("\n" + "="*50)
    print("Example Searches")
    print("="*50)
    
    # Search 1: Find entities related to AI
    print("\n1. Who oversees AI adoption in higher education?")
    results = vs.answer_question("Who oversees AI adoption in higher education?")
    print(f"Answer: {results['answer']}")
    
    # Search 2: Find digital transformation leaders
    print("\n2. Find digital transformation leaders")
    results = vs.search_people("digital transformation strategy policy", n_results=3)
    for r in results:
        meta = r['metadata']
        print(f"  - {meta['name']}: {meta['title']} (Score: {r['relevance_score']:.2%})")
    
    # Search 3: Find companies working on cybersecurity
    print("\n3. Find cybersecurity partners")
    results = vs.search_partners("cybersecurity", n_results=3)
    for r in results:
        meta = r['metadata']
        print(f"  - {meta['company_name']}: {meta['relationship_type']} (Score: {r['relevance_score']:.2%})")
    
    # Search 4: Find MyDIGITAL aligned entities
    print("\n4. Find MyDIGITAL aligned entities")
    results = vs.search_entities("MyDIGITAL digital economy blueprint", n_results=3)
    for r in results:
        meta = r['metadata']
        print(f"  - {meta['name']}: {meta['entity_type']} (Score: {r['relevance_score']:.2%})")
    
    print("\n" + "="*50)
    print("✅ Vector search system ready!")
    print("="*50)


if __name__ == "__main__":
    main()
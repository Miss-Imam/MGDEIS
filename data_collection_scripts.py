"""
Data Collection Scripts for Malaysian Government Mapping Project
Scrapes ministry websites, LinkedIn, and procurement portals
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from datetime import datetime
import logging
from typing import List, Dict
import re

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_collection.log'),
        logging.StreamHandler()
    ]
)

class GovernmentEntityScraper:
    """Scrape ministry and agency information from official websites"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.entities = []
        
    def scrape_mohe(self):
        """Scrape Ministry of Higher Education structure"""
        logging.info("Scraping MOHE website...")
        
        urls = {
            'main': 'https://www.mohe.gov.my',
            'about': 'https://www.mohe.gov.my/en/about-us',
            'organization': 'https://www.mohe.gov.my/en/about-us/organization-chart'
        }
        
        try:
            response = self.session.get(urls['organization'], headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Example extraction - adjust selectors based on actual website structure
            departments = soup.find_all('div', class_=['department', 'division', 'unit'])
            
            for dept in departments:
                entity = {
                    'entity_id': f"MOHE_{len(self.entities):03d}",
                    'name': self._clean_text(dept.find('h3').text if dept.find('h3') else ''),
                    'entity_type': 'Department',
                    'parent_org': 'MIN002',  # MOHE
                    'mandate': self._clean_text(dept.find('p').text if dept.find('p') else ''),
                    'policy_alignment': '4IR Policy',
                    'source_url': urls['organization'],
                    'scraped_at': datetime.now().isoformat(),
                    'confidence_score': 0.85
                }
                
                if entity['name']:
                    self.entities.append(entity)
                    logging.info(f"Found entity: {entity['name']}")
            
            return self.entities
            
        except Exception as e:
            logging.error(f"Error scraping MOHE: {e}")
            return []
    
    def scrape_mdec(self):
        """Scrape MDEC information"""
        logging.info("Scraping MDEC website...")
        
        urls = {
            'about': 'https://mdec.my/about-mdec',
            'programs': 'https://mdec.my/programs',
            'leadership': 'https://mdec.my/about-mdec/leadership'
        }
        
        try:
            # Scrape MDEC programs as sub-entities
            response = self.session.get(urls['programs'], headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            programs = soup.find_all('div', class_=['program-card', 'initiative'])
            
            for program in programs:
                entity = {
                    'entity_id': f"MDEC_{len(self.entities):03d}",
                    'name': self._clean_text(program.find('h2').text if program.find('h2') else ''),
                    'entity_type': 'Program',
                    'parent_org': 'AGN001',  # MDEC
                    'mandate': self._clean_text(program.find('p').text if program.find('p') else ''),
                    'policy_alignment': 'MyDIGITAL|Digital Economy Blueprint',
                    'source_url': urls['programs'],
                    'scraped_at': datetime.now().isoformat(),
                    'confidence_score': 0.90
                }
                
                if entity['name']:
                    self.entities.append(entity)
                    logging.info(f"Found entity: {entity['name']}")
            
            return self.entities
            
        except Exception as e:
            logging.error(f"Error scraping MDEC: {e}")
            return []
    
    def scrape_ministry_of_digital(self):
        """Scrape Ministry of Digital"""
        logging.info("Scraping Ministry of Digital website...")
        
        # Note: Adjust URL based on actual ministry website
        urls = {
            'main': 'https://www.digital.gov.my',  # Hypothetical
            'structure': 'https://www.digital.gov.my/organization'
        }
        
        try:
            response = self.session.get(urls['main'], headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract divisions and departments
            # This is a template - adjust based on actual structure
            divisions = soup.find_all('div', class_='division-item')
            
            for div in divisions:
                entity = {
                    'entity_id': f"DIGITAL_{len(self.entities):03d}",
                    'name': self._clean_text(div.get_text()),
                    'entity_type': 'Division',
                    'parent_org': 'MIN001',
                    'mandate': 'Digital transformation and policy',
                    'policy_alignment': 'MyDIGITAL|AI Roadmap|Cybersecurity',
                    'source_url': urls['main'],
                    'scraped_at': datetime.now().isoformat(),
                    'confidence_score': 0.80
                }
                
                if entity['name']:
                    self.entities.append(entity)
            
            return self.entities
            
        except Exception as e:
            logging.error(f"Error scraping Ministry of Digital: {e}")
            return []
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        if not text:
            return ""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def save_to_csv(self, filename='data/entities_scraped.csv'):
        """Save collected entities to CSV"""
        df = pd.DataFrame(self.entities)
        df.to_csv(filename, index=False)
        logging.info(f"Saved {len(self.entities)} entities to {filename}")
        return df


class PeopleScraper:
    """Scrape key personnel information"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.people = []
    
    def scrape_ministry_leadership(self, ministry_url: str, entity_id: str, ministry_name: str):
        """Scrape leadership from ministry website"""
        logging.info(f"Scraping leadership from {ministry_name}...")
        
        try:
            response = self.session.get(ministry_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for leadership section
            leaders = soup.find_all(['div', 'section'], class_=['leader', 'executive', 'management'])
            
            for leader in leaders:
                # Extract name
                name_elem = leader.find(['h2', 'h3', 'h4', 'strong'])
                name = self._clean_text(name_elem.text if name_elem else '')
                
                # Extract title
                title_elem = leader.find(['p', 'span'], class_=['title', 'position'])
                title = self._clean_text(title_elem.text if title_elem else '')
                
                # Extract bio/focus area
                bio_elem = leader.find('p', class_=['bio', 'description'])
                bio = self._clean_text(bio_elem.text if bio_elem else '')
                
                person = {
                    'person_id': f"P{len(self.people):04d}",
                    'name': name,
                    'title': title,
                    'entity_id': entity_id,
                    'role_type': self._classify_role(title),
                    'focus_area': self._extract_focus_area(bio, title),
                    'confidence_score': 0.85,
                    'source': f'{ministry_name} Official Website',
                    'source_url': ministry_url,
                    'scraped_at': datetime.now().isoformat(),
                    'email': self._extract_email(leader.get_text()),
                    'bio': bio[:500] if bio else ''  # Truncate bio
                }
                
                if person['name'] and person['title']:
                    self.people.append(person)
                    logging.info(f"Found person: {person['name']} - {person['title']}")
            
            return self.people
            
        except Exception as e:
            logging.error(f"Error scraping leadership: {e}")
            return []
    
    def scrape_mdec_leadership(self):
        """Scrape MDEC leadership"""
        url = 'https://mdec.my/about-mdec/leadership'
        return self.scrape_ministry_leadership(url, 'AGN001', 'MDEC')
    
    def _classify_role(self, title: str) -> str:
        """Classify role type based on title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['minister', 'deputy minister', 'yb']):
            return 'Political'
        elif any(word in title_lower for word in ['director general', 'dg', 'secretary general', 'ceo', 'chief']):
            return 'Executive'
        elif any(word in title_lower for word in ['director', 'deputy director', 'head', 'manager']):
            return 'Management'
        else:
            return 'Technical'
    
    def _extract_focus_area(self, bio: str, title: str) -> str:
        """Extract focus area from bio and title"""
        keywords = {
            'Digital Policy': ['digital', 'policy', 'strategy', 'transformation'],
            'Higher Education': ['education', 'university', 'student', 'academic'],
            'Digital Economy': ['economy', 'economic', 'business', 'industry'],
            'Technology': ['technology', 'tech', 'innovation', 'research'],
            'Cybersecurity': ['cyber', 'security', 'protection'],
            'AI & Data': ['artificial intelligence', 'ai', 'data', 'analytics'],
            'Infrastructure': ['infrastructure', 'network', 'connectivity']
        }
        
        text = (bio + ' ' + title).lower()
        
        for area, words in keywords.items():
            if any(word in text for word in words):
                return area
        
        return 'General Administration'
    
    def _extract_email(self, text: str) -> str:
        """Extract email from text"""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_pattern, text)
        return match.group(0) if match else ''
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def save_to_csv(self, filename='data/people_scraped.csv'):
        """Save collected people to CSV"""
        df = pd.DataFrame(self.people)
        df.to_csv(filename, index=False)
        logging.info(f"Saved {len(self.people)} people to {filename}")
        return df


class ProcurementScraper:
    """Scrape procurement and contract data"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.contracts = []
    
    def scrape_eperolehan(self, ministry_code: str = None):
        """
        Scrape Malaysian government e-Perolehan portal
        Note: May require authentication or specific access
        """
        logging.info("Scraping e-Perolehan portal...")
        
        base_url = 'https://www.eperolehan.gov.my'  # Adjust based on actual portal
        
        try:
            # This is a template - actual implementation depends on portal structure
            # You may need to handle authentication, pagination, etc.
            
            response = self.session.get(base_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Example: Find tender awards
            contracts = soup.find_all('div', class_=['tender-award', 'contract-item'])
            
            for contract in contracts:
                contract_data = {
                    'partner_id': f"COMP{len(self.contracts):04d}",
                    'company_name': self._extract_company_name(contract),
                    'entity_id': ministry_code or 'UNKNOWN',
                    'relationship_type': 'Service Provider',
                    'contract_value_rm': self._extract_contract_value(contract),
                    'contract_year': self._extract_year(contract),
                    'focus_area': self._extract_focus_area(contract),
                    'procurement_stage': 'Active',
                    'source': 'e-Perolehan',
                    'source_url': base_url,
                    'scraped_at': datetime.now().isoformat()
                }
                
                if contract_data['company_name']:
                    self.contracts.append(contract_data)
                    logging.info(f"Found contract: {contract_data['company_name']}")
            
            return self.contracts
            
        except Exception as e:
            logging.error(f"Error scraping procurement portal: {e}")
            return []
    
    def scrape_ministry_partners_from_reports(self, pdf_url: str, entity_id: str):
        """
        Extract partner information from annual reports or tender documents
        Note: Requires PDF parsing - use PyPDF2 or pdfplumber
        """
        logging.info(f"Extracting partners from report: {pdf_url}")
        
        # This would require PDF parsing libraries
        # Example placeholder:
        """
        import pdfplumber
        
        with pdfplumber.open(pdf_url) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                # Parse for company names, contract values, etc.
        """
        
        return []
    
    def _extract_company_name(self, element) -> str:
        """Extract company name from contract element"""
        name_elem = element.find(['h3', 'strong', 'span'], class_=['company', 'contractor'])
        return self._clean_text(name_elem.text if name_elem else '')
    
    def _extract_contract_value(self, element) -> int:
        """Extract contract value in RM"""
        value_elem = element.find(['span', 'td'], class_=['value', 'amount'])
        if value_elem:
            # Extract numbers and convert to int
            text = value_elem.text
            numbers = re.findall(r'[\d,]+', text)
            if numbers:
                return int(numbers[0].replace(',', ''))
        return 0
    
    def _extract_year(self, element) -> int:
        """Extract contract year"""
        date_elem = element.find(['span', 'td'], class_=['date', 'year'])
        if date_elem:
            years = re.findall(r'20\d{2}', date_elem.text)
            if years:
                return int(years[0])
        return datetime.now().year
    
    def _extract_focus_area(self, element) -> str:
        """Extract focus area from contract description"""
        desc_elem = element.find(['p', 'div'], class_=['description', 'scope'])
        if desc_elem:
            text = desc_elem.text.lower()
            
            keywords = {
                'Digital Infrastructure': ['infrastructure', 'network', 'server', 'cloud'],
                'Software Development': ['software', 'application', 'system', 'development'],
                'Cybersecurity': ['security', 'cyber', 'protection'],
                'AI & Analytics': ['ai', 'analytics', 'data', 'intelligence'],
                'IT Services': ['it services', 'support', 'maintenance'],
                'Consulting': ['consulting', 'advisory', 'strategy']
            }
            
            for area, words in keywords.items():
                if any(word in text for word in words):
                    return area
        
        return 'General IT Services'
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def save_to_csv(self, filename='data/partners_scraped.csv'):
        """Save collected contracts to CSV"""
        df = pd.DataFrame(self.contracts)
        df.to_csv(filename, index=False)
        logging.info(f"Saved {len(self.contracts)} contracts to {filename}")
        return df


def main():
    """Run all scrapers"""
    logging.info("="*50)
    logging.info("Starting data collection process...")
    logging.info("="*50)
    
    # Create data directory if it doesn't exist
    import os
    os.makedirs('data', exist_ok=True)
    
    # Scrape entities
    entity_scraper = GovernmentEntityScraper()
    entity_scraper.scrape_mohe()
    entity_scraper.scrape_mdec()
    entity_scraper.scrape_ministry_of_digital()
    entities_df = entity_scraper.save_to_csv()
    
    print(f"\n✅ Collected {len(entities_df)} entities")
    
    # Scrape people
    people_scraper = PeopleScraper()
    people_scraper.scrape_mdec_leadership()
    # Add more ministry scraping as needed
    people_df = people_scraper.save_to_csv()
    
    print(f"✅ Collected {len(people_df)} people")
    
    # Scrape procurement
    procurement_scraper = ProcurementScraper()
    # procurement_scraper.scrape_eperolehan()  # May need authentication
    partners_df = procurement_scraper.save_to_csv()
    
    print(f"✅ Collected {len(partners_df)} contracts/partners")
    
    logging.info("="*50)
    logging.info("Data collection complete!")
    logging.info("="*50)
    
    return entities_df, people_df, partners_df


if __name__ == "__main__":
    main()
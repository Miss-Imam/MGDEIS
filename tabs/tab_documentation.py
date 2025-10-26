"""
TAB 6: Documentation
Theme: Meta-information (recommendations, how the app was built, sources)
Subtabs: Strategic Recommendations, Methodology, References & Sources
"""

import streamlit as st
import pandas as pd


def render_documentation_tab():
    """Render Documentation with 3 subtabs"""

    st.markdown('<h4 style="text-align: center;">Recommendations, Methodology, & Citations</h4>', unsafe_allow_html=True)
    st.markdown("---")

    # Create subtabs
    doc_subtabs = st.tabs([
        "Strategic Recommendations",
        "Methodology",
        "References & Sources"
    ])

    # SUBTAB 1: Strategic Recommendations
    with doc_subtabs[0]:
        render_strategic_recommendations()

    # SUBTAB 2: Methodology
    with doc_subtabs[1]:
        render_methodology()

    # SUBTAB 3: References & Sources
    with doc_subtabs[2]:
        render_references()


# ============================================================================
# STRATEGIC RECOMMENDATIONS
# ============================================================================
def render_strategic_recommendations():
    """Render strategic recommendations for AI business plans"""

    st.markdown("<h4 style='text-align: center;'>Strategic Recommendations for AI Business Engagement</h4>", unsafe_allow_html=True)
    st.markdown("---")

    # Entry Points Table
    st.markdown("<h4 style='text-align: left;'>Entry Points for AI Business Plans</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left;'>Prioritized entry points based on active AI initiatives, partnerships, and procurements</p>", unsafe_allow_html=True)

    entry_points = pd.DataFrame({
        'Priority': [
            'HIGHEST',
            'HIGHEST',
            'STRATEGIC',
            'SECTOR-SPECIFIC',
            'REGULATORY'
        ],
        'Entity': [
            'Ministry of Digital',
            'MDEC',
            'MyDIGITAL Corporation',
            'MOHE',
            'MCMC'
        ],
        'Entry Strategy': [
            'AI@JDN chatbot enhancement, GovTech AI solutions, National AI Office coordination',
            'Malaysia Digital initiative partnerships, AI Innovation Division collaboration, cloud ecosystem expansion',
            'National AI Action Plan alignment, C4IR Malaysia innovation projects, AI governance advisory',
            'EdTech AI solutions, AI for Rakyat program delivery, research collaboration',
            'AI regulatory compliance framework, 5G + AI applications, AI ethics standards'
        ],
        'Active Initiatives': [
            'AI@JDN Chatbot (voice), National AI Office, GovTech Policy, Digital Rakyat Portal',
            'Malaysia Digital, National AI Roadmap, AI Innovation Division, RM13.91B MD Status',
            'National AI Action Plan, C4IR Malaysia (WEF), National 4IR Policy, AI governance',
            'AI for Rakyat, Malaysia Education Blueprint, Research Excellence, Learning Management',
            'AI Regulation Policy, 5G Deployment, JENDELA Phase 2, Cybersecurity AI'
        ],
        'Partnerships': [
            '12: Microsoft, Google, UNDP, telecoms',
            '9: AWS, Azure, Google Cloud, Huawei, Ericsson, Nokia',
            '7: WEF, UNDP, Bursa Malaysia, Asia School of Business',
            '3: Microsoft, Google Workspace, Universities',
            '6: Telcos, content providers, international regulators'
        ],
        'Why': [
            'Highest coordination role with 12 partnerships, active voice AI chatbot implementation',
            'Direct industry access, 9 tech partnerships, dedicated AI Innovation Division',
            'National policy architect with WEF partnership, strategic influence but limited operational scale',
            'Highest procurement activity (6 categories), strong EdTech and AI literacy focus',
            'Regulatory gateway for compliance, 5G infrastructure enabler, standards authority'
        ]
    })

    st.dataframe(entry_points, use_container_width=True, hide_index=True)
    st.markdown("---")

    # Key Decision Makers Table
    st.markdown("<h4 style='text-align: left;'>Key Decision Makers</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left;'>Critical stakeholders for AI engagement based on current roles and initiatives</p>", unsafe_allow_html=True)

    decision_makers = pd.DataFrame({
        'Name': [
            'YBrs. Ts. Dr. Fazidah binti Abu Bakar',
            'Datuk Ts. Fadzli Abdul Wahit',
            'Shakib Ahmad Shakir Jamaluddin',
            'Gopi Ganaselingam',
            'Fabian Bigar',
            'YB Tuan Gobind Singh Deo',
            'Anuar Fariz Fadzil',
            'Shamsul Izhan Abdul Majid',
            'Prof. Dr. Raha binti Abdul Rahim'
        ],
        'Position & Entity': [
            'Director General, National Digital Department (Ministry of Digital)',
            'SVP Corporate Affairs (MDEC)',
            'Deputy Secretary-General, Strategic (Ministry of Digital)',
            'SVP Industry & Ecosystem (MDEC)',
            'CEO (MyDIGITAL Corporation)',
            'Minister of Digital',
            'CEO (MDEC)',
            'CTIO (MCMC)',
            'Director BPKI (MOHE)'
        ],
        'Key AI Initiatives Managed': [
            'National AI Office, AI@JDN Chatbot, Digital Rakyat Portal, National AI Roadmap',
            'National AI Roadmap Lead, Malaysia Digital, GAIN, DE Rantau initiatives',
            'National Digital Economy Blueprint, National AI Roadmap, AI for Rakyat coordination',
            'Industry Divisions, Ecosystem Partnerships, AI Innovation collaboration',
            'National AI Action Plan, 4IR Policy Implementation, AI Nation Vision',
            'AI Policy Direction, Resilient Digital Malaysia, CyberDSA 2025',
            'Investor Engagements, Digital Economy execution, Malaysia Digital oversight',
            'AI Innovation & Technology Standards, 5G + AI applications',
            'Research & Innovation, AI R&D in higher education'
        ],
        'Engagement Priority': [
            'IMMEDIATE - Operational decisions',
            'IMMEDIATE - Roadmap implementation',
            'IMMEDIATE - Strategic coordination',
            'IMMEDIATE - Partnership facilitation',
            'HIGH - Strategic positioning',
            'HIGH - Policy approval',
            'HIGH - Investment & programs',
            'MEDIUM - Regulatory standards',
            'MEDIUM - Education sector'
        ]
    })

    st.dataframe(decision_makers, use_container_width=True, hide_index=True)
    st.markdown("---")

    # Partnership Opportunities Table
    st.markdown("<h4 style='text-align: left;'>Partnership Opportunities</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left;'>Specific areas with active demand and competitive positioning</p>", unsafe_allow_html=True)

    opportunities = pd.DataFrame({
        'Opportunity Area': [
            'Voice AI Solutions',
            'AI@JDN Chatbot Enhancement',
            'GovTech AI Integration',
            'Malaysia Digital AI Programs',
            'AI Governance & Ethics',
            'AI Education Platforms',
            '5G + Edge AI Applications',
            'AI Cloud Infrastructure',
            'AI for Public Services',
            'AI Research Collaboration'
        ],
        'Primary Entity': [
            'Ministry of Digital',
            'Ministry of Digital, JDN',
            'Ministry of Digital, NAIO',
            'MDEC',
            'MyDIGITAL, NAIO',
            'MOHE, Ministry of Digital',
            'MCMC, Ministry of Digital',
            'JDN, Ministry of Digital',
            'All Government Entities',
            'MOHE, MyDIGITAL'
        ],
        'Current Need & Competitive Position': [
            'Limited specialized voice AI vendors - LOW COMPETITION advantage',
            'Chatbot needs voice enhancement - MODERATE competition (MS/Google integration)',
            'E-government AI integration nascent - MODERATE (need gov experience)',
            'AI partners for business transformation - HIGH competition but AI-specific gap',
            'Policy frameworks exist, need implementation - LOW (ethics/transparency differentiator)',
            'AI for Rakyat requires scalable platforms - MODERATE (AI-focused EdTech limited)',
            '5G ready but AI apps limited - LOW COMPETITION (emerging area)',
            'Active government cloud procurement - HIGH (hyperscaler competition)',
            'Digital Rakyat Portal needs AI - MODERATE (public sector experience valued)',
            'Universities seek AI partnerships - LOW (knowledge transfer valued)',
        ],
        'Market Size': [
            'Large',
            'Medium',
            'Large',
            'Large',
            'Medium',
            'Large',
            'Large',
            'Large',
            'Large',
            'Medium'
        ],
        'Timeline': [
            'IMMEDIATE',
            'IMMEDIATE',
            '3-6 months',
            'IMMEDIATE',
            '3-6 months',
            '3-6 months',
            '6-12 months',
            'IMMEDIATE',
            'Ongoing',
            'Ongoing'
        ]
    })

    st.dataframe(opportunities, use_container_width=True, hide_index=True)
    st.markdown("---")

    # AI Alignment Framework Table
    st.markdown("<h4 style='text-align: left;'>AI Alignment Framework</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left;'>Critical frameworks for successful AI engagement aligned with national priorities</p>", unsafe_allow_html=True)

    ai_framework = pd.DataFrame({
        'Framework': [
            'National AI Action Plan (2021-2030)',
            'National AI Roadmap (2021-2025)',
            'Malaysia Digital Economy Blueprint',
            'National 4IR Policy',
            'AI Governance & Ethics Guidelines',
            'GovTech Policy',
            'Digital Rakyat Portal Initiative',
            'Malaysia Digital Initiative'
        ],
        'Owning Entity': [
            'MyDIGITAL Corporation',
            'Ministry of Digital, MDEC',
            'MyDIGITAL, Ministry of Digital',
            'MyDIGITAL Corporation',
            'NAIO, MyDIGITAL',
            'Ministry of Digital',
            'Ministry of Digital, JDN',
            'MDEC'
        ],
        'AI Focus Areas': [
            'National AI governance, ecosystem development, AI Nation Vision, coordinated AI strategy',
            'AI innovation, deployment, talent development, industry implementation across sectors',
            'AI-driven digital transformation by 2030, digital economy acceleration, AI adoption',
            'AI and 4IR adoption across sectors, innovation ecosystem, WEF C4IR partnership',
            'Responsible AI, ethical AI deployment, AI transparency, trust and safety frameworks',
            'AI integration in e-government services, public service automation, efficiency',
            'AI-enhanced public services, Digital inclusion, Public AI literacy and access',
            'AI-enabled business transformation, digital economy participation, AI investment'
        ],
        'Status': [
            'Active - Implementation Phase',
            'Active - 2021-2025 Period',
            'Active - Launched 2021-02-19',
            'Active - Launched 2021-07-01',
            'Active - Standards Development',
            'Active - Launched 2023',
            'Active - Ongoing Enhancement',
            'Active - Ongoing Programs'
        ],
        'Priority': [
            'CRITICAL',
            'CRITICAL',
            'CRITICAL',
            'HIGH',
            'HIGH',
            'HIGH',
            'HIGH',
            'HIGH'
        ],
        'How to Align': [
            'Demonstrate AI Nation Vision contribution, align with governance frameworks, show ecosystem impact',
            'Prove AI innovation capability, commit to talent development, support implementation targets',
            'Position as digital economy accelerator, show transformation impact, align with 2030 goals',
            'Showcase 4IR technology integration, highlight innovation, reference C4IR standards',
            'Commit to ethical AI principles, ensure transparency, implement trust frameworks',
            'Target e-government efficiency, support automation goals, enhance public services',
            'Focus on accessibility, support digital inclusion, enhance citizen experience',
            'Enable business AI adoption, facilitate digital participation, demonstrate ROI'
        ]
    })

    st.dataframe(ai_framework, use_container_width=True, hide_index=True)
    st.markdown("---")

    # Critical Success Factors
    st.markdown("<h4 style='text-align: left;'>Critical Success Factors</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left;'>Essential requirements and competitive advantages for AI partnerships</p>", unsafe_allow_html=True)

    success_factors = pd.DataFrame({
        'Category': [
            'Must-Have',
            'Must-Have',
            'Must-Have',
            'Must-Have',
            'Must-Have',
            'Competitive Edge',
            'Competitive Edge',
            'Competitive Edge',
            'Competitive Edge',
            'Red Flag',
            'Red Flag',
            'Red Flag'
        ],
        'Factor': [
            'Local Presence',
            'Government Experience',
            'AI Governance Alignment',
            'Security Clearance',
            'Bahasa Malaysia Support',
            'Voice AI Expertise',
            'Ethical AI Capabilities',
            'Integration with MS/Google',
            'Knowledge Transfer',
            'Bypassing NAIO',
            'Ignoring Local Partners',
            'Overpromising'
        ],
        'Description': [
            'Malaysian entity or strong local implementation partner required',
            'Proven track record with public sector projects and government culture',
            'Full alignment with National AI Guidelines and NAIO frameworks',
            'CyberSecurity Malaysia compliance and data localization adherence',
            'Local language support for AI inclusivity and accessibility',
            'Specialized voice solutions - currently limited competition in market',
            'Strong governance, transparency, and ethical AI implementation capability',
            'Ability to work with existing Microsoft/Google infrastructure',
            'Build local AI capabilities, talent development, and skills transfer',
            'All AI initiatives must align with and be approved by National AI Office',
            'Local partners essential for implementation, cultural fit, and long-term success',
            'Start with achievable pilots, demonstrate value before scaling commitments'
        ],
        'Impact': [
            'MANDATORY',
            'HIGH',
            'MANDATORY',
            'MANDATORY',
            'HIGH',
            'CRITICAL',
            'HIGH',
            'MEDIUM',
            'HIGH',
            'CRITICAL',
            'CRITICAL',
            'HIGH'
        ]
    })

    st.dataframe(success_factors, use_container_width=True, hide_index=True)
    st.markdown("---")

    # Recommended Phased Approach
    st.markdown("<h4 style='text-align: left;'>Recommended 3-Phase Entry Strategy</h4>", unsafe_allow_html=True)

    phased_approach = pd.DataFrame({
        'Phase & Timeline': [
            'Phase 1 (Months 1-3): Establish Credibility',
            'Phase 1 (Months 1-3): Establish Credibility',
            'Phase 1 (Months 1-3): Establish Credibility',
            'Phase 2 (Months 4-9): Scale Partnerships',
            'Phase 2 (Months 4-9): Scale Partnerships',
            'Phase 2 (Months 4-9): Scale Partnerships',
            'Phase 3 (Months 10-18): Sector Expansion',
            'Phase 3 (Months 10-18): Sector Expansion',
            'Phase 3 (Months 10-18): Sector Expansion'
        ],
        'Target': [
            'Ministry of Digital',
            'MDEC',
            'Foundational Setup',
            'MyDIGITAL',
            'MCMC',
            'Expand Existing',
            'MOHE',
            'Other Ministries',
            'Framework Agreements'
        ],
        'Key Actions': [
            'AI@JDN chatbot enhancement proposal, GovTech AI pilots',
            'Malaysia Digital initiative partnership, AI Innovation Division engagement',
            'Join tech partnership ecosystem (MS/Google co-selling), secure local partner, vendor registration',
            'National AI Action Plan alignment, C4IR Malaysia collaboration projects',
            'AI governance frameworks, 5G + AI application pilots, regulatory positioning',
            'Leverage Phase 1 success stories for expansion, scale successful pilots',
            'EdTech AI solutions, AI for Rakyat program delivery, research partnerships',
            'Cross-ministry adoption using proven track record, multi-ministry proposals',
            'Position as preferred AI vendor, negotiate long-term framework agreements'
        ],
        'Investment': [
            'Low - POCs',
            'Low - Pilots',
            'Low - Setup',
            'Medium - Implementations',
            'Medium - Strategic',
            'Medium - Scale',
            'Large - Deployments',
            'Large - Expansion',
            'Large - Contracts'
        ],
        'Success Metrics': [
            'Pilot approval, stakeholder relationships',
            'POC completion, positive feedback',
            'Vendor status, security clearance',
            'Strategic positioning, policy alignment',
            'Regulatory credibility',
            'Revenue growth, reference customers',
            'Sector penetration',
            'Government-wide adoption',
            'Framework agreement secured'
        ]
    })

    st.dataframe(phased_approach, use_container_width=True, hide_index=True)
# ============================================================================
# METHODOLOGY
# ============================================================================

def render_methodology():
    """Render methodology and research approach"""

    # Research Approach Overview
    st.markdown("<h4 style='text-align: left;'>Research Approach Overview</h4>", unsafe_allow_html=True)

    st.markdown("""
    This intelligence dashboard employs a **multi-source, triangulated research methodology** to map
    Malaysia's government digital ecosystem with focus on AI readiness and digital transformation capabilities.
""")

    st.markdown("---")

    # Data Collection Process
    st.markdown("<h4 style='text-align: left;'>Data Collection Process</h4>", unsafe_allow_html=True)

    data_collection_df = pd.DataFrame({
        'Phase': [
            'Phase 1: Entity Identification',
            'Phase 2: Personnel Mapping',
            'Phase 3: Policy Analysis',
            'Phase 4: Partnership Intelligence',
            'Phase 5: AI Alignment Assessment',
            'Phase 6: Knowledge Graph Construction'
        ],
        'Key Activities': [
            'Identify government ministries, agencies, departments; Map organizational hierarchies; Establish entity relationships; Document AI readiness indicators',
            'Identify key decision-makers (Ministers, CEOs, DGs); Verify current positions through multiple sources; Extract expertise and AI focus areas; Assign confidence scores',
            'Catalog national digital and AI policies; Map policy ownership and implementation; Identify cross-entity collaboration frameworks; Analyze AI alignment and gaps',
            'Identify government-private sector partnerships; Map vendor ecosystems and AI capabilities; Analyze procurement patterns; Document technology partnerships',
            'Evaluate AI readiness across entities; Assess AI policy alignment; Document AI initiatives and focus areas; Calculate confidence scores',
            'Model all data in Neo4j graph database; Create semantic connections; Enable graph-based querying; Validate data integrity'
        ]
    })

    st.dataframe(data_collection_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Multi-Source Triangulation
    st.markdown("<h4 style='text-align: left;'>Multi-Source Triangulation</h4>", unsafe_allow_html=True)

    st.markdown("**Source Priority Hierarchy:**")

    source_hierarchy_df = pd.DataFrame({
        'Priority': ['1', '2', '3', '4'],
        'Source Type': [
            'Primary Official Sources',
            'Verified Professional Sources',
            'Credible Media Sources',
            'Secondary Sources'
        ],
        'Description': [
            'Government websites, official press releases, policy documents',
            'LinkedIn profiles, official company websites, academic publications',
            'National newspapers, technology media, business publications',
            'Industry reports (validation only)'
        ]
    })

    st.dataframe(source_hierarchy_df, use_container_width=True, hide_index=True)

    st.markdown("**Confidence Score Requirements:**")

    confidence_df = pd.DataFrame({
        'Confidence Level': ['High (90-100%)', 'Medium (70-89%)', 'Low (50-69%)'],
        'Requirements': [
            '3+ primary sources OR 2+ official government sources',
            '2 credible sources OR 1 official + 1 verified source',
            '1 credible source OR contradicting information'
        ]
    })

    st.dataframe(confidence_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Tools & Technologies
    st.markdown("<h4 style='text-align: left;'>Tools & Technologies</h4>", unsafe_allow_html=True)

    tools_df = pd.DataFrame({
        'Category': [
            'Data Processing & Analysis',
            'Data Processing & Analysis',
            'Data Processing & Analysis',
            'Data Processing & Analysis',
            'Visualization',
            'Visualization',
            'Visualization',
            'Database & Storage',
            'Database & Storage',
            'Database & Storage',
            'Data Collection',
            'Data Collection',
            'Data Collection'
        ],
        'Tool': [
            'Python',
            'Pandas',
            'NumPy',
            'NetworkX',
            'Streamlit',
            'Plotly',
            'Plotly Graph Objects',
            'Neo4j Aura',
            'CSV Files',
            'Neo4j Cypher',
            'Web research',
            'API integration',
            'Document analysis'
        ],
        'Purpose': [
            'Data processing and analysis',
            'Data manipulation and transformation',
            'Numerical computations',
            'Graph analysis and network metrics',
            'Interactive dashboard framework',
            'Interactive charts and visualizations',
            'Custom visualizations',
            'Cloud graph database',
            'Structured data storage',
            'Graph query language',
            'Manual verification',
            'Automated data retrieval',
            'PDF parsing and extraction'
        ]
    })

    st.dataframe(tools_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Limitations
    st.markdown("<h4 style='text-align: left;'>Limitations & Caveats</h4>", unsafe_allow_html=True)

    limitations_df = pd.DataFrame({
        'Category': [
            'Data Gaps',
            'Data Gaps',
            'Data Gaps',
            'Data Gaps',
            'Methodological Constraints',
            'Methodological Constraints',
            'Methodological Constraints',
            'Methodological Constraints'
        ],
        'Limitation': [
            'Incomplete procurement data',
            'Personnel turnover',
            'Private sector information',
            'Decentralized data',
            'Verification lag',
            'Language limitations',
            'Access constraints',
            'Interpretation'
        ],
        'Description': [
            'Many contracts not publicly disclosed',
            'Political appointments change frequently',
            'Vendor relationships often confidential',
            'No single authoritative source',
            '2-4 week lag for non-critical updates',
            'Primary focus on English sources',
            'Some portals require authentication',
            'Policy alignment requires subjective assessment'
        ]
    })

    st.dataframe(limitations_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Update Schedule
    st.markdown("<h4 style='text-align: left;'>Maintenance & Update Schedule</h4>", unsafe_allow_html=True)

    update_schedule_df = pd.DataFrame({
        'Data Category': [
            'Minister/CEO Appointments',
            'National Policies',
            'Organizational Structures',
            'Partnership Data',
            'AI Alignment Data',
            'Procurement Data'
        ],
        'Update Frequency': [
            'Event-triggered + Monthly review',
            'Event-triggered + Quarterly review',
            'Quarterly review',
            'Event-triggered + Monthly review',
            'Quarterly review',
            'Monthly review'
        ]
    })

    st.dataframe(update_schedule_df, use_container_width=True, hide_index=True)


# ============================================================================
# REFERENCES & SOURCES
# ============================================================================

def render_references():
    """Render references and sources with export functionality"""

    # Primary Data Sources Overview
    st.markdown("<h4 style='text-align: left;'>Primary Data Sources Overview</h4>", unsafe_allow_html=True)

    st.markdown("""
    This dashboard aggregates data from multiple authoritative sources to provide comprehensive
    coverage of Malaysia's digital ecosystem and AI readiness. All sources verified as of October 2025.
    """)

    st.markdown("---")

    # Load sources.csv
    def load_sources():
        try:
            return pd.read_csv("data/sources.csv", dtype=str, encoding="utf-8")
        except Exception:
            return pd.DataFrame()

    sources_df = load_sources()

    # Government Portals
    st.markdown("<h4 style='text-align: left;'>Government Portals</h4>", unsafe_allow_html=True)

    govt_portals = pd.DataFrame({
        'Entity': [
            'Ministry of Higher Education (MOHE)',
            'MyDIGITAL Corporation',
            'Malaysia Digital Economy Corporation (MDEC)',
            'Ministry of Digital',
            'Malaysian Communications and Multimedia Commission (MCMC)',
            'National Digital Department (JDN)',
            'National AI Office (NAIO)',
            'CyberSecurity Malaysia',
            'Digital Nasional Berhad (DNB)'
        ],
        'Official Website': [
            'https://www.mohe.gov.my',
            'https://www.mydigital.gov.my',
            'https://mdec.my',
            'https://www.digital.gov.my',
            'https://www.mcmc.gov.my',
            'https://www.jdn.gov.my',
            'https://ai.gov.my',
            'https://www.cybersecurity.my',
            'https://www.digitalnasional.com.my'
        ],
        'Last Verified': ['Oct 2025'] * 9
    })

    st.dataframe(govt_portals, use_container_width=True, hide_index=True)
    st.markdown("---")

    # Policy Documents
    st.markdown("<h4 style='text-align: left;'>Key Policy Documents</h4>", unsafe_allow_html=True)

    policy_docs = pd.DataFrame({
        'Policy Document': [
            'Malaysia Digital Economy Blueprint (MyDIGITAL)',
            'National AI Roadmap 2021-2025',
            'National Fourth Industrial Revolution (4IR) Policy',
            'AI Governance & Ethics Guidelines',
            'Malaysia Education Blueprint 2015-2025 (Higher Education)',
            'JENDELA Phase 1 Progress Report',
            'Twelfth Malaysia Plan 2021-2025'
        ],
        'Publication Date': [
            'February 2021',
            '2021',
            'July 2021',
            '2024',
            '2015',
            '2022',
            '2021'
        ],
        'Source Entity': [
            'MyDIGITAL Corporation',
            'NAIO / MOSTI',
            'MyDIGITAL Corporation',
            'NAIO / Ministry of Digital',
            'Ministry of Higher Education',
            'MCMC',
            'Economic Planning Unit (EPU)'
        ]
    })

    st.dataframe(policy_docs, use_container_width=True, hide_index=True)
    st.markdown("---")

    # News & Media Sources
    st.markdown("<h4 style='text-align: left;'>News & Media Sources</h4>", unsafe_allow_html=True)

    news_media_df = pd.DataFrame({
        'Category': [
            'National News',
            'National News',
            'National News',
            'National News',
            'National News',
            'National News',
            'Technology & Business Media',
            'Technology & Business Media',
            'Technology & Business Media',
            'Technology & Business Media',
            'Technology & Business Media',
            'Technology & Business Media'
        ],
        'Source': [
            'The Star',
            'New Straits Times',
            'Malay Mail',
            'Bernama (National News Agency)',
            'Free Malaysia Today',
            'The Edge Markets',
            'Digital News Asia (DNA)',
            'Tech Wire Asia',
            'A+M (Marketing Interactive)',
            'Vulcan Post',
            'Soya Cincau',
            'TechNave'
        ]
    })

    st.dataframe(news_media_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Professional Networks
    st.markdown("<h4 style='text-align: left;'>Professional Networks</h4>", unsafe_allow_html=True)

    professional_networks_df = pd.DataFrame({
        'Platform': [
            'LinkedIn',
            'LinkedIn',
            'LinkedIn',
            'LinkedIn',
            'Company Websites',
            'Company Websites',
            'Company Websites',
            'Company Websites'
        ],
        'Type': [
            'Primary source for personnel verification',
            'Primary source for personnel verification',
            'Primary source for personnel verification',
            'Primary source for personnel verification',
            'Official announcements and press releases',
            'Official announcements and press releases',
            'Official announcements and press releases',
            'Official announcements and press releases'
        ],
        'Coverage': [
            'Official government agency profiles',
            'Individual professional profiles and employment history',
            'Organization updates and leadership announcements',
            'Verified credentials and expertise areas',
            'Leadership appointments and changes',
            'Partnership declarations and collaborations',
            'AI initiatives and product launches',
            'Strategic announcements'
        ]
    })

    st.dataframe(professional_networks_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # International Sources
    st.markdown("<h4 style='text-align: left;'>International & Regional Sources</h4>", unsafe_allow_html=True)

    intl_sources = pd.DataFrame({
        'Source': [
            'World Economic Forum',
            'ASEAN Secretariat',
            'International Telecommunication Union (ITU)',
            'World Bank - Digital Development',
            'OECD Digital Economy Papers',
            'GovInsider',
            'OpenGov Asia'
        ],
        'Relevance': [
            'Centre for 4IR Malaysia partnership and AI governance',
            'ASEAN AI frameworks and regional AI cooperation',
            'Global telecommunications and AI standards',
            'Digital economy and AI development reports',
            'Digital transformation and AI research',
            'Government technology and AI news',
            'Public sector AI technology coverage'
        ]
    })

    st.dataframe(intl_sources, use_container_width=True, hide_index=True)
    st.markdown("---")

    # Procurement Platforms
    st.markdown("<h4 style='text-align: left;'>Procurement & Tender Platforms</h4>", unsafe_allow_html=True)

    procurement_platforms = pd.DataFrame({
        'Platform': [
            'MyProcurement (ePerolehan)',
            'MDEC eTender',
            'Ministry of Finance Tender Portal',
            'Government Contracts Information System'
        ],
        'URL': [
            'https://www.eperolehan.com.my',
            'https://tenders.mdec.com.my',
            'https://www.treasury.gov.my',
            'Various ministry portals'
        ],
        'Coverage': [
            'Federal government procurement',
            'MDEC-specific tenders and contracts',
            'Ministry-level contracts',
            'Department and agency tenders'
        ]
    })

    st.dataframe(procurement_platforms, use_container_width=True, hide_index=True)
    st.markdown("---")

    # Export Sources
    st.markdown("<h4 style='text-align: center;'>Export Sources Data</h4>", unsafe_allow_html=True)

    if not sources_df.empty:

        csv = sources_df.to_csv(index=False)
        st.download_button(
            label="Export Sources (CSV)",
            data=csv,
            file_name="mgdeis_sources.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.markdown(f"**Total Sources:** {len(sources_df)}")
    else:
        st.info("No sources data available for export")

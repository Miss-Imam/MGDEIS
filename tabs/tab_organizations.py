"""
TAB 2: Organization Structure - FIXED VERSION
Fixes: 1) Horizontal Quick Facts, 2) Full-size Markmap diagrams
"""

import streamlit as st
import pandas as pd
import streamlit_mermaid as stmd


def render_organizations_tab(entities_df, people_df, partners_df, has_csv_data, nodes_raw, relationships_raw):
    """Render the Organization Structure tab with subtabs for each organization"""
    
    st.markdown('<h3 style="text-align: center;">Organizational Structure</h3>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Create subtabs for each organization
    org_tabs = st.tabs([
        "MOHE", 
        "MCMC", 
        "Ministry of Digital", 
        "MyDIGITAL Corp", 
        "MDEC"
    ])
    
    # ============================================================================
    # SUBTAB 1: MINISTRY OF HIGHER EDUCATION (MOHE)
    # ============================================================================
    with org_tabs[0]:
        st.markdown('<h3 style="text-align: center;">Ministry of Higher Education (MOHE)</h3>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Quick Facts - Using Streamlit columns instead of HTML
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div style="text-align: center;"><strong>Established</strong><br>March 27, 2004</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div style="text-align: center;"><strong>Budget 2025</strong><br>RM18.09B</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div style="text-align: center;"><strong>Public Universities</strong><br>20</div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div style="text-align: center;"><strong>Students</strong><br>1.2M+</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Organizational Hierarchy
        
        st.markdown('<h4 style="text-align: center;">Organizational Structure</h4>', unsafe_allow_html=True)
        st.markdown("---")
        
         # Dot Diagram
         
        mohe_dot = """
digraph {
    rankdir=TB;
    node [shape=box, style=filled, fillcolor=lightyellow];

    MOHE -> "Prime Minister's Office";
    "Prime Minister's Office" -> "Minister of Higher Education";
    "Minister of Higher Education" -> "Deputy Minister";
    "Deputy Minister" -> "Core Departments";
    "Core Departments" -> {"Higher Education Dept" "Polytechnic Education Dept" 
                           "Community College Education Dept" "Scholarship Management Dept" "Research Excellence Dept"};
    "Prime Minister's Office" -> "Secretary-General";
    "Secretary-General" -> "Supervised Institutions";
    "Supervised Institutions" -> {"20 Public Universities" "36 Polytechnics" "103 Community Colleges"};
    "Secretary-General" -> "Agencies";
    "Agencies" -> {"MQA" "PTPTN" "National Professors Council" "Malaysian Citation Centre"};
}
"""
        st.graphviz_chart(mohe_dot, use_container_width=True)

        st.markdown("---")
        st.markdown('<h4 style="text-align: left;">Breakdown Table</h4>', unsafe_allow_html=True)
        
        # Breakdown Table
        breakdown_data = pd.DataFrame({
            'Type': ['Departments', 'Public Universities', 'Polytechnics', 'Community Colleges', 'Agencies'],
            'Count': [5, 20, 36, 103, 4],
            'Oversight': ['Direct', 'Autonomous', 'Centralized', 'Centralized', 'Regulatory']
        })
        st.dataframe(breakdown_data, use_container_width=True, hide_index=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================================================
    # SUBTAB 2: MCMC
    # ============================================================================
    with org_tabs[1]:
        st.markdown('<h3 style="text-align: center;">Malaysian Communications and Multimedia Commission (MCMC)</h3>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Quick Facts - Using Streamlit columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div style="text-align: center;"><strong>Established</strong><br>November 1, 1998</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div style="text-align: center;"><strong>5G Coverage</strong><br>82.4%</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div style="text-align: center;"><strong>New Towers (JENDELA)</strong><br>382+</div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div style="text-align: center;"><strong>Active Licenses</strong><br>Multiple Telcos</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Organizational Hierarchy
        
        st.markdown('<h4 style="text-align: center;">Organizational Structure</h4>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Dot Diagram
        
        mcmc_dot = """
digraph {
    rankdir=TB;
    node [shape=box, style=filled, fillcolor=lightcyan];

    MCMC -> "Communications & Multimedia Act 1998";
    "Communications & Multimedia Act 1998" -> "Commission (5 Members)";
    "Commission (5 Members)" -> "Chief Operating Officer";
    "Chief Operating Officer" -> "Operational Divisions";
    "Operational Divisions" -> {"Telecom Division" "Broadcasting Division" "Digital Content Division"
                                "Licensing Division" "Postal Services Division" "Cybersecurity Division" "AI Innovation Division"};
}
"""
        st.graphviz_chart(mcmc_dot, use_container_width=True)
        
        st.markdown("---")
        st.markdown('<h4 style="text-align: left;">Breakdown Table</h4>', unsafe_allow_html=True)
        
        # Breakdown Table
        breakdown_data = pd.DataFrame({
            'Type': ['Divisions', 'Commission Members'],
            'Count': [7, 5],
            'Function': ['Operational', 'Governance']
        })
        st.dataframe(breakdown_data, use_container_width=True, hide_index=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================================================
    # SUBTAB 3: Ministry of Digital
    # ============================================================================
    with org_tabs[2]:
        st.markdown('<h3 style="text-align: center;">Ministry of Digital</h3>', unsafe_allow_html=True)
        st.markdown("---") 
        
        # Quick Facts - Using Streamlit columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div style="text-align: center;"><strong>Established</strong><br>December 2, 2023</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div style="text-align: center;"><strong>Departments</strong><br>8+</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div style="text-align: center;"><strong>Key Agencies</strong><br>6</div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div style="text-align: center;"><strong>Focus</strong><br>Digital Transformation</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Organizational Hierarchy
        
        st.markdown('<h4 style="text-align: center;">Organizational Structure</h4>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Dot Diagram
        
        mod_dot = """
digraph {
    rankdir=TB;
    node [shape=box, style=filled, fillcolor=lightblue];

    "Ministry of Digital" -> Cabinet -> Minister -> "Deputy Minister";
    "Deputy Minister" -> "Core Departments";
    "Core Departments" -> {"National Digital Dept (JDN)" "AI Office" "e-Govt Dept" "Data Protection Dept"
                           "Innovation Dept" "RegTech Dept" "Cybersecurity Dept" "JPDP"};
    Minister -> "Secretary-General";
    "Secretary-General" -> "Key Agencies";
    "Key Agencies" -> {"MDEC" "MyDIGITAL" "NAIO" "CSM" "DNB" "MYNIC"};
}
"""
        st.graphviz_chart(mod_dot, use_container_width=True)

        
        
        st.markdown("---")
        st.markdown('<h4 style="text-align: left;">Breakdown Table</h4>', unsafe_allow_html=True)
        
        # Breakdown Table
        breakdown_data = pd.DataFrame({
            'Type': ['Departments', 'Agencies'],
            'Count': [8, 6],
            'Oversight': ['Direct Policy', 'Implementation']
        })
        st.dataframe(breakdown_data, use_container_width=True, hide_index=True)
        
    
    # ============================================================================
    # SUBTAB 4: MyDIGITAL Corporation
    # ============================================================================
    with org_tabs[3]:
        st.markdown('<h3 style="text-align: center;">MyDIGITAL Corporation</h3>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Quick Facts - Using Streamlit columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div style="text-align: center;"><strong>Established</strong><br>September 2021</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div style="text-align: center;"><strong>Investments 2025 (Q2)</strong><br>RM29.47B</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div style="text-align: center;"><strong>Jobs Created (2024)</strong><br>48,000</div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div style="text-align: center;"><strong>Departments</strong><br>4</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Organizational Hierarchy
        
        st.markdown('<h4 style="text-align: center;">Organizational Structure</h4>', unsafe_allow_html=True)
        st.markdown("---")
        
        
        # Dot Diagram
        
        mydigital_dot = """
digraph {
    rankdir=TB;
    node [shape=box, style=filled, fillcolor=plum];

    "MyDIGITAL Corporation" -> "Board of Directors";
    "Board of Directors" -> "Chief Executive Officer";
    "Chief Executive Officer" -> "Senior Directors & Directors";
    "Senior Directors & Directors" -> "Core Departments";
    "Core Departments" -> {"Strategic Management Dept" "National 4IR Dept"
                           "Digital Economy Secretariat" "Transformation Dept"};
    "Senior Directors & Directors" -> "Agencies & Partners";
    "Agencies & Partners" -> {"MYCentre4IR" "Implementation Partners"};
}
"""
        st.graphviz_chart(mydigital_dot, use_container_width=True)
        
        st.markdown("---")
        st.markdown('<h4 style="text-align: left;">Breakdown Table</h4>', unsafe_allow_html=True)
        
        # Breakdown Table
        breakdown_data = pd.DataFrame({
            'Type': ['Departments', 'Agencies'],
            'Count': [4, 2],
            'Oversight': ['Operational', 'Implementation']
        })
        st.dataframe(breakdown_data, use_container_width=True, hide_index=True)
        

    # ============================================================================
    # SUBTAB 5: MDEC
    # ============================================================================
    with org_tabs[4]:
        st.markdown('<h3 style="text-align: center;">Malaysia Digital Economy Corporation (MDEC)</h3>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Quick Facts - Using Streamlit columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div style="text-align: center;"><strong>Established</strong><br>1996</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div style="text-align: center;"><strong>Digital GDP Target 2025</strong><br>25.5%</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div style="text-align: center;"><strong>Investments 2024</strong><br>RM163.6B</div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div style="text-align: center;"><strong>Jobs Created 2024</strong><br>48,000</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Organizational Hierarchy
        
        st.markdown('<h4 style="text-align: center;">Organizational Structure</h4>', unsafe_allow_html=True)
        st.markdown("---")
     
        
        # Dot Diagram
        
        mdec_dot = """
digraph {
    rankdir=TB;
    node [shape=box, style=filled, fillcolor=mistyrose];

    MDEC -> "Board of Directors" -> "Chief Executive Officer" -> "Senior Vice Presidents & Directors";
    "Senior Vice Presidents & Directors" -> "Core Departments";
    
    "Core Departments" -> "Digital Industry Development";
    "Digital Industry Development" -> {"Tech Industry Ecosystem" "MSC Malaysia Program" "Industry Partnership"};

    "Core Departments" -> "Talent & Innovation";
    "Talent & Innovation" -> {"Digital Skills Development" "Innovation Programs" "R&D Initiatives"};

    "Core Departments" -> "Investment Department";
    "Investment Department" -> {"Foreign Direct Investment" "Venture Capital Programs" "Funding Facilitation"};

    "Core Departments" -> "Corporate Management";
    "Corporate Management" -> {"Finance & Administration" "Human Resources" "Operations"};
}
"""
        st.graphviz_chart(mdec_dot, use_container_width=True)
        
        st.markdown("---")
        st.markdown('<h4 style="text-align: left;">Breakdown Table</h4>', unsafe_allow_html=True)
        
        # Breakdown Table
        breakdown_data = pd.DataFrame({
            'Type': ['Departments'],
            'Count': [4],
            'Oversight': ['Operational']
        })
        st.dataframe(breakdown_data, use_container_width=True, hide_index=True)

def get_dashboard_styles():
    """Return custom CSS styles for the dashboard"""
    return """
    <style>
    /* Main tab styling - full width distribution */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        padding: 0;
        width: 100%;
        display: flex;
        justify-content: space-between;
        background: #f8f9fa;
        border-radius: 8px 8px 0 0;
        border-bottom: 2px solid #e0e0e0;
    }
    
    .stTabs [data-baseweb="tab"] {
        flex: 1;
        padding: 12px 16px;
        white-space: nowrap;
        font-size: 0.95rem;
        font-weight: 500;
        text-align: center;
        border-right: 1px solid #e0e0e0;
        background: white;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:last-child {
        border-right: none;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f5f5f5;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
        color: white !important;
        font-weight: 600;
    }
    
    /* Subtab styling - full width */
    .stTabs [data-baseweb="tab-list"] button {
        flex: 1;
        font-size: 0.9rem;
        padding: 10px 12px;
        text-align: center;
    }
    
    /* Remove tab panel padding for full width */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1.5rem;
    }
    
    /* Dashboard header */
    .dashboard-header {
        background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .dashboard-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        padding: 0;
        text-align: center;
    }
    
    .dashboard-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 0.95rem;
        margin: 0.5rem 0 0 0;
        padding: 0;
        text-align: center; 
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.2rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 4px solid;
    }
    
    .metric-card.blue { border-left-color: #1976d2; }
    .metric-card.green { border-left-color: #388e3c; }
    .metric-card.orange { border-left-color: #f57c00; }
    .metric-card.yellow { border-left-color: #fbc02d; }
    .metric-card.red { border-left-color: #d32f2f; }
    
    .metric-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        color: #666;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #333;
    }
    
    /* Section cards */
    .section-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }
    
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1976d2;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e0e0e0;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .dashboard-title {
            font-size: 1.4rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
    }
    </style>
    """
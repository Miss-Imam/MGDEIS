"""
Tabs package for Malaysian Government Digital Ecosystem Dashboard
Modular 6-tab structure with subtabs
"""

from .tab_overview import render_overview_tab
from .tab_organizations import render_organizations_tab
from .tab_stakeholders import render_stakeholders_tab
from .tab_policy import render_policy_tab
from .tab_analytics import render_analytics_tab
from .tab_documentation import render_documentation_tab

__all__ = [
    'render_overview_tab',
    'render_organizations_tab',
    'render_stakeholders_tab',
    'render_policy_tab',
    'render_analytics_tab',
    'render_documentation_tab'
]
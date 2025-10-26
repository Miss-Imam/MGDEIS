"""
Diagnostic Script - Check Data Loading Issues
Run this to diagnose why your dashboard isn't loading data
"""

import os
import pandas as pd
from pathlib import Path

def diagnose_data_loading():
    """Comprehensive diagnostic check"""
    
    print("="*70)
    print("MALAYSIAN GOVT DASHBOARD - DATA LOADING DIAGNOSTIC")
    print("="*70)
    print()
    
    # Check 1: Current directory
    print("📁 CHECK 1: Current Working Directory")
    print(f"   Location: {os.getcwd()}")
    print()
    
    # Check 2: List all CSV files in current directory
    print("📄 CHECK 2: CSV Files in Current Directory")
    csv_files = list(Path('.').glob('*.csv'))
    if csv_files:
        for csv_file in csv_files:
            size = os.path.getsize(csv_file)
            print(f"   ✅ {csv_file.name} ({size:,} bytes)")
    else:
        print("   ❌ No CSV files found in current directory!")
    print()
    
    # Check 3: Required CSV files
    print("📋 CHECK 3: Required CSV Files Status")
    required_files = [
        'nodes.csv',
        'relationships.csv',
        'people_intelligence.csv',
        'partnership_network.csv',
        'procurement_analysis.csv',
        'vendor_ecosystem_map.csv',
        'voice_ai_alignment.csv',
        'entity_policy_alignment.csv',
        'summary.csv'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   ✅ {file} - {size:,} bytes")
        else:
            print(f"   ❌ {file} - NOT FOUND")
    print()
    
    # Check 4: Try to load critical files
    print("🔬 CHECK 4: Data Loading Test")
    
    # Try nodes.csv
    if os.path.exists('nodes.csv'):
        try:
            nodes_df = pd.read_csv('nodes.csv')
            print(f"   ✅ nodes.csv loaded: {len(nodes_df)} rows, {len(nodes_df.columns)} columns")
            print(f"      Columns: {', '.join(nodes_df.columns.tolist())}")
            print(f"      Types: {nodes_df['type'].value_counts().to_dict() if 'type' in nodes_df.columns else 'No type column'}")
        except Exception as e:
            print(f"   ❌ nodes.csv FAILED to load: {str(e)}")
    else:
        print(f"   ❌ nodes.csv not found")
    print()
    
    # Try relationships.csv
    if os.path.exists('relationships.csv'):
        try:
            rels_df = pd.read_csv('relationships.csv')
            print(f"   ✅ relationships.csv loaded: {len(rels_df)} rows, {len(rels_df.columns)} columns")
            print(f"      Columns: {', '.join(rels_df.columns.tolist())}")
        except Exception as e:
            print(f"   ❌ relationships.csv FAILED to load: {str(e)}")
    else:
        print(f"   ❌ relationships.csv not found")
    print()
    
    # Try people_intelligence.csv
    if os.path.exists('people_intelligence.csv'):
        try:
            people_df = pd.read_csv('people_intelligence.csv')
            print(f"   ✅ people_intelligence.csv loaded: {len(people_df)} rows, {len(people_df.columns)} columns")
            print(f"      Columns: {', '.join(people_df.columns.tolist())}")
        except Exception as e:
            print(f"   ❌ people_intelligence.csv FAILED to load: {str(e)}")
    else:
        print(f"   ⚠️  people_intelligence.csv not found (optional)")
    print()
    
    # Try partnership_network.csv
    if os.path.exists('partnership_network.csv'):
        try:
            partners_df = pd.read_csv('partnership_network.csv')
            print(f"   ✅ partnership_network.csv loaded: {len(partners_df)} rows, {len(partners_df.columns)} columns")
            print(f"      Columns: {', '.join(partners_df.columns.tolist())}")
        except Exception as e:
            print(f"   ❌ partnership_network.csv FAILED to load: {str(e)}")
    else:
        print(f"   ⚠️  partnership_network.csv not found (optional)")
    print()
    
    # Check 5: Test the actual data_loader function
    print("🧪 CHECK 5: Testing data_loader.py")
    try:
        from utils.data_loader import load_data_from_graph
        entities_df, people_df, partners_df, has_csv_data = load_data_from_graph()
        
        print(f"   ✅ load_data_from_graph() executed successfully")
        print(f"      has_csv_data: {has_csv_data}")
        print(f"      entities_df: {len(entities_df)} rows")
        print(f"      people_df: {len(people_df)} rows")
        print(f"      partners_df: {len(partners_df)} rows")
        
        if len(entities_df) > 0:
            print(f"      Sample entity: {entities_df.iloc[0]['name'] if 'name' in entities_df.columns else 'N/A'}")
        
    except Exception as e:
        print(f"   ❌ data_loader FAILED: {str(e)}")
        import traceback
        print(traceback.format_exc())
    print()
    
    # Check 6: Directory structure
    print("📂 CHECK 6: Directory Structure")
    for root, dirs, files in os.walk('.'):
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files[:10]:  # Limit to first 10 files per directory
            print(f"{subindent}{file}")
        if len(files) > 10:
            print(f"{subindent}... and {len(files) - 10} more files")
    print()
    
    # Final recommendation
    print("="*70)
    print("🎯 RECOMMENDATIONS")
    print("="*70)
    
    # Count found vs missing
    found_files = [f for f in required_files if os.path.exists(f)]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if len(found_files) == 0:
        print("""
❌ NO CSV FILES FOUND!

SOLUTION:
1. Make sure you're running the dashboard from the correct directory
2. Your CSV files should be in the SAME folder as dashboard.py
3. Run this command from where dashboard.py is located:
   
   cd /path/to/your/project
   python diagnose_data.py
   streamlit run dashboard.py

4. If CSV files are in a different location, either:
   - Move them to the current directory, OR
   - Update the paths in data_loader.py
""")
    
    elif 'nodes.csv' not in found_files:
        print("""
❌ CRITICAL: nodes.csv NOT FOUND!

This is the main data file. Without it, the dashboard cannot work.

SOLUTION:
Place nodes.csv in the same directory as dashboard.py
""")
    
    elif len(found_files) < len(required_files):
        print(f"""
⚠️  PARTIAL DATA FOUND: {len(found_files)}/{len(required_files)} files

Missing files:
{chr(10).join(f'   - {f}' for f in missing_files)}

SOLUTION:
Add the missing CSV files to enable full dashboard functionality.
The dashboard will work with partial data, but some features will be limited.
""")
    
    else:
        print("""
✅ ALL CSV FILES FOUND!

If the dashboard still shows zeros, check:
1. CSV files have actual data (not empty)
2. Column names match expected format
3. Run: streamlit run dashboard.py --logger.level=debug
""")
    
    print("="*70)


if __name__ == "__main__":
    diagnose_data_loading()
with open('app.py', 'r') as f:
    content = f.read()

# Find and replace the CSS section
css_start = '# Custom CSS - Base styles for both modes'
if css_start in content:
    # Find from css_start to the next section
    import re
    pattern = r'# Custom CSS - Base styles for both modes.*?if st\.session_state\.theme_mode == \'dark\':'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        # Replace with simpler CSS
        simple_css = '''# Custom CSS - Base styles
st.markdown("""
<style>
    /* Base styles that work in both themes */
    .main-header { 
        font-size: 2.5rem; 
        text-align: center; 
        margin-bottom: 1rem; 
        font-weight: bold;
    }
    .sub-header { 
        font-size: 1.2rem; 
        text-align: center; 
        margin-bottom: 2rem; 
        color: #666666;
    }
    .risk-high {
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #DC2626;
        background-color: #FEF2F2;
        margin: 10px 0;
    }
    .risk-medium {
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #D97706;
        background-color: #FEF3C7;
        margin: 10px 0;
    }
    .risk-low {
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #059669;
        background-color: #D1FAE5;
        margin: 10px 0;
    }
    .metric-card {
        padding: 15px;
        border-radius: 8px;
        background-color: #F3F4F6;
        text-align: center;
        border: 1px solid #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)
'''
        
        # Replace the matched CSS section
        content = content.replace(match.group(0), simple_css + '\nif st.session_state.theme_mode == \'dark\':')
        print("Simplified CSS (no emojis)")
    else:
        print("Could not find CSS pattern to replace")

with open('app.py', 'w') as f:
    f.write(content)

with open('app.py', 'r') as f:
    content = f.read()

# Find the exact dark mode CSS block
import re

# Look for the dark mode section
pattern = r"(if st\.session_state\.theme_mode == 'dark':\s*st\.markdown\(\"\"\")(.*?)(\"\"\", unsafe_allow_html=True)"
match = re.search(pattern, content, re.DOTALL)

if match:
    before = match.group(1)
    css_content = match.group(2)
    after = match.group(3)
    
    # Add input styling to the existing CSS
    input_fixes = '''
    /* Fix input fields for dark mode */
    input, textarea, [data-baseweb="input"] input {
        background-color: #2a2a2a !important;
        color: #e0e0e0 !important;
        border-color: #444444 !important;
    }
    
    /* Fix number inputs specifically */
    div[data-testid="stNumberInput"] input,
    div[data-testid="stNumberInputContainer"] input {
        background-color: #2a2a2a !important;
        color: #e0e0e0 !important;
        border: 1px solid #444444 !important;
    }
    
    /* Fix slider components */
    div[data-testid="stSlider"] > div {
        background-color: #2a2a2a !important;
    }
    
    /* Fix labels in dark mode */
    label, p, span, div {
        color: #e0e0e0 !important;
    }
    
    /* Fix metric values */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #e0e0e0 !important;
    }
    '''
    
    # Combine existing CSS with new fixes
    new_css = css_content + input_fixes
    
    # Replace in content
    new_section = before + new_css + after
    content = content.replace(match.group(0), new_section)
    
    print("✓ Added input field fixes to dark mode CSS")
else:
    print("✗ Could not find dark mode CSS pattern")
    # Try alternative pattern
    alt_pattern = r'st\.session_state\.theme_mode == \"dark\"'
    if re.search(alt_pattern, content):
        print("Found alternative pattern, trying different approach...")
        
        # Add a new dark mode CSS section
        new_dark_css = '''
if st.session_state.theme_mode == 'dark':
    st.markdown("""
    <style>
    /* Dark mode input fixes */
    input, textarea, select, [data-baseweb="input"] {
        background-color: #2a2a2a !important;
        color: #e0e0e0 !important;
        border-color: #444444 !important;
    }
    
    .stNumberInput input, .stSlider div {
        background-color: #2a2a2a !important;
        color: #e0e0e0 !important;
    }
    
    label, p, div, span {
        color: #e0e0e0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
'''
        
        # Find where to insert (after theme mode check)
        insert_point = "if st.session_state.theme_mode == 'dark':"
        if insert_point in content:
            # Get everything after this point
            parts = content.split(insert_point, 1)
            if len(parts) == 2:
                content = parts[0] + new_dark_css + parts[1]
                print("✓ Added new dark mode CSS section")

with open('app.py', 'w') as f:
    f.write(content)

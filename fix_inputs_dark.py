import re

with open('app.py', 'r') as f:
    content = f.read()

# Add CSS to fix input backgrounds in dark mode
# Find the dark mode CSS section
dark_css_pattern = r'if st\.session_state\.theme_mode == \'dark\':.*?st\.markdown\("""'
match = re.search(dark_css_pattern, content, re.DOTALL)

if match:
    # Add input styling to dark mode CSS
    input_styles = '''
    /* Fix input fields for dark mode */
    div[data-baseweb="input"] input,
    div[data-baseweb="input"] textarea,
    div[data-baseweb="select"] div,
    div[data-baseweb="slider"] div {
        background-color: #2a2a2a !important;
        color: #e0e0e0 !important;
        border-color: #444444 !important;
    }
    
    /* Fix input labels */
    label, .stNumberInput label, .stSlider label {
        color: #e0e0e0 !important;
    }
    
    /* Fix select dropdown */
    div[role="listbox"] {
        background-color: #2a2a2a !important;
        color: #e0e0e0 !important;
    }
    
    /* Fix metric cards */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #e0e0e0 !important;
    }
    '''
    
    # Insert input styles into dark mode CSS
    old_dark_css = match.group(0)
    new_dark_css = old_dark_css.replace(
        'st.markdown("""',
        f'st.markdown("""{input_styles}'
    )
    
    content = content.replace(old_dark_css, new_dark_css)
    print("Added input field styling to dark mode")
else:
    print("Could not find dark mode CSS section")

with open('app.py', 'w') as f:
    f.write(content)

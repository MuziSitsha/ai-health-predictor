with open('app.py', 'r') as f:
    content = f.read()

# Add CSS at the beginning of the app (right after imports)
css_to_add = '''
# ===== THEME CSS =====
# Apply CSS based on theme
if st.session_state.get("theme_mode", "light") == "dark":
    st.markdown("""
    <style>
    /* DARK THEME - FIXES FOR INPUT BACKGROUNDS */
    
    /* 1. Fix the entire app background */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #0E1117 !important;
    }
    
    /* 2. Fix sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1E1E1E !important;
    }
    
    /* 3. Fix ALL text elements */
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: #e0e0e0 !important;
    }
    
    /* 4. Fix INPUT FIELDS - This fixes the white background issue */
    input, textarea, select {
        background-color: #2a2a2a !important;
        color: #FFFFFF !important;
        border: 1px solid #444444 !important;
    }
    
    /* 5. Fix Streamlit-specific input components */
    .stNumberInput input,
    div[data-testid="stNumberInputContainer"] input,
    input[type="number"] {
        background-color: #2a2a2a !important;
        color: #FFFFFF !important;
        border: 1px solid #444444 !important;
    }
    
    /* 6. Fix sliders */
    .stSlider > div,
    div[data-testid="stSlider"] > div {
        background-color: #2a2a2a !important;
    }
    
    /* 7. Fix metric displays */
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"],
    [data-testid="stMetricDelta"] {
        color: #e0e0e0 !important;
    }
    
    /* 8. Fix buttons */
    .stButton > button {
        background-color: #FF4B4B !important;
        color: white !important;
        border: none !important;
    }
    
    /* 9. Fix containers and cards */
    .risk-high, .risk-medium, .risk-low,
    .metric-card, [data-testid="stExpander"] {
        background-color: #2a2a2a !important;
        color: #e0e0e0 !important;
        border-color: #444444 !important;
    }
    
    /* 10. Fix Plotly chart backgrounds */
    .js-plotly-plot, .plotly, .plot-container {
        background-color: #242424 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Light theme CSS (minimal)
else:
    st.markdown("""
    <style>
    /* Light theme - ensure proper contrast */
    .stNumberInput input, .stSlider div {
        background-color: white !important;
        color: #31333F !important;
    }
    </style>
    """, unsafe_allow_html=True)
'''

# Find where to insert (right after the create_risk_gauge function ends)
if 'def create_risk_gauge(' in content:
    # Find the end of the function
    lines = content.split('\\n')
    insert_index = -1
    in_function = False
    indent_level = 0
    
    for i, line in enumerate(lines):
        if 'def create_risk_gauge(' in line:
            in_function = True
            # Get initial indent
            indent_level = len(line) - len(line.lstrip())
        elif in_function and line.strip() == '':
            continue
        elif in_function and len(line) - len(line.lstrip()) <= indent_level and line.strip() != '':
            # Function ended
            insert_index = i
            break
    
    if insert_index != -1:
        # Insert CSS after the function
        new_lines = lines[:insert_index] + [''] + css_to_add.split('\\n') + lines[insert_index:]
        content = '\\n'.join(new_lines)
        print("✓ Added CSS after create_risk_gauge function")
    else:
        # Insert at the beginning of main app
        if 'st.set_page_config' in content:
            parts = content.split('st.set_page_config', 1)
            if len(parts) == 2:
                # Find the end of set_page_config
                config_end = parts[1].find(')') + 1
                before = parts[0] + 'st.set_page_config' + parts[1][:config_end]
                after = parts[1][config_end:]
                content = before + '\\n' + css_to_add + after
                print("✓ Added CSS after page config")
else:
    print("Could not find create_risk_gauge function")

with open('app.py', 'w') as f:
    f.write(content)

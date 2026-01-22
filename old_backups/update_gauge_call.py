import re

with open('app.py', 'r') as f:
    content = f.read()

# Find and replace the old gauge creation with theme-aware version
# Look for patterns like: fig_gauge = go.Figure(go.Indicator
pattern1 = r'fig_gauge = go\.Figure\(go\.Indicator'
pattern2 = r'fig = go\.Figure\(go\.Indicator.*?probability'

if re.search(pattern1, content, re.DOTALL) or re.search(pattern2, content, re.DOTALL):
    # Replace with theme-aware call
    new_call = '''fig_gauge = create_risk_gauge(st.session_state.current_proba, st.session_state.theme_mode)'''
    
    # Replace the pattern
    content = re.sub(pattern1, new_call, content, flags=re.DOTALL)
    content = re.sub(pattern2, new_call, content, flags=re.DOTALL)
    
    print("✓ Updated gauge creation to use theme-aware function")
else:
    print("✗ Could not find gauge creation pattern")
    
    # Try to find where probability is used in visualization
    if 'st.session_state.current_proba' in content:
        # Find the visualization section
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'st.plotly_chart' in line and 'fig_gauge' in line:
                # Add the theme-aware creation before this line
                new_line = '        fig_gauge = create_risk_gauge(st.session_state.current_proba, st.session_state.theme_mode)'
                lines.insert(i, new_line)
                content = '\n'.join(lines)
                print("✓ Added theme-aware gauge creation before plotly_chart")
                break

with open('app.py', 'w') as f:
    f.write(content)

import re

with open('app.py', 'r') as f:
    content = f.read()

# Function to create theme-aware Plotly chart
plotly_fix = '''
def create_risk_gauge(probability, current_theme):
    """Create risk gauge chart that adapts to theme"""
    import plotly.graph_objects as go
    
    # Set colors based on theme
    if current_theme == "dark":
        bg_color = "#1a1a1a"
        text_color = "#e0e0e0"
        plot_bgcolor = "#242424"
        paper_bgcolor = "#242424"
        gauge_bg = "#2a2a2a"
        needle_color = "#ff6b6b"
    else:
        bg_color = "#FFFFFF"
        text_color = "#31333F"
        plot_bgcolor = "#F0F2F6"
        paper_bgcolor = "#FFFFFF"
        gauge_bg = "#F8F9FA"
        needle_color = "#FF4B4B"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,
        domain={"x": [0, 1], "y": [0, 1]},
        title={
            "text": "Risk Level",
            "font": {"size": 20, "color": text_color}
        },
        number={
            "font": {"size": 40, "color": text_color},
            "suffix": "%"
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": text_color,
                "tickfont": {"color": text_color}
            },
            "bar": {"color": needle_color},
            "bgcolor": gauge_bg,
            "borderwidth": 2,
            "bordercolor": text_color,
            "steps": [
                {"range": [0, 30], "color": "#10B981"},
                {"range": [30, 70], "color": "#F59E0B"},
                {"range": [70, 100], "color": "#EF4444"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": probability * 100
            }
        }
    ))
    
    # Update layout for theme
    fig.update_layout(
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor,
        font={"color": text_color},
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig
'''

# Find where to add this function (after imports)
if 'import plotly.graph_objects as go' in content:
    # Add function right after the import
    content = content.replace(
        'import plotly.graph_objects as go',
        'import plotly.graph_objects as go\n\n' + plotly_fix
    )
    print("Added create_risk_gauge function")

# Now find and replace the existing Plotly chart creation
# Look for go.Figure(go.Indicator pattern
pattern = r'fig = go\.Figure\(go\.Indicator\(.*?st\.plotly_chart\(fig'
match = re.search(pattern, content, re.DOTALL)

if match:
    # Replace with new call to our function
    replacement = '''fig = create_risk_gauge(st.session_state.current_proba, st.session_state.theme_mode)
        st.plotly_chart(fig'''
    
    content = content.replace(match.group(0), replacement)
    print("Replaced Plotly chart with theme-aware version")
else:
    print("Could not find Plotly chart pattern, will try different pattern")

with open('app.py', 'w') as f:
    f.write(content)

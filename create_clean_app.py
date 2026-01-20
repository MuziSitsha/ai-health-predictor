# First, get your original app_clean.py
with open('app_clean.py', 'r') as f:
    original_app = f.read()

# Now add the theme-aware create_risk_gauge function
theme_aware_function = '''
def create_risk_gauge(probability, current_theme):
    """Create risk gauge chart that adapts to theme"""
    import plotly.graph_objects as go
    
    # Set colors based on theme
    if current_theme == "dark":
        text_color = "#e0e0e0"
        plot_bgcolor = "#242424"
        paper_bgcolor = "#242424"
        gauge_bg = "#2a2a2a"
        needle_color = "#ff6b6b"
    else:
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
    
    fig.update_layout(
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor,
        font={"color": text_color},
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig
'''

# Add the function to the original app
# Find where to add it (after plotly import)
if 'import plotly.graph_objects as go' in original_app:
    new_app = original_app.replace(
        'import plotly.graph_objects as go',
        'import plotly.graph_objects as go\n' + theme_aware_function
    )
    print("✓ Added create_risk_gauge function to original app")
else:
    new_app = original_app

# Now update the gauge creation in the app
# Find where fig_gauge is created with go.Figure
import re
pattern = r'fig_gauge = go\.Figure\(go\.Indicator\(.*?\)\)'
if re.search(pattern, new_app, re.DOTALL):
    new_app = re.sub(
        pattern,
        'fig_gauge = create_risk_gauge(st.session_state.current_proba, st.session_state.theme_mode)',
        new_app,
        flags=re.DOTALL
    )
    print("✓ Updated gauge creation to use theme-aware function")

with open('app.py', 'w') as f:
    f.write(new_app)

with open('app.py', 'r') as f:
    content = f.read()

# Add the theme-aware create_risk_gauge function after imports
new_function = '''
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

# Find where to add it (after imports)
import_line = "import plotly.graph_objects as go"
if import_line in content:
    # Add function right after the import
    content = content.replace(
        import_line,
        import_line + new_function
    )
    print("✓ Added create_risk_gauge function after plotly import")
else:
    # Try to add after other plotly import
    if 'import plotly.express as px' in content:
        content = content.replace(
            'import plotly.express as px',
            'import plotly.express as px' + new_function
        )
        print("✓ Added create_risk_gauge function after plotly express import")
    else:
        # Add at the end of imports
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                continue
            else:
                # Insert before first non-import line
                lines.insert(i, new_function)
                content = '\n'.join(lines)
                print("✓ Added create_risk_gauge function after imports")
                break

with open('app.py', 'w') as f:
    f.write(content)

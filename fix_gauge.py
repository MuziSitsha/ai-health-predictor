import re

# Read the original file
with open('app.py', 'r') as file:
    content = file.read()

# Find and replace the gauge code
old_gauge_pattern = r'''with viz_col1:
    # Risk gauge
    fig_gauge = go\.Figure\(go\.Indicator\(
        mode = "gauge\+number",
        value = risk_percentage,
        title = \{"text": "Risk Gauge"\},
        domain = \{"x": \[0, 1\], "y": \[0, 1\]\},
        gauge = \{
            "axis": \{"range": \[0, 100\]\},
            "bar": \{"color": bar_color\},
            "steps": \[
                \{"range": \[0, 30\], "color": "#D1FAE5"\},
                \{"range": \[30, 70\], "color": "#FEF3C7"\},
                \{"range": \[70, 100\], "color": "#FEE2E2"\}
            \],
            "threshold": \{
                "line": \{"color": "black", "width": 4\},
                "thickness": 0\.75,
                "value": risk_percentage
            \}
        \}
    \)\)
    fig_gauge\.update_layout\(height=300\)
    st\.plotly_chart\(fig_gauge, use_container_width=True\)'''

new_gauge_code = '''with viz_col1:
    # Risk gauge with centered number
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_percentage,
        title={'text': "Diabetes Risk Gauge", 'font': {'size': 20}},
        domain={'x': [0, 1], 'y': [0, 1]},
        number={
            'font': {'size': 60, 'color': bar_color, 'family': "Arial"},
            'prefix': '',
            'suffix': '%'
        },
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "gray"},
            'bar': {'color': bar_color, 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': '#D1FAE5'},
                {'range': [30, 70], 'color': '#FEF3C7'},
                {'range': [70, 100], 'color': '#FEE2E2'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.8,
                'value': risk_percentage
            }
        }
    ))
    
    fig_gauge.update_layout(
        height=350,
        margin=dict(t=50, b=10, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "darkblue", 'family': "Arial"}
    )
    st.plotly_chart(fig_gauge, use_container_width=True)'''

# Replace the gauge code
if old_gauge_pattern in content:
    content = content.replace(old_gauge_pattern, new_gauge_code)
    print("✓ Gauge code replaced successfully")
else:
    print("⚠ Could not find exact gauge pattern. Trying alternative search...")
    # Try a simpler search
    import re
    gauge_section = re.search(r'with viz_col1:.*?st\.plotly_chart\(fig_gauge, use_container_width=True\)', content, re.DOTALL)
    if gauge_section:
        content = content.replace(gauge_section.group(0), new_gauge_code)
        print("✓ Gauge code replaced using regex search")
    else:
        print("✗ Could not find gauge section")

# Write the updated content back
with open('app.py', 'w') as file:
    file.write(content)
    
print("✓ Updated app.py saved")

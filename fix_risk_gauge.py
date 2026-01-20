with open('app.py', 'r') as f:
    lines = f.readlines()

# Find and fix the create_risk_gauge function
new_lines = []
in_function = False
function_fixed = False

for i, line in enumerate(lines):
    if 'def create_risk_gauge(' in line:
        in_function = True
        new_lines.append(line)
    elif in_function and not function_fixed:
        # Check if this line has the error
        if 'fig = create_risk_gauge(' in line:
            # Replace with correct code
            new_lines.append('    fig = go.Figure(go.Indicator(\n')
            new_lines.append('        mode="gauge+number",\n')
            new_lines.append('        value=probability * 100,\n')
            new_lines.append('        domain={"x": [0, 1], "y": [0, 1]},\n')
            new_lines.append('        title={\n')
            new_lines.append('            "text": "Risk Level",\n')
            new_lines.append('            "font": {"size": 20, "color": text_color}\n')
            new_lines.append('        },\n')
            new_lines.append('        number={\n')
            new_lines.append('            "font": {"size": 40, "color": text_color},\n')
            new_lines.append('            "suffix": "%"\n')
            new_lines.append('        },\n')
            new_lines.append('        gauge={\n')
            new_lines.append('            "axis": {\n')
            new_lines.append('                "range": [0, 100],\n')
            new_lines.append('                "tickwidth": 1,\n')
            new_lines.append('                "tickcolor": text_color,\n')
            new_lines.append('                "tickfont": {"color": text_color}\n')
            new_lines.append('            },\n')
            new_lines.append('            "bar": {"color": needle_color},\n')
            new_lines.append('            "bgcolor": gauge_bg,\n')
            new_lines.append('            "borderwidth": 2,\n')
            new_lines.append('            "bordercolor": text_color,\n')
            new_lines.append('            "steps": [\n')
            new_lines.append('                {"range": [0, 30], "color": "#10B981"},\n')
            new_lines.append('                {"range": [30, 70], "color": "#F59E0B"},\n')
            new_lines.append('                {"range": [70, 100], "color": "#EF4444"}\n')
            new_lines.append('            ],\n')
            new_lines.append('            "threshold": {\n')
            new_lines.append('                "line": {"color": "red", "width": 4},\n')
            new_lines.append('                "thickness": 0.75,\n')
            new_lines.append('                "value": probability * 100\n')
            new_lines.append('            }\n')
            new_lines.append('        }\n')
            new_lines.append('    ))\n')
            new_lines.append('    \n')
            new_lines.append('    # Update layout for theme\n')
            new_lines.append('    fig.update_layout(\n')
            new_lines.append('        paper_bgcolor=paper_bgcolor,\n')
            new_lines.append('        plot_bgcolor=plot_bgcolor,\n')
            new_lines.append('        font={"color": text_color},\n')
            new_lines.append('        height=300,\n')
            new_lines.append('        margin=dict(l=20, r=20, t=50, b=20)\n')
            new_lines.append('    )\n')
            new_lines.append('    \n')
            new_lines.append('    return fig\n')
            function_fixed = True
            in_function = False
        elif 'st.plotly_chart(fig_gauge' in line:
            # This is outside the function, skip
            new_lines.append(line)
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open('app.py', 'w') as f:
    f.writelines(new_lines)

print("✓ Fixed create_risk_gauge function")

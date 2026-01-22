with open('app.py', 'r') as file:
    lines = file.readlines()

new_lines = []
i = 0
in_viz_col2 = False
viz_col2_indent_level = 0

while i < len(lines):
    line = lines[i]
    
    # Fix 1: Handle the button logic - it should be INSIDE the sidebar block (indented)
    if line.strip() == 'predict_button = st.sidebar.button("Predict Diabetes Risk", type="primary", use_container_width=True)':
        # This is inside the sidebar block, so it should be indented
        # Find the current indentation level
        indent = len(line) - len(line.lstrip())
        new_lines.append(line)
        i += 1
        
        # Skip the next empty line if present
        if i < len(lines) and lines[i].strip() == '':
            i += 1
        
        # Now add the button logic WITH PROPER INDENTATION
        if i < len(lines) and '# Check if button was clicked' in lines[i]:
            # Skip the incorrectly placed button logic (we'll add it properly later)
            while i < len(lines) and 'pass' not in lines[i]:
                i += 1
            i += 1  # Skip the pass line
            continue
    
    # Fix 2: Add button logic in the correct place (after function definition)
    if 'def make_prediction(features_array):' in line:
        # Add the function
        new_lines.append(line)
        i += 1
        
        # Add the entire function
        while i < len(lines) and lines[i].strip() != '':
            new_lines.append(lines[i])
            i += 1
        
        # Now add properly indented button logic
        indent = '    '  # 4 spaces for sidebar block
        new_lines.append('')
        new_lines.append(indent + '# Check if button was clicked')
        new_lines.append(indent + 'if predict_button:')
        new_lines.append(indent + '    st.session_state.current_prediction, st.session_state.current_proba = make_prediction(st.session_state.current_features)')
        new_lines.append(indent + '    st.session_state.prediction_made = True')
        new_lines.append(indent + 'elif st.session_state.prediction_made and st.session_state.current_prediction is not None:')
        new_lines.append(indent + '    # Use cached prediction - do nothing')
        new_lines.append(indent + '    pass')
        new_lines.append('')
        continue
    
    # Fix 3: Handle the with statement indentation error (line 651)
    if 'with viz_col2:' in line and i > 0:
        # Check if this is properly indented
        prev_indent = len(new_lines[-1]) - len(new_lines[-1].lstrip()) if new_lines else 0
        current_indent = len(line) - len(line.lstrip())
        
        if current_indent < prev_indent:
            # Need to fix indentation
            line = ' ' * prev_indent + line.lstrip()
        
        new_lines.append(line)
        i += 1
        continue
    
    new_lines.append(line)
    i += 1

# Write back
with open('app.py', 'w') as file:
    file.writelines(new_lines)

print("✓ Complete fix applied")

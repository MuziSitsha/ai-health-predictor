with open('app.py', 'r') as file:
    lines = file.readlines()

new_lines = []
i = 0
in_sidebar_block = False

while i < len(lines):
    line = lines[i]
    
    # Check if we're entering the sidebar block
    if 'else:' in line and i > 0 and 'st.session_state.current_page' in lines[i-1]:
        in_sidebar_block = True
    
    # Inside sidebar block, everything should be indented
    if in_sidebar_block:
        # Check current indentation
        current_indent = len(line) - len(line.lstrip())
        
        # Button definition line should be indented
        if line.strip().startswith('predict_button = st.sidebar.button'):
            if current_indent < 4:
                line = '    ' + line.lstrip()
        
        # Button logic should be indented and moved after function
        if '# Check if button was clicked' in line:
            # Skip this entire block - we'll handle it separately
            while i < len(lines) and 'pass' not in lines[i]:
                i += 1
            i += 1  # Skip pass line
            continue
    
    # Handle function definition - add button logic after it
    if 'def make_prediction(features_array):' in line:
        # Add the function
        new_lines.append(line)
        i += 1
        
        # Add function body
        while i < len(lines) and lines[i].strip() != '':
            new_lines.append(lines[i])
            i += 1
        
        # Now add properly indented button logic
        if in_sidebar_block:
            new_lines.append('')
            new_lines.append('    # Check if button was clicked')
            new_lines.append('    if predict_button:')
            new_lines.append('        st.session_state.current_prediction, st.session_state.current_proba = make_prediction(st.session_state.current_features)')
            new_lines.append('        st.session_state.prediction_made = True')
            new_lines.append('    elif st.session_state.prediction_made and st.session_state.current_prediction is not None:')
            new_lines.append('        # Use cached prediction - do nothing')
            new_lines.append('        pass')
            new_lines.append('')
        continue
    
    new_lines.append(line)
    i += 1

# Write back
with open('app.py', 'w') as file:
    file.writelines(new_lines)

print("✓ Fixed button logic indentation and placement")

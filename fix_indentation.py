with open('app.py', 'r') as file:
    lines = file.readlines()

# Find the problematic section
new_lines = []
in_sidebar_block = False
button_logic_added = False
prediction_made_line = -1

for i, line in enumerate(lines):
    # Check if we're in the sidebar block (after 'else:')
    if 'else:' in line and 'st.session_state.current_page' in lines[i-1]:
        in_sidebar_block = True
    
    # Find the button definition line
    if in_sidebar_block and 'predict_button = st.sidebar.button("Predict Diabetes Risk"' in line:
        new_lines.append(line)
        continue
    
    # Skip the incorrectly placed button logic
    if in_sidebar_block and '# Check if button was clicked' in line:
        # We'll save this logic to insert later
        button_logic_lines = []
        j = i
        while j < len(lines) and 'pass' not in lines[j]:
            button_logic_lines.append(lines[j])
            j += 1
        if j < len(lines):
            button_logic_lines.append(lines[j])  # Add the 'pass' line
        # Save these lines for later insertion
        saved_button_logic = ''.join(button_logic_lines)
        button_logic_added = True
        # Skip adding these lines now
        continue
    
    # Skip the auto-prediction comment line (we'll keep it commented)
    if '#     st.session_state.current_prediction, st.session_state.current_proba = make_prediction(current_features)' in line:
        new_lines.append(line)
        continue
    
    # Find where to insert the button logic (after the function definition and before display)
    if in_sidebar_block and 'def make_prediction' in line:
        # We'll add the button logic after this function
        func_lines = []
        j = i
        while j < len(lines) and lines[j].strip() != '':
            func_lines.append(lines[j])
            j += 1
        # Add the function
        new_lines.extend(func_lines)
        i = j - 1  # Adjust index
        
        # Now add the button logic AFTER the function
        if button_logic_added:
            new_lines.append('\n')
            new_lines.append('    # Check if button was clicked\n')
            new_lines.append('    if predict_button:\n')
            new_lines.append('        st.session_state.current_prediction, st.session_state.current_proba = make_prediction(st.session_state.current_features)\n')
            new_lines.append('        st.session_state.prediction_made = True\n')
            new_lines.append('    elif st.session_state.prediction_made and st.session_state.current_prediction is not None:\n')
            new_lines.append('        # Use cached prediction - do nothing\n')
            new_lines.append('        pass\n')
            button_logic_added = False  # Reset flag
        continue
    
    new_lines.append(line)

# Write back
with open('app.py', 'w') as file:
    file.writelines(new_lines)

print("✓ Fixed indentation - button logic now in correct place")

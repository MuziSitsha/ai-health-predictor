import re

# Read the current file
with open('app.py', 'r') as file:
    content = file.read()

# First, let's find and comment out the auto-prediction line
# Look for this exact line:
# st.session_state.current_prediction, st.session_state.current_proba = make_prediction(current_features)

lines = content.split('\n')
new_lines = []
skip_next = False

for i, line in enumerate(lines):
    if 'st.session_state.current_prediction, st.session_state.current_proba = make_prediction(current_features)' in line:
        # Comment out this line
        new_lines.append(f'# {line}  # AUTO-PREDICTION REMOVED - Now only on button click')
        print(f"✓ Commented out auto-prediction at line {i}")
    elif 'st.session_state.prediction_made = True' in line and i > 0 and 'make_prediction' not in lines[i-1]:
        # Keep this line but we'll handle it differently
        new_lines.append(line)
    else:
        new_lines.append(line)

# Join back
content = '\n'.join(new_lines)

# Now let's add the button click logic
# Find where the button is created
button_match = re.search(r'predict_button = st\.sidebar\.button\("Predict Diabetes Risk".*?use_container_width=True\)', content)
if button_match:
    button_line = button_match.group(0)
    button_end = button_match.end()
    
    # Insert the button click logic right after the button definition
    new_content = content[:button_end] + '\n\n' + '''# Check if button was clicked
if predict_button:
    st.session_state.current_prediction, st.session_state.current_proba = make_prediction(st.session_state.current_features)
    st.session_state.prediction_made = True
elif st.session_state.prediction_made and st.session_state.current_prediction is not None:
    # Use cached prediction - do nothing
    pass''' + content[button_end:]
    
    content = new_content
    print("✓ Added button click logic")
else:
    print("⚠ Could not find button definition")

# Write the updated content back
with open('app.py', 'w') as file:
    file.write(content)
    
print("✓ Updated app.py saved")

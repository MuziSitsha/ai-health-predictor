import re

with open('app.py', 'r') as file:
    content = file.read()

print("Fixing multiple issues...")

# Fix 1: Ensure with viz_col1: has proper indented block
content = re.sub(
    r'with viz_col1:\n(?!\s)',
    'with viz_col1:\n    ',
    content
)

# Fix 2: Remove duplicate button logic and place it correctly
# First, find and remove any button logic outside function
lines = content.split('\n')
cleaned_lines = []
skip = False

for i, line in enumerate(lines):
    if '# Check if button was clicked' in line and 'def make_prediction' not in lines[i-2:i+2]:
        skip = True
    if skip and 'pass' in line:
        skip = False
        continue
    if not skip:
        cleaned_lines.append(line)

content = '\n'.join(cleaned_lines)

# Fix 3: Insert button logic after make_prediction function
func_match = re.search(r'(def make_prediction\(features_array\):.*?\n)(\n|$)', content, re.DOTALL)
if func_match:
    func_end = func_match.end(1)
    button_logic = '''
    # Check if button was clicked
    if predict_button:
        st.session_state.current_prediction, st.session_state.current_proba = make_prediction(st.session_state.current_features)
        st.session_state.prediction_made = True
    elif st.session_state.prediction_made and st.session_state.current_prediction is not None:
        # Use cached prediction - do nothing
        pass
'''
    content = content[:func_end] + button_logic + content[func_end:]

# Fix 4: Ensure all sidebar content is indented
# Find the sidebar block
sidebar_start = content.find('''else:
    # Back button for example pages''')
if sidebar_start != -1:
    # Get everything from sidebar_start to end
    before = content[:sidebar_start]
    sidebar_content = content[sidebar_start:]
    
    # Indent all lines in sidebar by 4 spaces
    sidebar_lines = sidebar_content.split('\n')
    indented_sidebar = []
    for line in sidebar_lines:
        if line.strip() == '':
            indented_sidebar.append(line)
        else:
            indented_sidebar.append('    ' + line)
    
    content = before + '\n'.join(indented_sidebar)

# Write back
with open('app.py', 'w') as file:
    file.write(content)

print("✓ All fixes applied")

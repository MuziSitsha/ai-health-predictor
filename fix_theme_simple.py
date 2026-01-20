import re

with open('app.py', 'r') as f:
    content = f.read()

# Find and replace the theme toggle section
# Look for the theme toggle button code
toggle_pattern = r'# Sidebar theme toggle at the top.*?st\.sidebar\.markdown\("---"\)'
match = re.search(toggle_pattern, content, re.DOTALL)

if match:
    # Replace with clean version without emojis
    new_toggle = '''# Sidebar theme toggle at the top
current_theme = st.session_state.theme_mode
button_text = "Switch to Dark Mode" if current_theme == 'light' else "Switch to Light Mode"
if st.sidebar.button(button_text, key="theme_toggle", use_container_width=True):
    if current_theme == 'light':
        st.session_state.theme_mode = 'dark'
    else:
        st.session_state.theme_mode = 'light'
    st.rerun()
    
# Show current theme status
st.sidebar.caption(f"Current theme: {current_theme.title()} Mode")
st.sidebar.markdown("---")'''
    
    content = content.replace(match.group(0), new_toggle)
    print("Fixed theme toggle (no emojis)")
else:
    print("Could not find theme toggle pattern")

with open('app.py', 'w') as f:
    f.write(content)

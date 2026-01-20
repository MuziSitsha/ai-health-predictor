with open('app.py', 'r') as f:
    content = f.read()

# Add global input styling that works for both themes
global_styles = '''
    /* Global input styling that adapts to theme */
    div.stNumberInput, div.stSlider {
        background-color: transparent;
    }
    
    /* Make sure inputs inherit theme colors */
    .stNumberInput input, .stSlider div {
        transition: background-color 0.3s ease;
    }
'''

# Add to the existing CSS
css_start = '# Custom CSS - Base styles for both modes'
if css_start in content:
    # Insert after the opening style tag
    insert_point = '<style>'
    if insert_point in content:
        # Find the position after <style>
        pos = content.find(insert_point) + len(insert_point)
        content = content[:pos] + '\n    ' + global_styles + content[pos:]
        print("Added global input styles")
    else:
        print("Could not find <style> tag")
else:
    print("Could not find CSS section")

with open('app.py', 'w') as f:
    f.write(content)

with open('app.py', 'r') as f:
    content = f.read()

# Find where the create_risk_gauge function ends
func_end = content.find('    return fig\n')
if func_end != -1:
    # Find the next non-empty line after return fig
    after_return = content[func_end + len('    return fig\n'):]
    
    # Look for the next line that starts with proper indentation (not floating code)
    lines_after = after_return.split('\n')
    for i, line in enumerate(lines_after):
        if line.strip() and not line.startswith('        '):
            # This is where valid code starts again
            break_point = func_end + len('    return fig\n') + sum(len(l) + 1 for l in lines_after[:i])
            
            # Remove everything between return fig and the next valid code
            content = content[:func_end + len('    return fig\n')] + content[break_point:]
            print(f"✓ Removed {i} lines of floating code after create_risk_gauge function")
            break
else:
    print("Could not find 'return fig' in function")

with open('app.py', 'w') as f:
    f.write(content)

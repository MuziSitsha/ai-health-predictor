with open('app.py', 'r') as file:
    lines = file.readlines()

# Find and fix the with viz_col1: statement
new_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Look for the problematic with statement
    if line.strip() == 'with viz_col1:' and (i+1 < len(lines) and not lines[i+1].startswith('    ')):
        print(f"Found unindented with statement at line {i}")
        
        # Add the with statement
        new_lines.append(line)
        
        # The next line should be indented but isn't
        # We need to add proper indentation to the next block
        i += 1
        
        # Find how much to indent (should be 4 spaces for inside viz_col1)
        base_indent = len(line) - len(line.lstrip())
        target_indent = base_indent + 4
        
        # Indent all lines until we find a line with less indentation
        while i < len(lines):
            current_line = lines[i]
            current_indent = len(current_line) - len(current_line.lstrip())
            
            # Stop if we hit another with statement at same level or less indentation
            if current_line.strip().startswith('with ') and current_indent <= base_indent:
                break
            
            # Skip empty lines with no indentation
            if current_line.strip() == '' and current_indent == 0:
                new_lines.append(current_line)
                i += 1
                continue
            
            # Add indentation
            if current_indent < target_indent:
                indented_line = ' ' * target_indent + current_line.lstrip()
                new_lines.append(indented_line)
            else:
                new_lines.append(current_line)
            
            i += 1
        
        continue
    
    new_lines.append(line)
    i += 1

# Write back
with open('app.py', 'w') as file:
    file.writelines(new_lines)

print("✓ Fixed with statement indentation")

with open('app.py', 'r') as file:
    lines = file.readlines()

# Find the with viz_col1: statement
new_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    if 'with viz_col1:' in line:
        print(f"Found with viz_col1: at line {i+1}")
        
        # Add the with statement
        new_lines.append(line)
        i += 1
        
        # Get the indentation level
        base_indent = len(lines[i-1]) - len(lines[i-1].lstrip())
        
        # Now we need to indent everything until the matching with viz_col2:
        while i < len(lines):
            current_line = lines[i]
            
            # Check if we've reached with viz_col2: at the same indentation level
            if 'with viz_col2:' in current_line:
                current_indent = len(current_line) - len(current_line.lstrip())
                if current_indent == base_indent:
                    print(f"  Found matching with viz_col2: at line {i+1}, stopping indentation")
                    break
            
            # Indent this line
            if current_line.strip() != '':
                # Add 4 spaces to the existing indentation
                new_lines.append(' ' * 4 + current_line)
            else:
                # Keep empty lines as is
                new_lines.append(current_line)
            
            i += 1
        
        # Don't increment i here, we'll process the with viz_col2: next
        continue
    
    new_lines.append(line)
    i += 1

# Write back
with open('app.py', 'w') as file:
    file.writelines(new_lines)

print("✓ Fixed with statement indentation definitively")

with open('app.py', 'r') as file:
    lines = file.readlines()

print("Fixing all syntax errors...")

# Fix 1: Line 370 - else without if
# Let's see what's around line 370
for i in range(365, 375):
    print(f"Line {i}: {lines[i].rstrip()}")

# Fix 2: The with viz_col1: statement at line 641
# Let me find the exact line
with_line_num = -1
for i, line in enumerate(lines):
    if 'with viz_col1:' in line:
        with_line_num = i
        print(f"Found 'with viz_col1:' at line {i}: {line.rstrip()}")
        # Check next line
        if i+1 < len(lines):
            print(f"Next line {i+1}: {lines[i+1].rstrip()}")
        break

# Now let's rewrite the file with proper fixes
new_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Fix the else at line 370
    if i == 369:  # Python is 0-indexed, line 370 is index 369
        print(f"Fixing line 370: {line.rstrip()}")
        # Let's see the context to understand what's wrong
        prev_lines = lines[i-5:i]
        next_lines = lines[i:i+5]
        print("Previous lines:")
        for j, pl in enumerate(prev_lines):
            print(f"  {i-5+j}: {pl.rstrip()}")
        print("Next lines:")
        for j, nl in enumerate(next_lines):
            print(f"  {i+j}: {nl.rstrip()}")
    
    # Fix the with viz_col1: indentation
    if 'with viz_col1:' in line:
        print(f"Fixing with statement at line {i+1}")
        # Add the with statement
        new_lines.append(line)
        i += 1
        
        # The next line MUST be indented
        if i < len(lines):
            next_line = lines[i]
            if not next_line.startswith('    ') and next_line.strip() != '':
                print(f"  Line {i+1} needs indentation: {next_line.rstrip()}")
                # Add 4 spaces
                new_lines.append('    ' + next_line.lstrip())
                i += 1
                
                # Continue indenting until we hit a line with less indentation
                base_indent = len(line) - len(line.lstrip())
                while i < len(lines):
                    current_line = lines[i]
                    current_indent = len(current_line) - len(current_line.lstrip())
                    
                    # Check if we should stop indenting
                    if (current_line.strip().startswith('with ') or 
                        current_line.strip().startswith('if ') or
                        current_line.strip().startswith('elif ') or
                        current_line.strip().startswith('else:') or
                        current_line.strip().startswith('for ') or
                        current_line.strip().startswith('def ')):
                        # This starts a new block, stop indenting
                        break
                    
                    # Check if line is empty or has less indentation than expected
                    if current_line.strip() == '' and current_indent <= base_indent:
                        # Empty line at base level, stop
                        break
                    
                    # Indent this line
                    if current_indent < base_indent + 4:
                        new_lines.append(' ' * (base_indent + 4) + current_line.lstrip())
                    else:
                        new_lines.append(current_line)
                    
                    i += 1
                
                continue  # Skip the normal append at the end
    
    new_lines.append(line)
    i += 1

# Write back
with open('app.py', 'w') as file:
    file.writelines(new_lines)

print("✓ Applied fixes")

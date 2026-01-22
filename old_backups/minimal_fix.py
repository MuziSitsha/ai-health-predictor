with open('app_original.py', 'r') as f:
    lines = f.readlines()

# Just fix the with statement
new_lines = []
for i, line in enumerate(lines):
    if line.strip() == 'with viz_col1:' and i+1 < len(lines):
        # Make sure next line is indented
        new_lines.append(line)
        if not lines[i+1].startswith('    '):
            # Indent the next block
            j = i + 1
            while j < len(lines) and (lines[j].strip() != '' or j == i+1):
                if not lines[j].startswith('    '):
                    new_lines.append('    ' + lines[j])
                else:
                    new_lines.append(lines[j])
                j += 1
            # Skip the lines we just added
            i = j - 1
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open('app.py', 'w') as f:
    f.writelines(new_lines)

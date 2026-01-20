with open('app.py', 'r') as file:
    content = file.read()

# Find the problematic else statement
lines = content.split('\n')
for i, line in enumerate(lines):
    if i == 369:  # Line 370
        print(f"Line {i+1} (before): {line}")
        # Check what comes before
        print("Looking at previous lines to understand context...")
        
        # Check 5 lines before
        for j in range(max(0, i-5), i):
            print(f"  Line {j+1}: {lines[j]}")
        
        # Check if this is part of a button click check
        # It looks like it might be from the button logic that was moved
        # Let's check if we should remove it
        if line.strip() == 'else:' and 'predict_button' not in lines[i-1] and 'predict_button' not in lines[i-2]:
            print("This else: doesn't seem to have a matching if. Removing it.")
            lines[i] = '# ' + line + '  # REMOVED: No matching if statement'
        break

# Write back
with open('app.py', 'w') as file:
    file.write('\n'.join(lines))

print("✓ Fixed else statement")

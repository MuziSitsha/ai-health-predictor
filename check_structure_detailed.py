with open('app.py', 'r') as file:
    lines = file.readlines()

print("Checking structure from line 350 to 400...")
print("=" * 60)

for i in range(350, 400):
    line = lines[i]
    indent = len(line) - len(line.lstrip())
    prefix = " " * (indent // 4) + "|-> " if indent > 0 else ""
    
    # Highlight problematic lines
    if line.strip() == 'else:':
        print(f"Line {i+1}: {prefix}⚠⚠⚠ {line.rstrip()} ⚠⚠⚠")
    elif 'if ' in line and ':' in line:
        print(f"Line {i+1}: {prefix}IF: {line.rstrip()}")
    elif 'elif ' in line:
        print(f"Line {i+1}: {prefix}ELIF: {line.rstrip()}")
    elif line.strip().startswith('def '):
        print(f"Line {i+1}: {prefix}FUNCTION: {line.rstrip()}")
    elif line.strip().startswith('with '):
        print(f"Line {i+1}: {prefix}WITH: {line.rstrip()}")
    else:
        print(f"Line {i+1}: {prefix}{line.rstrip()}")

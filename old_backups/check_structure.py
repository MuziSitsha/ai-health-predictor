with open('app.py', 'r') as file:
    lines = file.readlines()

print("Checking structure...")
print("=" * 50)

# Find key sections
for i, line in enumerate(lines):
    if 'predict_button = st.sidebar.button' in line:
        print(f"Line {i}: BUTTON DEFINITION")
        # Show context
        for j in range(max(0, i-2), min(len(lines), i+10)):
            prefix = ">>> " if j == i else "    "
            print(f"{prefix}{j}: {lines[j].rstrip()}")
        print()
    
    if 'def make_prediction' in line:
        print(f"Line {i}: FUNCTION DEFINITION")
        # Show context
        for j in range(max(0, i-2), min(len(lines), i+15)):
            prefix = ">>> " if j == i else "    "
            print(f"{prefix}{j}: {lines[j].rstrip()}")
        print()
    
    if '# Check if button was clicked' in line:
        print(f"Line {i}: BUTTON LOGIC")
        # Show context
        for j in range(max(0, i-2), min(len(lines), i+8)):
            prefix = ">>> " if j == i else "    "
            print(f"{prefix}{j}: {lines[j].rstrip()}")
        print()


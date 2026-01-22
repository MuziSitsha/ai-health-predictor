import re

def remove_emojis(text):
    # Remove emojis and other non-ASCII characters
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove emojis
clean_content = remove_emojis(content)

# Also remove any problematic characters
clean_content = clean_content.replace('Ìø•', '')
clean_content = clean_content.replace('Ì≤ä', '')
clean_content = clean_content.replace('Ì≥ä', '')
clean_content = clean_content.replace('Ì≥à', '')
clean_content = clean_content.replace('‚ö†Ô∏è', '')
clean_content = clean_content.replace('‚úÖ', '')
clean_content = clean_content.replace('‚ùå', '')

# Save cleaned file
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(clean_content)

print("Emojis removed from app.py")

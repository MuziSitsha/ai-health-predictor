#!/usr/bin/env python3
import re

def remove_all_emojis(text):
    # Pattern to match emojis and other special Unicode characters
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002500-\U00002BEF"  # Chinese/Japanese/Korean characters
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"
        u"\u3030"
        "]+", flags=re.UNICODE)
    
    # Remove all matching patterns
    return emoji_pattern.sub(r'', text)

# Read the app.py file
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove emojis
clean_content = remove_all_emojis(content)

# Also remove specific common emoji replacements
clean_content = clean_content.replace("‚úÖ", "")
clean_content = clean_content.replace("‚ùå", "")
clean_content = clean_content.replace("‚ö†", "")
clean_content = clean_content.replace("Ìæâ", "")
clean_content = clean_content.replace("Ì≥±", "")
clean_content = clean_content.replace("‚è≥", "")
clean_content = clean_content.replace("Ì¥Æ", "")
clean_content = clean_content.replace("Ì∫®", "")
clean_content = clean_content.replace("Ìø•", "")
clean_content = clean_content.replace("‚úì", "")
clean_content = clean_content.replace("‚úó", "")

# Write back to app.py
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(clean_content)

print("Removed all emojis from app.py")

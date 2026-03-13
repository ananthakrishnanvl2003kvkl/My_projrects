import re

# Read the main HTML
with open('frontend/public/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Read the manual form section
with open('frontend/manual_form_section.html', 'r', encoding='utf-8') as f:
    manual_form = f.read()

# Find the position after voice section (before loading section)
# Look for the closing div of voice section followed by loading section
pattern = r'(</div>\s*</div>\s*)\s*(<div class="loading" id="loading">)'

# Insert the manual form section
html_content = re.sub(
    pattern,
    r'\1\n' + manual_form + r'\n\2',
    html_content,
    count=1
)

# Write back
with open('frontend/public/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Manual form section inserted successfully!")

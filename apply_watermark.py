import base64
import re

img_path = r"C:\Users\ANANTHAKRISHNAN V L\.gemini\antigravity\brain\3df8da00-b94b-42bc-bf19-6712b2017efd\flat_ai_shield_watermark_1773428033072.png"
app_path = r"c:\Users\ANANTHAKRISHNAN V L\OneDrive\Desktop\Ananthan\fir_app.py"

with open(img_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

b64_url = f"url('data:image/png;base64,{encoded_string}')"

with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace watermark pseudo element
content = re.sub(
    r"content: '⚖️';\s*position: fixed;", 
    f"content: '';\\n        background-image: {b64_url};\\n        background-size: 50vw auto;\\n        background-repeat: no-repeat;\\n        background-position: center;\\n        position: fixed;", 
    content
)

# Replace the giant font size for the watermark to changing opacity 
content = re.sub(
    r"font-size: 50vw;  /\* Enormous size \*/\s*opacity: 0.03;    /\* Very faint watermark \*/",
    r"/* font-size replaced by image bg */\n        opacity: 0.05;    /* Subtle flat watermark */",
    content
)

with open(app_path, "w", encoding="utf-8") as f:
    f.write(content)

print("App background watermark patched successfully.")

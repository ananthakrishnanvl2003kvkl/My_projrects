import json
import csv
import os

json_path = r"c:\Users\ANANTHAKRISHNAN V L\OneDrive\Desktop\Ananthan\intelligent-fir-analyzer-main\data\ipc_sections.json"
csv_path = r"c:\Users\ANANTHAKRISHNAN V L\OneDrive\Desktop\Ananthan\all_ipc_sections.csv"

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    sections = data.get('sections', [])

with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # Write header
    writer.writerow(['Section', 'Title', 'Description', 'Keywords'])
    
    # Write rows
    for sec in sections:
        section_id = sec.get('section', '')
        title = sec.get('title', '')
        desc = sec.get('description', '')
        keywords = ", ".join(sec.get('keywords', []))
        
        writer.writerow([section_id, title, desc, keywords])

print(f"Successfully created CSV with {len(sections)} sections at: {csv_path}")

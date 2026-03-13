"""
Test OCR and Legal-BERT with sample FIR
"""
from backend.services.ocr_service import ocr_service
from backend.services.enhanced_classification_service import enhanced_classification_service
from backend.services.text_extractor import text_extractor

# Test with sample FIR
image_path = 'C:/Users/aravi/.gemini/antigravity/brain/52e0d39e-9145-4fe3-aba0-7b7f180cea8b/sample_fir_theft_1768752498176.png'

print("="*80)
print("TESTING FIR ANALYSIS PIPELINE WITH SAMPLE FIR")
print("="*80)

# Step 1: OCR Extraction
print("\n>> Step 1: OCR Extraction...")
text, confidence, method = ocr_service.extract_text(image_path)

print(f"Method Used: {method}")
print(f"Confidence: {confidence:.2%}")
print(f"Text Length: {len(text)} characters")
print(f"\nExtracted Text (first 500 chars):\n{text[:500]}")

# Step 2: Text Extraction
print("\n" + "="*80)
print(">> Step 2: Field Extraction...")
extracted = text_extractor.extract_complete_fir(text)

print(f"FIR Number: {extracted.get('fir_number', 'Not found')}")
print(f"Date: {extracted.get('date_of_incident', 'Not found')}")
print(f"Time: {extracted.get('time_of_incident', 'Not found')}")
print(f"Police Station: {extracted.get('police_station', 'Not found')}")
print(f"Complainant: {extracted.get('complainant', 'Not found')}")
print(f"Location: {extracted.get('location', 'Not found')}")
print(f"IPC Sections Found: {extracted.get('ipc_sections', [])}")
print(f"Extraction Confidence: {extracted.get('extraction_confidence', 0):.1%}")

# Step 3: Classification & IPC Prediction
print("\n" + "="*80)
print(">> Step 3: Legal-BERT Analysis...")
analysis = enhanced_classification_service.analyze_fir(text)

print(f"\nClassification:")
criminal_type = 'CRIMINAL' if analysis['classification']['is_criminal'] else 'NON-CRIMINAL'
print(f"  Type: {criminal_type}")
print(f"  Confidence: {analysis['classification']['confidence']:.1%}")
print(f"  Reasoning: {analysis['classification']['reasoning']}")

print(f"\nPrimary IPC Section: {analysis['primary_section']}")

print(f"\nTop 5 Predicted IPC Sections:")
for i, section in enumerate(analysis['predicted_sections'][:5], 1):
    print(f"{i}. {section['section']}: {section['title']}")
    print(f"   Confidence: {section['confidence']:.1%}")
    print(f"   Method: {section.get('method', 'N/A')}")
    if 'ml_confidence' in section:
        print(f"   ML: {section['ml_confidence']:.1%} | Rules: {section['rule_confidence']:.1%}")
    print()

ml_used = 'YES' if analysis['ml_model_used'] else 'NO'
print(f"ML Model Used: {ml_used}")

# Step 4: Verification
print("\n" + "="*80)
print("VERIFICATION")
print("="*80)

expected_sections = ['IPC 379', 'IPC 380']
predicted_sections = [s['section'] for s in analysis['predicted_sections'][:5]]

print(f"Expected IPC Sections: {', '.join(expected_sections)}")
print(f"Predicted Sections: {', '.join(predicted_sections)}")

# Check if expected sections are in predictions
found = [exp for exp in expected_sections if exp in predicted_sections]
print(f"\nMatches Found: {found}")

if found:
    print("[PASS] Legal-BERT correctly predicted theft-related IPC sections!")
else:
    print("[FAIL] Expected sections not in predictions")

print("\n" + "="*80)

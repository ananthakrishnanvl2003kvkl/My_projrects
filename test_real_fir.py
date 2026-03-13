"""
Test the real FIR image uploaded by user
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.services.ocr_service import ocr_service
from backend.services.classification_service import classification_service

# Test with real FIR
real_fir = project_root / "scripts" / "sample_firs" / "real_fir_test.jpg"

print(f"Testing Real FIR Image: {real_fir.name}")
print("="*80)

# Extract text
print("\n[STEP 1] OCR TEXT EXTRACTION")
print("-" * 80)
text, confidence, method = ocr_service.extract_text(str(real_fir))
print(f"OCR Method: {method.upper()}")
print(f"Confidence: {confidence:.1%}")
print(f"Characters Extracted: {len(text)}")
print(f"\n--- EXTRACTED TEXT ---")
print(text)
print("-" * 80)

# Classify and predict sections
print("\n\n[STEP 2] ANALYSIS & CLASSIFICATION")
print("-" * 80)
analysis = classification_service.analyze_fir(text)

classification = analysis['classification']['is_criminal']
conf = analysis['classification']['confidence']
reasoning = analysis['classification']['reasoning']

print(f"\nClassification: {'CRIMINAL CASE' if classification else 'NON-CRIMINAL CASE'}")
print(f"Confidence: {conf:.1%}")
print(f"Reasoning: {reasoning}")

print("\n\n[STEP 3] IPC/CrPC SECTION PREDICTIONS")
print("-" * 80)
sections = analysis['predicted_sections']

if sections:
    print(f"\nFound {len(sections)} predicted sections:\n")
    for i, section in enumerate(sections, 1):
        print(f"{i}. {section['section']}")
        print(f"   Title: {section['title']}")
        print(f"   Confidence: {section['confidence']:.1%}")
        print(f"   Description: {section['description'][:120]}...")
        print()
else:
    print("No sections predicted")

print("\n" + "="*80)
print("FINAL SUMMARY")
print("="*80)
print(f"OCR Confidence: {confidence:.1%}")
print(f"Classification: {'CRIMINAL' if classification else 'NON-CRIMINAL'} ({conf:.1%})")
print(f"IPC Sections Predicted: {len(sections)}")
if sections:
    print(f"Top Section: {sections[0]['section']} - {sections[0]['title']} ({sections[0]['confidence']:.1%})")
print("="*80)

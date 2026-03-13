"""
Test the improved OCR and section prediction with clean FIR
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.services.ocr_service import ocr_service
from backend.services.classification_service import classification_service

# Test with clean FIR
clean_fir = project_root / "scripts" / "sample_firs" / "clean_fir_robbery.png"

print(f"Testing OCR and Classification on: {clean_fir.name}\n")
print("="*70)

# Extract text
print("\n1. OCR EXTRACTION")
print("-" * 70)
text, confidence, method = ocr_service.extract_text(str(clean_fir))
print(f"Method: {method}")
print(f"OCR Confidence: {confidence:.1%}")
print(f"Text Length: {len(text)} characters")
print(f"\nExtracted Text:")
print(text)

# Classify and predict sections
print("\n\n2. CLASSIFICATION & SECTION PREDICTION")
print("-" * 70)
analysis = classification_service.analyze_fir(text)

print(f"\nClassification: {'CRIMINAL' if analysis['classification']['is_criminal'] else 'NON-CRIMINAL'}")
print(f"Confidence: {analysis['classification']['confidence']:.1%}")
print(f"Reasoning: {analysis['classification']['reasoning']}")

print(f"\n\n3. PREDICTED IPC SECTIONS")
print("-" * 70)
sections = analysis['predicted_sections']
if sections:
    print(f"Found {len(sections)} predicted sections:\n")
    for i, section in enumerate(sections, 1):
        print(f"{i}. {section['section']}: {section['title']}")
        print(f"   Confidence: {section['confidence']:.1%}")
        print()
else:
    print("No sections predicted")

print("\n" + "="*70)
print(f"\nRESULTS SUMMARY:")
print(f"[OK] OCR Confidence: {confidence:.1%}")
print(f"[OK] Classification: {'CRIMINAL' if analysis['classification']['is_criminal'] else 'NON-CRIMINAL'} ({analysis['classification']['confidence']:.1%})")
print(f"[OK] IPC Sections Predicted: {len(sections)}")
if sections:
    print(f"[OK] Top Section: {sections[0]['section']} ({sections[0]['confidence']:.1%})")

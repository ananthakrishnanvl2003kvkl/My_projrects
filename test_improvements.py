"""
Test the improved OCR and section prediction directly
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.services.ocr_service import ocr_service
from backend.services.classification_service import classification_service

# Test with sample FIR
sample_fir = project_root / "scripts" / "sample_firs" / "sample_fir_1_criminal.png"

print(f"Testing OCR and Classification on: {sample_fir.name}\n")
print("="*70)

# Extract text
print("\n1. OCR EXTRACTION")
print("-" * 70)
text, confidence, method = ocr_service.extract_text(str(sample_fir))
print(f"Method: {method}")
print(f"Confidence: {confidence:.2%}")
print(f"Text Length: {len(text)} characters")
print(f"\nExtracted Text Preview (first 500 chars):")
print(text[:500])
print("...")

# Classify and predict sections
print("\n\n2. CLASSIFICATION & SECTION PREDICTION")
print("-" * 70)
analysis = classification_service.analyze_fir(text)

print(f"\nClassification: {'CRIMINAL' if analysis['classification']['is_criminal'] else 'NON-CRIMINAL'}")
print(f"Confidence: {analysis['classification']['confidence']:.2%}")
print(f"Reasoning: {analysis['classification']['reasoning']}")

print(f"\n\n3. PREDICTED SECTIONS")
print("-" * 70)
sections = analysis['predicted_sections']
if sections:
    print(f"Found {len(sections)} predicted sections:\n")
    for i, section in enumerate(sections, 1):
        print(f"{i}. {section['section']}: {section['title']}")
        print(f"   Confidence: {section['confidence']:.2%}")
        print(f"   Description: {section['description'][:100]}...")
        print()
else:
    print("No sections predicted")

print("\n" + "="*70)
print(f"\nSUMMARY:")
print(f"✓ OCR Confidence: {confidence:.2%}")
print(f"✓ Classification: {'CRIMINAL' if analysis['classification']['is_criminal'] else 'NON-CRIMINAL'} ({analysis['classification']['confidence']:.2%})")
print(f"✓ Sections Predicted: {len(sections)}")

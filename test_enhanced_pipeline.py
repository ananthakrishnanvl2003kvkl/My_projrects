"""
Test the complete enhanced FIR processing pipeline
Stage 1: Advanced OpenCV Preprocessing
Stage 2: Handwritten TrOCR
Stage 3: Intelligent Field Extraction
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.services.ocr_service import ocr_service
from backend.services.classification_service import classification_service
from backend.services.fir_field_extractor import fir_field_extractor

# Test with real FIR
real_fir = project_root / "scripts" / "sample_firs" / "real_fir_test.jpg"

print("=" * 80)
print("ENHANCED FIR PROCESSING PIPELINE TEST")
print("=" * 80)
print(f"\nInput: {real_fir.name}")
print("\nPipeline Stages:")
print("  1. Advanced OpenCV Preprocessing (skew, denoise, enhance)")
print("  2. Handwritten TrOCR (large model)")
print("  3. Intelligent Field Extraction (regex + mapping)")
print("\n" + "=" * 80)

# STAGE 1 & 2: OCR with preprocessing
print("\n[STAGE 1 & 2] OCR EXTRACTION WITH PREPROCESSING")
print("-" * 80)
text, confidence, method = ocr_service.extract_text(str(real_fir), use_preprocessing=True)
print(f"OCR Method: {method.upper()}")
print(f"Confidence: {confidence:.1%}")
print(f"Characters Extracted: {len(text)}")
print(f"\n--- RAW OCR TEXT ---")
print(text[:500] + "..." if len(text) > 500 else text)
print("-" * 80)

# STAGE 3: Field Extraction
print("\n\n[STAGE 3] INTELLIGENT FIELD EXTRACTION")
print("-" * 80)
extraction_result = fir_field_extractor.extract_all_fields(text)

fields = extraction_result['fields']
confidences = extraction_result['field_confidences']
summary = extraction_result['extraction_summary']

print(f"\nExtraction Summary:")
print(f"  Fields Extracted: {summary['fields_extracted']}/{summary['total_fields']}")
print(f"  Extraction Rate: {summary['extraction_rate']:.1%}")
print(f"  Overall Confidence: {extraction_result['overall_confidence']:.1%}")

print(f"\n--- EXTRACTED FIELDS ---\n")

def print_field(name, value, confidence):
    status = "✓" if value else "✗"
    conf_str = f"({confidence:.0%})" if value else "(N/A)"
    value_str = str(value) if value else "Not found"
    print(f"{status} {name:20s}: {value_str:40s} {conf_str}")

print_field("FIR Number", fields['fir_number'], confidences['fir_number'])
print_field("Date", fields['date'], confidences['date'])
print_field("Time", fields['time'], confidences['time'])
print_field("Police Station", fields['police_station'], confidences['police_station'])
print_field("Complainant", fields['complainant'], confidences['complainant'])
print_field("Accused", fields['accused'], confidences['accused'])
print_field("Location", fields['location'], confidences['location'])

if fields['ipc_sections']:
    print(f"✓ IPC Sections      : {', '.join(fields['ipc_sections'])}")
else:
    print(f"✗ IPC Sections      : Not found")

if fields['crpc_sections']:
    print(f"✓ CrPC Sections     : {', '.join(fields['crpc_sections'])}")
else:
    print(f"✗ CrPC Sections     : Not found")

if fields['other_acts']:
    print(f"✓ Other Acts        : {', '.join(fields['other_acts'])}")
else:
    print(f"✗ Other Acts        : Not found")

# ADDITIONAL: Classification
print("\n\n[ADDITIONAL] CLASSIFICATION & SECTION PREDICTION")
print("-" * 80)
analysis = classification_service.analyze_fir(text)

classification = analysis['classification']['is_criminal']
conf = analysis['classification']['confidence']
reasoning = analysis['classification']['reasoning']

print(f"\nClassification: {'CRIMINAL CASE' if classification else 'NON-CRIMINAL CASE'}")
print(f"Confidence: {conf:.1%}")
print(f"Reasoning: {reasoning}")

sections = analysis['predicted_sections']
if sections:
    print(f"\n{len(sections)} IPC/CrPC Sections Predicted (from ML):")
    for i, section in enumerate(sections[:3], 1):
        print(f"  {i}. {section['section']}: {section['title']} ({section['confidence']:.1%})")

# FINAL SUMMARY
print("\n\n" + "=" * 80)
print("FINAL RESULTS SUMMARY")
print("=" * 80)
print(f"OCR Confidence:          {confidence:.1%}")
print(f"Field Extraction Rate:   {summary['extraction_rate']:.1%}")
print(f"Fields Extracted:        {summary['fields_extracted']}/{summary['total_fields']}")
print(f"Classification:          {'CRIMINAL' if classification else 'NON-CRIMINAL'} ({conf:.1%})")
print(f"ML Sections Predicted:   {len(sections)}")
print("=" * 80)

# Success metrics
success_score = (confidence + summary['extraction_rate'] + extraction_result['overall_confidence']) / 3
print(f"\nOverall Success Score: {success_score:.1%}")
if success_score > 0.7:
    print("Status: ✓ EXCELLENT")
elif success_score > 0.5:
    print("Status: ✓ GOOD")
else:
    print("Status: ⚠ NEEDS IMPROVEMENT")

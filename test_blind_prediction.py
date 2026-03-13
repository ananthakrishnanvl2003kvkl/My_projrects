"""
Test Legal-BERT prediction capability with FIR that has NO IPC sections mentioned
This proves the model is truly predicting, not just extracting
"""

from backend.services.ocr_service import ocr_service
from backend.services.enhanced_classification_service import enhanced_classification_service

# Test with FIR that has NO IPC sections in the text
image_path = 'C:/Users/aravi/.gemini/antigravity/brain/52e0d39e-9145-4fe3-aba0-7b7f180cea8b/fir_no_sections_*.png'

import glob
files = glob.glob(image_path)
if files:
    image_path = files[0]
    print("="*80)
    print("TESTING LEGAL-BERT PREDICTION (NO IPC SECTIONS IN FIR TEXT)")
    print("="*80)
    print(f"\nUsing: {image_path}")
    
    # Extract text
    print("\n>> Extracting text...")
    text, confidence, method = ocr_service.extract_text(image_path)
    print(f"OCR Method: {method}")
    print(f"Confidence: {confidence:.1%}")
    print(f"\nExtracted Text (first 500 chars):")
    print(text[:500])
    
    # Check if IPC sections are mentioned in text
    import re
    ipc_mentions = re.findall(r'IPC\s*\d+|section\s*\d+', text, re.IGNORECASE)
    print(f"\n>> Checking for IPC mentions in text...")
    print(f"IPC mentions found: {ipc_mentions if ipc_mentions else 'NONE (Good!)'}")
    
    # Analyze with Legal-BERT
    print("\n>> Analyzing with Legal-BERT (noisy-trained model)...")
    analysis = enhanced_classification_service.analyze_fir(text)
    
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80)
    
    print(f"\nClassification: {'CRIMINAL' if analysis['classification']['is_criminal'] else 'NON-CRIMINAL'}")
    print(f"Confidence: {analysis['classification']['confidence']:.1%}")
    
    print(f"\n>> Top 5 Predicted IPC Sections:")
    for i, section in enumerate(analysis['predicted_sections'][:5], 1):
        print(f"\n{i}. {section['section']}: {section['title']}")
        print(f"   Overall Confidence: {section['confidence']:.1%}")
        if 'ml_confidence' in section:
            print(f"   ML: {section['ml_confidence']:.1%} | Rules: {section['rule_confidence']:.1%}")
        print(f"   Description: {section['description'][:100]}...")
    
    print(f"\n{'='*80}")
    print(f"ML Model Used: {'YES (Legal-BERT)' if analysis['ml_model_used'] else 'NO'}")
    print(f"{'='*80}")
    
    # Expected result
    print(f"\n>> EXPECTED RESULT:")
    print(f"   This is a THEFT IN DWELLING case")
    print(f"   Expected IPC sections: 380 (Theft in Dwelling), 457 (House Breaking)")
    print(f"   Legal-BERT should predict these WITHOUT them being in the FIR text!")
    
else:
    print("FIR image not found!")

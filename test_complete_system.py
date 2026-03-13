"""
Comprehensive Test Suite for Enhanced FIR Analysis System
Tests OCR accuracy, IPC prediction, and end-to-end pipeline
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from backend.services.text_extractor import text_extractor
from backend.services.enhanced_classification_service import enhanced_classification_service
from backend.services.ocr_service import ocr_service
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_text_extraction():
    """Test text field extraction"""
    logger.info("\n" + "="*80)
    logger.info("TEST 1: Text Field Extraction")
    logger.info("="*80)
    
    sample_fir_text = """
    FIR No. 123/2024 dated 15-01-2024
    Police Station: Koramangala
    Complainant: Rajesh Kumar
    
    I want to report a case of theft. On 14th January 2024 at around 10:30 PM,
    unknown persons broke into my house at HSR Layout and stole cash worth Rs. 50,000
    and jewelry worth Rs. 2,00,000. The accused fled the scene before I could see them.
    
    This incident happened at my residence located at #123, 5th Main Road, HSR Layout.
    I request immediate action under applicable IPC sections.
    """
    
    result = text_extractor.extract_complete_fir(sample_fir_text)
    
    logger.info(f"\nExtracted Fields:")
    logger.info(f"  FIR Number: {result.get('fir_number')}")
    logger.info(f"  Police Station: {result.get('police_station')}")
    logger.info(f"  Complainant: {result.get('complainant')}")
    logger.info(f"  Date: {result.get('date_of_incident')}")
    logger.info(f"  Time: {result.get('time_of_incident')}")
    logger.info(f"  Location: {result.get('location')}")
    logger.info(f"  IPC Sections Found: {result.get('ipc_sections')}")
    logger.info(f"  Extraction Confidence: {result.get('extraction_confidence'):.1%}")
    
    success = result.get('fir_number') is not None
    logger.info(f"\n{'✓' if success else '✗'} Field extraction test {'PASSED' if success else 'FAILED'}")
    
    return success


def test_criminal_classification():
    """Test criminal vs non-criminal classification"""
    logger.info("\n" + "="*80)
    logger.info("TEST 2: Criminal Classification")
    logger.info("="*80)
    
    test_cases = [
        {
            'text': "I want to report a theft case. Someone stole my mobile phone yesterday.",
            'expected': True,
            'description': "Theft case (should be criminal)"
        },
        {
            'text': "My son has been missing since yesterday. We cannot find him anywhere.",
            'expected': False,
            'description': "Missing person (should be non-criminal)"
        },
        {
            'text': "The accused attacked me with a knife and caused severe injury.",
            'expected': True,
            'description': "Assault with weapon (should be criminal)"
        }
    ]
    
    passed = 0
    for i, case in enumerate(test_cases, 1):
        is_criminal, confidence, reasoning = enhanced_classification_service.classify_criminal(case['text'])
        correct = is_criminal == case['expected']
        
        logger.info(f"\nTest Case {i}: {case['description']}")
        logger.info(f"  Result: {'Criminal' if is_criminal else 'Non-criminal'} ({confidence:.1%})")
        logger.info(f"  Expected: {'Criminal' if case['expected'] else 'Non-criminal'}")
        logger.info(f"  {'✓ PASS' if correct else '✗ FAIL'}")
        
        if correct:
            passed += 1
    
    success_rate = passed / len(test_cases)
    logger.info(f"\n{'✓' if success_rate >= 0.66 else '✗'} Classification accuracy: {success_rate:.1%} ({passed}/{len(test_cases)})")
    
    return success_rate >= 0.66


def test_ipc_prediction():
    """Test IPC section prediction"""
    logger.info("\n" + "="*80)
    logger.info("TEST 3: IPC Section Prediction")
    logger.info("="*80)
    
    test_cases = [
        {
            'text': "The accused murdered my brother by stabbing him with a knife. He died on the spot.",
            'expected_sections': ['IPC 302', 'IPC 324'],
            'description': "Murder case"
        },
        {
            'text': "Someone stole my wallet containing Rs. 5000 from my house.",
            'expected_sections': ['IPC 379', 'IPC 380'],
            'description': "Theft in dwelling"
        },
        {
            'text': "The person cheated me and took Rs. 1 lakh promising to return but never did.",
            'expected_sections': ['IPC 420', 'IPC 406'],
            'description': "Cheating and fraud"
        }
    ]
    
    passed = 0
    for i, case in enumerate(test_cases, 1):
        predictions = enhanced_classification_service.predict_sections_hybrid(
            case['text'], 
            is_criminal=True, 
            top_k=5
        )
        
        predicted_sections = [p['section'] for p in predictions[:3]]
        
        # Check if any expected section is in predictions
        found_match = any(exp in predicted_sections for exp in case['expected_sections'])
        
        logger.info(f"\nTest Case {i}: {case['description']}")
        logger.info(f"  Text: {case['text'][:80]}...")
        logger.info(f"  Expected sections: {', '.join(case['expected_sections'])}")
        logger.info(f"  Predicted sections:")
        for p in predictions[:3]:
            logger.info(f"    - {p['section']}: {p['title']} ({p['confidence']:.1%})")
        logger.info(f"  {'✓ PASS' if found_match else '✗ FAIL'}")
        
        if found_match:
            passed += 1
    
    success_rate = passed / len(test_cases)
    logger.info(f"\n{'✓' if success_rate >= 0.66 else '✗'} Prediction accuracy: {success_rate:.1%} ({passed}/{len(test_cases)})")
    
    return success_rate >= 0.66


def test_end_to_end_pipeline():
    """Test complete FIR analysis pipeline"""
    logger.info("\n" + "="*80)
    logger.info("TEST 4: End-to-End Pipeline")
    logger.info("="*80)
    
    sample_fir = """
    FIR Number: 456/2024
    Date: 16-01-2024
    Police Station: Indiranagar
    
    Complainant: Priya Sharma
    Location: Indiranagar 100 Feet Road
    
    I want to file a complaint against unknown persons who robbed me at gunpoint
    yesterday night around 11 PM. The accused pointed a gun at me, threatened to
    kill me if I didn't hand over my belongings. They took my purse containing
    Rs. 15,000 cash, my mobile phone, and gold chain worth Rs. 50,000.
    
    I am very afraid and request immediate action under IPC 392 (Robbery) and
    IPC 506 (Criminal Intimidation).
    """
    
    logger.info("Analyzing complete FIR...")
    
    # Step 1: Extract fields
    extracted_data = text_extractor.extract_complete_fir(sample_fir)
    
    # Step 2: Classify and predict sections
    analysis = enhanced_classification_service.analyze_fir(sample_fir)
    
    logger.info(f"\n📋 ANALYSIS RESULTS:")
    logger.info(f"  FIR Number: {extracted_data.get('fir_number')}")
    logger.info(f"  Police Station: {extracted_data.get('police_station')}")
    logger.info(f"  Complainant: {extracted_data.get('complainant')}")
    logger.info(f"  Criminal: {analysis['classification']['is_criminal']} ({analysis['classification']['confidence']:.1%})")
    logger.info(f"  Primary Section: {analysis['primary_section']}")
    logger.info(f"  Predicted Sections:")
    for sec in analysis['predicted_sections'][:3]:
        logger.info(f"    - {sec['section']}: {sec['title']} ({sec['confidence']:.1%})")
    logger.info(f"  ML Model Used: {analysis['ml_model_used']}")
    
    # Verify results
    checks = {
        'FIR number extracted': extracted_data.get('fir_number') is not None,
        'Classified as criminal': analysis['classification']['is_criminal'],
        'IPC 392 or 506 predicted': any('392' in s['section'] or '506' in s['section'] 
                                       for s in analysis['predicted_sections']),
    }
    
    all_passed = all(checks.values())
    
    logger.info(f"\n{'✓' if all_passed else '✗'} End-to-end test {'PASSED' if all_passed else 'FAILED'}")
    for check, result in checks.items():
        logger.info(f"  {'✓' if result else '✗'} {check}")
    
    return all_passed


def main():
    """Run all tests"""
    logger.info("\n" + "="*80)
    logger.info("ENHANCED FIR ANALYSIS SYSTEM - COMPREHENSIVE TEST SUITE")
    logger.info("="*80)
    
    results = {
        'Text Extraction': test_text_extraction(),
        'Criminal Classification': test_criminal_classification(),
        'IPC Prediction': test_ipc_prediction(),
        'End-to-End Pipeline': test_end_to_end_pipeline()
    }
    
    # Summary
    logger.info("\n" + "="*80)
    logger.info("TEST SUMMARY")
    logger.info("="*80)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✓ PASS" if passed_test else "✗ FAIL"
        logger.info(f"  {status}: {test_name}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed ({passed/total:.1%})")
    
    if passed == total:
        logger.info("\n🎉 ALL TESTS PASSED! System is ready for deployment.")
    elif passed >= total * 0.75:
        logger.info("\n⚠️  Most tests passed. System is functional but needs minor fixes.")
    else:
        logger.info("\n❌ Multiple tests failed. System needs debugging.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

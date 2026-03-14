import sys
print(f"Python: {sys.version}")
try:
    print("Attempting to import rapidocr_onnxruntime...")
    from rapidocr_onnxruntime import RapidOCR
    print("RapidOCR imported successfully.")
    
    print("Attempting to initialize RapidOCR engine...")
    engine = RapidOCR()
    print("RapidOCR engine initialized successfully.")
    
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()

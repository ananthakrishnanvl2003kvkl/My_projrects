# FIR Analyzer - Intelligent Analysis System

An intelligent system to analyze First Information Report (FIR) documents by uploading images, extracting text using OCR, classifying criminal vs non-criminal cases, and predicting relevant IPC or CrPC sections using machine learning.

## Features

✨ **Image Upload & OCR**
- Support for multiple image formats (JPG, PNG, BMP, TIFF, PDF)
- Advanced OCR using EasyOCR and Tesseract
- Image preprocessing for better text extraction
- Support for English and Hindi text

🎯 **Intelligent Classification**
- Criminal vs Non-criminal case classification
- Confidence scoring for predictions
- Detailed reasoning for classifications

📋 **Section Prediction**
- Automatic IPC section prediction for criminal cases
- CrPC section prediction for non-criminal cases
- Multi-label classification with confidence scores
- Top-K section recommendations

🔍 **Entity Extraction**
- Extract complainant and accused names
- Identify locations, dates, and times
- Incident type classification

🎨 **Modern UI**
- Beautiful dark theme with glassmorphism effects
- Responsive design for all devices
- Real-time progress updates
- Smooth animations and transitions

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **EasyOCR** - Advanced OCR engine
- **Tesseract** - Backup OCR engine
- **scikit-learn** - Machine learning library
- **TensorFlow** - Deep learning framework

### Frontend
- **HTML5/CSS3/JavaScript** - Modern web technologies
- **Vanilla JavaScript** - No framework dependencies
- **CSS Animations** - Smooth, engaging UI

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Tesseract OCR (optional, for backup OCR)

### Step 1: Clone or Navigate to Project

```bash
cd c:\intelligent_fir_analyzer3
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Install Tesseract OCR (Windows - Optional)

Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

Or use the default path: `C:\Program Files\Tesseract-OCR\tesseract.exe`

If installed elsewhere, update the path in `backend/config.py`

### Step 4: Download EasyOCR Models

EasyOCR will automatically download required models on first run. Ensure you have internet connectivity.

## Running the Application

### Start the Backend Server

```bash
cd backend
python app.py
```

The API server will start at `http://localhost:8000`

### Access the Frontend

Open your browser and navigate to:
```
http://localhost:8000/static/index.html
```

Or serve the frontend separately and update `API_BASE_URL` in `frontend/public/app.js`

## API Documentation

Once the server is running, access the interactive API documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main Endpoints

#### Health Check
```
GET /api/health
```

#### Upload FIR Image
```
POST /api/upload-fir
Content-Type: multipart/form-data
Body: file (image file)
```

#### Analyze FIR
```
POST /api/analyze-fir/{fir_id}
```

#### Get Analysis Results
```
GET /api/fir/{fir_id}
```

#### List All FIRs
```
GET /api/firs?skip=0&limit=50
```

## Usage

1. **Open the Application**
   - Navigate to http://localhost:8000/static/index.html

2. **Upload FIR Image**
   - Click "Choose File" or drag and drop an FIR image
   - Supported formats: JPG, PNG, BMP, TIFF, PDF
   - Maximum file size: 10MB

3. **Analyze**
   - Click "Analyze FIR" button
   - Wait for OCR extraction and classification
   - View comprehensive results

4. **Review Results**
   - Classification (Criminal/Non-Criminal)
   - Predicted IPC or CrPC sections
   - Extracted text from OCR
   - Identified entities (names, dates, locations)

5. **New Analysis**
   - Click "New Analysis" to analyze another FIR

## Project Structure

```
intelligent_fir_analyzer3/
├── backend/
│   ├── app.py                 # Main FastAPI application
│   ├── config.py              # Configuration settings
│   ├── models.py              # Database models
│   ├── schemas.py             # Pydantic schemas
│   ├── database.py            # Database connection
│   └── services/
│       ├── ocr_service.py            # OCR text extraction
│       └── classification_service.py # ML classification
├── frontend/
│   └── public/
│       ├── index.html         # Main UI
│       ├── styles.css         # Styling
│       └── app.js             # Frontend logic
├── data/
│   ├── ipc_sections.json      # IPC sections database
│   └── crpc_sections.json     # CrPC sections database
├── models/                    # Trained ML models (generated)
├── uploads/                   # Uploaded FIR images (generated)
└── requirements.txt           # Python dependencies
```

## Machine Learning Approach

### Classification Method

1. **Criminal vs Non-Criminal Classification**
   - Keyword-based matching
   - IPC section detection
   - Context analysis

2. **Section Prediction**
   - TF-IDF vectorization
   - Cosine similarity matching
   - Combined keyword and semantic scoring

3. **Entity Extraction**
   - Rule-based pattern matching
   - Named entity recognition
   - Date, time, and location extraction

### Training Data

The system uses a combination of:
- Rule-based classification with predefined keywords
- Pre-trained NLP models for semantic understanding
- IPC/CrPC section databases for mapping

## Configuration

Edit `backend/config.py` to customize:
- Upload directory paths
- Database settings
- OCR languages
- Confidence thresholds
- CORS origins

## Troubleshooting

### OCR Not Working
- Ensure EasyOCR models are downloaded (requires internet on first run)
- Check Tesseract installation if using as fallback
- Verify image quality and format

### Backend Connection Issues
- Ensure backend server is running on port 8000
- Check CORS settings in `config.py`
- Verify API_BASE_URL in `frontend/public/app.js`

### Low Classification Accuracy
- Ensure image is clear and readable
- Check if text is in English or Hindi
- Verify FIR contains sufficient information

## Future Enhancements

- [ ] Custom ML model training with real FIR datasets
- [ ] Multi-language support (regional Indian languages)
- [ ] Advanced NER models for better entity extraction
- [ ] PDF text extraction (in addition to OCR)
- [ ] Export results to PDF/Excel
- [ ] User authentication and role-based access
- [ ] Integration with police databases

## License

This project is for educational and demonstration purposes.

## Support

For issues or questions, please check the API documentation at `/docs` or review the code comments.

---

**Developed with ❤️ using FastAPI and Modern Web Technologies**

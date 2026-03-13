"""
Run the FIR Analyzer backend server
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import uvicorn
from backend.app import app
from backend.config import settings

if __name__ == "__main__":
    print(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    print(f"Server will be available at: http://{settings.HOST}:{settings.PORT}")
    print(f"API Documentation: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"Frontend: http://{settings.HOST}:{settings.PORT}/static/index.html")
    print("\nPress CTRL+C to stop the server\n")
    
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=False,
        log_level="info"
    )

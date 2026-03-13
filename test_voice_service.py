"""
Quick test script to check voice service status
"""
import sys
import requests

def test_voice_service():
    print("Testing Voice Service...")
    print("="*50)
    
    try:
        # Test voice status endpoint
        response = requests.get('http://localhost:8000/api/voice/status')
        print(f"\n✓ Server is running on port 8000")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Voice API Response:")
            print(f"  Available: {data.get('available')}")
            print(f"  Model: {data.get('model')}")
            
            if data.get('available'):
                print(f"\n✅ SUCCESS: Voice service is working!")
            else:
                print(f"\n⚠️ WARNING: Voice service loaded but not available")
                print(f"   This usually means Whisper model failed to load")
        else:
            print(f"\n❌ ERROR: Voice API returned status {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ ERROR: Cannot connect to server")
        print(f"   Make sure the server is running: python run_server.py")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":
    test_voice_service()

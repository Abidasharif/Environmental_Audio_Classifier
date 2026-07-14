import uvicorn
from main import app  # Imports your FastAPI instance from main.py

if __name__ == "__main__":
    # Hugging Face Spaces listens on port 7860 automatically
    uvicorn.run(app, host="0.0.0.0", port=7860)
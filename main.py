import os
import sys
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
# Adds the parent directory of 'src' to your Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inference import predict_environment_sound

app = FastAPI(
    title="Acoustic Environment Classification System Engine",
    description="An advanced Deep Learning API processing raw 2D audio mel spectrogram transforms to extract acoustic scene markers.",
    version="1.0.0"
)

TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "system_pipeline": "PyTorch Sound Classification Framework",
        "documentation_endpoint": "/docs"
    }

@app.post("/classify-audio/")
async def classify_audio_endpoint(file: UploadFile = File(...)):
    # Restrict input data to audio wave variants
    if not file.filename.endswith(('.wav', '.WAV')):
        raise HTTPException(status_code=400, detail="Unsupported payload formatting. Only valid uncompressed .wav audio files are accepted.")
        
    # Generate path targeting temporary execution workspace disk memory
    temp_file_path = os.path.join(TEMP_DIR, file.filename)
    
    try:
        # Buffer input stream data locally on disk
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Execute DSP and model inference tracking metrics
        results = predict_environment_sound(
            audio_path=temp_file_path,
            model_weights_path="models/best_audio_cnn.pt"
        )
        
        return {
            "filename": file.filename,
            "prediction": results["label"],
            "confidence": f"{results['confidence_score'] * 100:.2f}%",
            "class_idx": results["class_id"],
            "execution_status": "Success"
        }
        
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Pipeline operational fault encountered: {str(err)}")
        
    finally:
        # Clean up temporary upload files to prevent storage leakages
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
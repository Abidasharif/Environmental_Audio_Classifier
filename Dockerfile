# ==========================================
# 1. Base Image (Use a stable Python version)
# ==========================================
FROM python:3.10-slim

# ==========================================
# 2. System Dependencies
# ==========================================
# We install system packages required for audio processing (libsndfile is needed for Librosa/soundfile)
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# ==========================================
# 3. App Directory Setup
# ==========================================
WORKDIR /app

# ==========================================
# 4. Install Dependencies
# ==========================================
# Copying requirements first allows Docker to cache this layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ==========================================
# 5. Copy Application Files
# ==========================================
COPY . .

# ==========================================
# 6. Expose Port & Launch (Streamlit Example)
# ==========================================
# Koyeb assigns a port dynamically. We configure Streamlit to run on 8000
EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
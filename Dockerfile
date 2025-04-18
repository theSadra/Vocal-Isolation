FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy your Streamlit app
COPY demucs.py /app/demucs.py

# Install Python dependencies
RUN pip install --no-cache-dir streamlit pydub

# Install torch and demucs (CPU version)
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir demucs

EXPOSE 5000

CMD ["streamlit", "run", "demucs.py", "--server.port=5000", "--server.address=0.0.0.0"]
FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN git clone --depth 1 https://github.com/ggerganov/whisper.cpp.git /app/whisper.cpp

WORKDIR /app/whisper.cpp
RUN cmake -B build
RUN cmake --build build -j2 --config Release

RUN ./models/download-ggml-model.sh base

WORKDIR /app

COPY . .

CMD ["python", "main.py"]

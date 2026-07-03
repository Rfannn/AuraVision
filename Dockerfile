FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    portaudio19-dev \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p models

EXPOSE 5000

CMD ["python", "app.py"]

# Speaker Diarization - Docker Setup

## Prerequisites
- Docker installed on your system
- Hugging Face token set as environment variable

## Quick Start

### 1. Set up environment variable
```bash
export HF_TOKEN=your_huggingface_token_here
```

### 2. Build and run with Docker Compose (Recommended)
```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

### 3. Build and run with Docker directly
```bash
# Build the image
docker build -t speaker-diarization .

# Run the container
docker run --rm \
  -v $(pwd)/Interview.mp3:/app/Interview.mp3:ro \
  -v $(pwd)/conversation.md:/app/conversation.md \
  -e HF_TOKEN=$HF_TOKEN \
  speaker-diarization
```

## Volume Mounts
- `Interview.mp3`: Input audio file (read-only)
- `conversation.md`: Output conversation file
- `./output`: Additional output directory

## Environment Variables
- `HF_TOKEN`: Required for Hugging Face authentication

## Docker Image Details
- **Base Image**: Python 3.13-slim
- **Size**: Optimized for production
- **Dependencies**: All required packages pre-installed

## Troubleshooting
1. **HF Token Error**: Make sure to set the HF_TOKEN environment variable
2. **Audio File Not Found**: Ensure Interview.mp3 is in the same directory
3. **Permission Issues**: Check file permissions on mounted volumes

## Development
To rebuild the image after changes:
```bash
docker-compose build --no-cache
```

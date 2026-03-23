# Diarization Project

This project uses **WhisperX** to perform speech-to-text transcription with speaker diarization (identifying who spoke when).

## Features
- Audio preprocessing (conversion to mono 16kHz WAV).
- Fast transcription using WhisperX (Large-v3 model).
- Speaker diarization to identify different speakers.
- Word-level alignment for precise timestamps.
- Clean output formatted in Markdown.

## Prerequisites
- Python 3.10+
- NVIDIA GPU with CUDA (recommended) or CPU.
- FFmpeg installed on your system.
- A Hugging Face account and Access Token (HF_TOKEN) with access to:
  - `pyannote/segmentation-3.0`
  - `pyannote/speaker-diarization-3.1`

## Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd Diarization
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add your Hugging Face token:
   ```env
   HF_TOKEN=your_huggingface_token_here
   ```

## Usage

1. Place your audio file (e.g., `Interview.mp3`) in the project root.
2. Update the `audio_file` variable in `app1.py` if necessary.
3. Run the script:
   ```bash
   python app1.py
   ```
4. The diarized transcript will be saved to `conversation.md`.

## Project Structure
- `app1.py`: Main script for transcription and diarization.
- `requirements.txt`: List of Python dependencies.
- `.gitignore`: Files and folders to be excluded from Git.
- `Dockerfile` & `docker-compose.yml`: For containerized execution.

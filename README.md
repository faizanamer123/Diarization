# Diarization Project

This project uses **WhisperX** to perform speech-to-text transcription with speaker diarization (identifying who spoke when).

## Key Versions
- **Python**: 3.10+
- **WhisperX**: 3.8.1
- **PyTorch**: 2.8.0
- **Pyannote Audio**: 4.0.4
- **Transformers**: 4.57.6

## Setup & Run Commands

1. **Create & Activate Environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Hugging Face Token**:
   Create a `.env` file and add your token:
   ```env
   HF_TOKEN=your_token_here
   ```

4. **Run Transcription**:
   ```bash
   python app1.py
   ```

## Requirements
Ensure you have access to these models on Hugging Face:
- `pyannote/segmentation-3.0`
- `pyannote/speaker-diarization-3.1`

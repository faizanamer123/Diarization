import whisperx
import torch
from whisperx.diarize import DiarizationPipeline
from datetime import timedelta
import os
import gc
from dotenv import load_dotenv
from pydub import AudioSegment

original_load = torch.load
def unsafe_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return original_load(*args, **kwargs)
torch.load = unsafe_load

device = "cuda" if torch.cuda.is_available() else "cpu"
audio_file = "Interview.mp3"
output_file = "conversation.md"
model_size = "large-v3"
compute_type = "float16" if device=="cuda" else "float32"
language = "en"

min_speakers = 2
max_speakers = 2

load_dotenv()
HF_TOKEN = os.environ.get("HF_TOKEN")
if HF_TOKEN is None:
    raise ValueError("Set HF_TOKEN environment variable!")

# print("Preprocessing audio...")
# sound = AudioSegment.from_file(audio_file)
# sound = sound.set_channels(1).set_frame_rate(16000) 
# clean_audio_file = "Interview_clean.wav"
# sound.export(clean_audio_file, format="wav")

print("Preprocessing audio...")
file_ext = os.path.splitext(audio_file)[1].replace(".", "").lower()

if file_ext not in ["wav", "mp3"]:
    raise ValueError("Unsupported audio format")

sound = AudioSegment.from_file(audio_file, format=file_ext)
sound = sound.set_channels(1).set_frame_rate(16000) # mono and 16khz sample rate 
clean_audio_file = "Interview_clean.wav"
sound.export(clean_audio_file, format="wav")

print("Loading WhisperX model...")
asr_model = whisperx.load_model(model_size, device=device, compute_type=compute_type, language=language)

print("Loading audio...")
audio = whisperx.load_audio(clean_audio_file)

print("Transcribing...")
result = asr_model.transcribe(audio, batch_size=6)

gc.collect()
torch.cuda.empty_cache()

print("Loading alignment model...")
align_model, metadata = whisperx.load_align_model(language_code=language, device=device)

print("Aligning...")
result = whisperx.align(
    result["segments"],
    align_model,
    metadata,
    audio,
    device,
    return_char_alignments=True 
)

gc.collect()
torch.cuda.empty_cache()

print("Running diarization...")
diarize_model = DiarizationPipeline(use_auth_token=HF_TOKEN, device=device)
diarization = diarize_model(
    audio,
    min_speakers=min_speakers,
    max_speakers=max_speakers
)

result = whisperx.assign_word_speakers(diarization, result)

def merge_words_by_speaker(result, min_segment_duration=0.5, max_gap=1.5, allow_micro_flip=True):
    merged_segments = []
    
    # Collect all words from all segments
    all_words = []
    for segment in result.get("segments", []):
        words = segment.get("words", [])
        all_words.extend(words)
    
    if not all_words:
        return merged_segments
    
    # Sort words by start time
    all_words.sort(key=lambda x: x["start"])
    
    # Initialize first word
    current_speaker = all_words[0].get("speaker", "UNKNOWN")
    start_time = all_words[0]["start"]
    end_time = all_words[0]["end"]
    text_buffer = all_words[0]["word"]
    
    # Process remaining words
    for i in range(1, len(all_words)):
        word = all_words[i]
        speaker = word.get("speaker", "UNKNOWN")
        
        gap = word["start"] - end_time
        duration_so_far = end_time - start_time
        
        # Check if same speaker and small gap
        same_speaker = speaker == current_speaker
        small_gap = gap <= max_gap
        
        # Optional smoothing for tiny speaker flips
        micro_flip = (
            allow_micro_flip
            and not same_speaker
            and duration_so_far < min_segment_duration
        )
        
        if (same_speaker and small_gap) or micro_flip:
            # Merge word into current segment
            text_buffer += " " + word["word"]
            end_time = word["end"]
        else:
            # Close current segment
            if (end_time - start_time) >= min_segment_duration:
                merged_segments.append({
                    "speaker": current_speaker,
                    "start": start_time,
                    "end": end_time,
                    "text": text_buffer.strip()
                })
            
            # Start new segment
            current_speaker = speaker
            start_time = word["start"]
            end_time = word["end"]
            text_buffer = word["word"]
    
    # Add final segment
    if (end_time - start_time) >= min_segment_duration:
        merged_segments.append({
            "speaker": current_speaker,
            "start": start_time,
            "end": end_time,
            "text": text_buffer.strip()
        })
    
    return merged_segments

final_segments = merge_words_by_speaker(result)

def format_time(seconds):
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes}:{secs:05.2f}"

print(f"Saving to {output_file}...")

with open(output_file, "w", encoding="utf-8") as f:
    f.write("# Speaker Diarized Conversation\n\n")
    for seg in final_segments:
        start = format_time(seg["start"])
        end = format_time(seg["end"])
        f.write(f"**{seg['speaker']} ({start}-{end})**: {seg['text']}\n\n")

print("Done")

#printing diarization output
for segment in result.get("segments", []):
    words = segment.get("words", [])
    for word in words:
        speaker = word.get("speaker", "UNKNOWN")
        start = word["start"]
        end = word["end"]
        text = word["word"]
        print(f"{speaker} ({start:.2f}-{end:.2f}): {text}")
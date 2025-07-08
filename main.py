import gradio as gr
from vosk import Model, KaldiRecognizer
import wave
import json
import ffmpeg
import os
import tempfile

MODEL_PATH = "vosk-model-small-en-in-0.4"
model = Model(MODEL_PATH)

def convert_mp3_to_wav(mp3_path):
    # Create temp wav file path (we'll manage deletion manually)
    tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp_wav_path = tmp_wav.name
    tmp_wav.close()

    # ffmpeg writes output to tmp_wav_path
    ffmpeg.input(mp3_path).output(tmp_wav_path, ar=16000, ac=1, format='wav').overwrite_output().run(quiet=True)
    
    return tmp_wav_path

def transcribe_audio(file_path):
    wav_path = None
    try:
        # Convert MP3 to WAV mono 16kHz
        wav_path = convert_mp3_to_wav(file_path)

        # Now open wav file safely
        with wave.open(wav_path, "rb") as wf:
            rec = KaldiRecognizer(model, wf.getframerate())
            results = []
            
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    results.append(result.get('text', ''))
            
            final_result = json.loads(rec.FinalResult())
            results.append(final_result.get('text', ''))
        
        return ' '.join(results)

    except Exception as e:
        return f"❌ Exception: {str(e)}"

    finally:
        # Clean up temp file
        if wav_path and os.path.exists(wav_path):
            os.remove(wav_path)

# Gradio interface
iface = gr.Interface(
    fn=transcribe_audio,
    inputs=gr.Audio(sources=["upload"], type="filepath"),
    outputs="text",
    title="Vosk Speech-to-Text (MP3 Supported)",
    description="Upload MP3 (or WAV) file. It will be auto converted and transcribed."
)

iface.launch()


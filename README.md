# 🎙️ Vosk Speech-to-Text Transcription App

This project is a simple **speech-to-text transcription** tool built with:

- ✅ [Vosk](https://alphacephei.com/vosk/) for offline speech recognition (supports Indian English)
- ✅ [Gradio](https://gradio.app/) for a simple web UI
- ✅ [FFmpeg](https://ffmpeg.org/) for converting MP3 files to WAV (mono, 16kHz) — required by Vosk

---

## 🔧 Features

- Upload MP3 or WAV audio files
- Auto conversion to the format Vosk requires
- Full offline transcription using a small Indian English model
- Instant transcription output in your browser

---

## 🚀 How to Run

### 1. Install Requirements

Make sure Python 3.8+ is installed. Then run:

```bash
pip install vosk gradio ffmpeg-python

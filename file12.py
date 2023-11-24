import assemblyai as aai
import pyttsx3
import sounddevice as sd
import numpy as np

# Replace with your AssemblyAI API key
aai.settings.api_key = '0e3452aa6e344a50b24677cc8c9fbf60'

# Set up pyttsx3 for text-to-speech
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0 for male, 1 for female

# Set up sounddevice for audio recording
fs = 44100  # Sample rate
duration = 5  # Recording duration in seconds

def record_audio():
    print("Recording... Speak now.")
    audio_data = sd.rec(int(fs * duration), samplerate=fs, channels=1, dtype=np.int16)
    sd.wait()
    print("Recording complete.")
    return audio_data.flatten()

def transcribe_audio(audio):
    print("Transcribing...")
    transcript = aai.Transcriber().transcribe(audio, acoustically_aligned=False)
    return transcript.text

def text_to_speech(text):
    print("Speaking...")
    engine.say(text)
    engine.runAndWait()


while True:
    # Record audio
    audio_input = record_audio()

    # Transcribe speech to text
    transcribed_text = transcribe_audio(audio_input)
    print("You said:", transcribed_text)

    # Convert text to speech
    text_to_speech(transcribed_text)

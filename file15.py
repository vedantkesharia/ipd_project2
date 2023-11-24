import assemblyai as aai
import pyttsx3
import sounddevice as sd
import wave

# Declare the audio_data variable
audio_data = []

# Set the recording parameters
sample_rate = 44100
channels = 2

# Create a callback function to record the audio
def callback(indata, frames, time, status):
    global audio_data
    audio_data.append(indata)

# Start recording
sd.InputStream(samplerate=sample_rate, channels=channels, callback=callback).start()

# Record for 5 seconds
duration = 5
import time
time.sleep(duration)

# Stop recording
sd.InputStream().stop()

# Save the recorded audio to a file
filename = "user_audio.wav"
with wave.open(filename, "wb") as f:
    f.setnchannels(channels)
    f.setsampwidth(2)
    f.setframerate(sample_rate)
    for data in audio_data:
        f.writeframes(data)

# Perform speech-to-text
transcriber = aai.Transcriber()
transcript = transcriber.transcribe(filename)
transcribed_text = transcript.text

# Print the transcript
print(transcribed_text)

# Perform text-to-speech
engine = pyttsx3.init()
engine.say(transcribed_text)
engine.runAndWait()

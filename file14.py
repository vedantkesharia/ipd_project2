import assemblyai as aai
import pyttsx3
import sounddevice as sd
import wavio
from pydub import AudioSegment
from pydub.playback import play
import pyaudio
import wave
# import base64


aai.settings.api_key = "0e3452aa6e344a50b24677cc8c9fbf60"


def record_audio(audio_path):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
    print("Start recording...")

    frames = []
    seconds = 3
    for i in range(0,int(RATE/CHUNK*seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("recording stopped")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open("new_file.wav",'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Convert audio to WAV format
def convert_to_wav(input_file, output_file):
    audio = AudioSegment.from_mp3(input_file)
    audio.export(output_file, format="wav")

# Transcribe audio file
def transcribe_audio(file_url):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_url)
    return transcript.text

# Text-to-speech
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    # Set the file paths
    audio_file_path = "new_file.wav"
    # wav_file_path = "recorded_audio.wav"

    # Record audio and save as MP3
    record_audio(audio_file_path)

    # Convert MP3 to WAV
    # convert_to_wav(audio_file_path, wav_file_path)

    # Transcribe and print the text
    transcribed_text = transcribe_audio(audio_file_path)
    print("Transcribed Text:", transcribed_text)

    # Perform text-to-speech
    text_to_speech(transcribed_text)









# import assemblyai as aai
# import pyttsx3
# import sounddevice as sd
# import wave

# # Set the recording parameters
# sample_rate = 44100
# channels = 2

# # Create a callback function to record the audio
# def callback(indata, frames, time, status):
#     global audio_data
#     audio_data += indata

# # Start recording
# sd.InputStream(samplerate=sample_rate, channels=channels, callback=callback).start()

# # Record for 5 seconds
# duration = 5
# import time
# time.sleep(duration)

# # Stop recording
# sd.InputStream().stop()

# # Save the recorded audio as a WAV file
# filename = "user_audio.wav"
# with wave.open(filename, "wb") as f:
#     f.setnchannels(channels)
#     f.setsampwidth(2)
#     f.setframerate(sample_rate)
#     f.writeframes(audio_data)

# # Perform speech-to-text
# transcriber = aai.Transcriber()
# transcript = transcriber.transcribe(filename)
# transcribed_text = transcript.text

# # Print the transcript
# print(transcribed_text)

# # Perform text-to-speech
# engine = pyttsx3.init()
# engine.say(transcribed_text)
# engine.runAndWait()















# import assemblyai as aai
# import openai
# import elevenlabs
# import time

# aai.settings.api_key = '0e3452aa6e344a50b24677cc8c9fbf60'
# openai.api_key = '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'
# elevenlabs.set_api_key("b1e7bbd0483eb716952454564cb1e028") 

# def transcribe_audio_file(file_url):
#     transcriber = aai.Transcriber()
#     transcript = transcriber.transcribe(file_url)
#     return transcript.text

# def generate_response_and_play(audio_text):
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": 'You are a highly skilled AI, answer the questions given within a maximum of 200 characters.'},
#             {"role": "user", "content": audio_text}
#         ]
#     )


#     ai_text = response['choices'][0]['message']['content']

#     audio = elevenlabs.generate(text=ai_text, voice="Bella")
#     print("\nAI:", ai_text)
#     elevenlabs.play(audio)


# file_url = "user_audio.wav"


# transcript_result = transcribe_audio_file(file_url)


# generate_response_and_play(transcript_result)

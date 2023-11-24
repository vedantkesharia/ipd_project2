import assemblyai as aai
import pyttsx3


aai.settings.api_key = f"0e3452aa6e344a50b24677cc8c9fbf60"


FILE_URL = "user_audio.wav"

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(FILE_URL)
print(transcript.text)

transcribed_text = transcript.text


engine = pyttsx3.init()
engine.say(transcribed_text)
engine.runAndWait()
















# import assemblyai as aai


# aai.settings.api_key = f"0e3452aa6e344a50b24677cc8c9fbf60"


# FILE_URL = "user_audio.wav"


# transcriber = aai.Transcriber()
# transcript = transcriber.transcribe(FILE_URL)

# print(transcript.text)

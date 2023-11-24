import openai
import pyttsx3
import os
import json
import requests
from pydub import AudioSegment

personality = "p.txt"
usewhisper = True
key = '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'

# OpenAI set-up
openai.api_key = key
with open(personality, "r") as file:
    mode = file.read()
messages = [{"role": "system", "content": f"{mode}"}]

# pyttsx3 setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0 for male, 1 for female

def transcribe_audio(audio_path):
    url = "https://api.openai.com/v1/engines/whisper-1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }
    audio = AudioSegment.from_wav(audio_path)
    audio.export("speech.flac", format="flac")
    with open("speech.flac", "rb") as f:
        audio_data = f.read()

    response = requests.post(url, headers=headers, json={
        "prompt": "",
        "max_tokens": 512,
        "n": 1,
        "stop": None,
        "temperature": 0.7,
        "audio": audio_data
    })

    result = response.json()
    user_input = result['choices'][0]['text']
    return user_input

def save_conversation(save_foldername):
    os.makedirs(save_foldername, exist_ok=True)
    base_filename = 'conversation'
    suffix = 0
    filename = os.path.join(save_foldername, f'{base_filename}_{suffix}.txt')

    while os.path.exists(filename):
        suffix += 1
        filename = os.path.join(save_foldername, f'{base_filename}_{suffix}.txt')

    with open(filename, 'w') as file:
        json.dump(messages, file, indent=4)

    return suffix

def save_inprogress(suffix, save_foldername):
    os.makedirs(save_foldername, exist_ok=True)
    base_filename = 'conversation'
    filename = os.path.join(save_foldername, f'{base_filename}_{suffix}.txt')

    with open(filename, 'w') as file:
        json.dump(messages, file, indent=4)


script_dir = os.path.dirname(os.path.abspath(__file__))
foldername = "voice_assistant"
save_foldername = os.path.join(script_dir, f"conversations/{foldername}")
suffix = save_conversation(save_foldername)

while True:
    audio_path = "speech.wav"  # Ensure "speech.wav" contains the recorded audio
    user_input = transcribe_audio(audio_path)

    messages.append({"role": "user", "content": user_input})

    completion = openai.Completion.create(
        engine="davinci",
        prompt=messages,
        max_tokens=50
    )

    response = completion.choices[0].text
    messages.append({"role": "assistant", "content": response})
    print(f"\n{response}\n")
    save_inprogress(suffix, save_foldername)

    engine.say(f'{response}')
    engine.runAndWait()











# import openai
# import pyttsx3
# import os
# import json
# import requests
# from pydub import AudioSegment

# personality = "p.txt"
# usewhisper = True
# key = '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'

# # openAI set-up
# openai.api_key = key
# with open(personality, "r") as file:
#     mode = file.read()
# messages = [{"role": "system", "content": f"{mode}"}]

# # pyttsx3 setup
# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)  # 0 for male, 1 for female

# def transcribe_audio(audio_path):
#     url = "https://api.openai.com/v1/engines/whisper-1/completions"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {key}"
#     }
#     audio = AudioSegment.from_wav(audio_path)
#     audio.export("speech.flac", format="flac")
#     with open("speech.flac", "rb") as f:
#         audio_data = f.read()

#     response = requests.post(url, headers=headers, json={
#         "prompt": "",
#         "max_tokens": 512,
#         "n": 1,
#         "stop": None,
#         "temperature": 0.7,
#         "audio": audio_data
#     })

#     result = response.json()
#     user_input = result['choices'][0]['text']
#     return user_input

# def save_conversation(save_foldername):
#     os.makedirs(save_foldername, exist_ok=True)
#     base_filename = 'conversation'
#     suffix = 0
#     filename = os.path.join(save_foldername, f'{base_filename}_{suffix}.txt')

#     while os.path.exists(filename):
#         suffix += 1
#         filename = os.path.join(save_foldername, f'{base_filename}_{suffix}.txt')

#     with open(filename, 'w') as file:
#         json.dump(messages, file, indent=4)

#     return suffix

# def save_inprogress(suffix, save_foldername):
#     os.makedirs(save_foldername, exist_ok=True)
#     base_filename = 'conversation'
#     filename = os.path.join(save_foldername, f'{base_filename}_{suffix}.txt')

#     with open(filename, 'w') as file:
#         json.dump(messages, file, indent=4)


# script_dir = os.path.dirname(os.path.abspath(__file__))
# foldername = "voice_assistant"
# save_foldername = os.path.join(script_dir, f"conversations/{foldername}")
# suffix = save_conversation(save_foldername)


# while True:


#     audio_path = "speech.wav"
#     user_input = transcribe_audio(audio_path)

#     messages.append({"role": "user", "content": user_input})

#     completion = openai.Completion.create(
#         engine="davinci",
#         prompt=messages,
#         max_tokens=50
#     )

#     response = completion.choices[0].text
#     messages.append({"role": "assistant", "content": response})
#     print(f"\n{response}\n")
#     save_inprogress(suffix, save_foldername)

#     engine.say(f'{response}')
#     engine.runAndWait()

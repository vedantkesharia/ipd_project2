import openai
import pyttsx3
import os
import json
import requests
import pyaudio
import base64

# Your OpenAI API key and personality
key = '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'
personality = 'You are a helpful voice assistant.'

# OpenAI setup
openai.api_key = key
# os.environ["OPENAI_API_KEY"] = "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"
messages = [{"role": "system", "content": personality}]

# pyttsx3 setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0 for male, 1 for female

def record_audio(audio_path):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")

    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with open(audio_path, 'wb') as wf:
        wf.write(b''.join(frames))

def transcribe_audio(audio_path):
    url = "https://api.openai.com/v1/engines/whisper-1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }

    with open(audio_path, "rb") as f:
        audio_data = f.read()

    audio_base64 = base64.b64encode(audio_data).decode('utf-8')

    response = requests.post(url, headers=headers, json={
        "prompt": "",
        "max_tokens": 512,
        "n": 1,
        "stop": None,
        "temperature": 0.7,
        "audio": audio_base64  # Use base64-encoded audio data
    })

    result = response.json()
    if 'choices' in result and len(result['choices']) > 0:
        user_input = result['choices'][0]['message']['content']
    else:
        user_input = "Sorry, I couldn't understand your audio."

    return user_input

def save_conversation(save_foldername, conversation):
    os.makedirs(save_foldername, exist_ok=True)
    base_filename = 'conversation'
    suffix = 0
    filename = os.path.join(save_foldername, f'{base_filename}_{suffix}.json')

    while os.path.exists(filename):
        suffix += 1
        filename = os.path.join(save_foldername, f'{base_filename}_{suffix}.json')

    with open(filename, 'w') as file:
        json.dump(conversation, file, indent=4)

    return suffix

# Add an exit condition
exit_commands = ["exit", "quit", "stop"]

while True:
    audio_path = "speech.wav"
    record_audio(audio_path)
    user_input = transcribe_audio(audio_path)

    messages.append({"role": "user", "content": user_input})

    completion = openai.Completion.create(
        engine="davinci",
        messages=messages,
        max_tokens=50
    )

    response = completion.choices[0].message["content"]
    messages.append({"role": "assistant", "content": response})

    # Exit condition
    if any(command in user_input.lower() for command in exit_commands):
        break

    print(f"\nAssistant: {response}\n")

    engine.say(response)
    engine.runAndWait()

# Save the conversation
script_dir = os.path.dirname(os.path.abspath(__file__))
foldername = "voice_assistant"
save_foldername = os.path.join(script_dir, f"conversations/{foldername}")
save_conversation(save_foldername, messages)


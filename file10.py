import openai
import assemblyai as aai
import pyttsx3
import os
import json

personality = "p.txt"
usewhisper = True
key = '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'
assemblyai_token = 'your-assemblyai-token'  # Replace with your AssemblyAI API token

# openAI set-up
openai.api_key = key
with open(personality, "r") as file:
    mode = file.read()
messages = [{"role": "system", "content": f"{mode}"}]

# pyttsx3 setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0 for male, 1 for female

# AssemblyAI setup
aai.settings.api_key = assemblyai_token

# Save conversation setup
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

# grab script location
script_dir = os.path.dirname(os.path.abspath(__file__))
foldername = "voice_assistant"
save_foldername = os.path.join(script_dir, f"conversations/{foldername}")
suffix = save_conversation(save_foldername)

# main while loop where the conversation occurs
while True:
    # Replace this with your actual audio input mechanism
    # For example, using a microphone or loading an audio file
    audio_data = get_audio_input()

    if usewhisper:
        # Use AssemblyAI for voice recognition
        result = aai.Transcriber().transcribe(audio_data)
        user_input = result.text
    else:
        # Replace with your preferred speech recognition method
        user_input = recognize_speech(audio_data)

    messages.append({"role": "user", "content": user_input})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=messages,
        temperature=0.8
    )

    response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": response})
    print(f"\n{response}\n")
    save_inprogress(suffix, save_foldername)

    engine.say(f'{response}')
    engine.runAndWait()

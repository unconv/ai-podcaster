#!/usr/bin/env python3

from elevenlabs import generate, set_api_key, save, RateLimitError
import subprocess
import random
import openai
import time
import json
import sys
import os

elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
# OpenAI imports environment variable OPENAI_API_KEY by default

if elevenlabs_key:
    set_api_key(elevenlabs_key)

print("## AI-Podcaster by Unconventional Coding ##\n")

if len(sys.argv) > 1:
    with open(sys.argv[1]) as f:
        podcast_description = f.read().strip()
else:
    podcast_description = input("What is the podcast about?\n")
    print()

if len(sys.argv) > 2:
    dialog_count = int(sys.argv[2])
else:
    dialog_count = int(input("How many dialogs do you want? [5]\n") or "5")

if not os.path.exists("dialogs"):
    os.mkdir("dialogs")

if not os.path.exists("podcasts"):
    os.mkdir("podcasts")

voice_names = {
    "male": [
        "Adam",
        "Antoni",
        "Arnold",
        "Callum",
        "Charlie",
        "Clyde",
        "Daniel",
        "Ethan",
    ],
    "female": [
        "Bella",
        "Charlotte",
        "Domi",
        "Dorothy",
        "Elli",
        "Emily",
        "Gigi",
        "Grace",
    ]
}

voices = {}

def get_voice(name, gender):
    if name not in voices:
        voices[name] = random.choice(voice_names[gender])
        voice_names[gender].remove(voices[name])
    return voices[name]

messages = [
    {
        "role": "system",
        "content": "You are a podcast generator. Generate the dialog for a podcast based on the description given by the user.",
    },
    {
        "role": "user",
        "content": podcast_description,
    }
]

podcast_id = f"{time.time()}"

def generate_dialog(number_of_dialogs):
    transcript_file_name = f"podcasts/podcast{podcast_id}.txt"
    transcript_file = open(transcript_file_name, "w")

    dialogs = []

    for _ in range(0, number_of_dialogs):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=[
                {
                    "name": "add_dialog",
                    "description": "Add dialog to the podcast",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "speaker": {
                                "type": "string",
                                "description": "The name of the speaker"
                            },
                            "gender": {
                                "type": "string",
                                "description": "The gender of the speaker (male of female)"
                            },
                            "content": {
                                "type": "string",
                                "description": "The content of the speech"
                            }
                        },
                        "required": ["speaker", "gender", "content"]
                    }
                }
            ],
            function_call={
                "name": "add_dialog",
                "arguments": ["speaker", "gender", "content"]
            }
        )

        message = response["choices"][0]["message"] # type: ignore

        messages.append(message)

        function_call = message["function_call"]
        arguments = json.loads(function_call["arguments"])

        transcript_file.write(arguments['speaker'] + " says: " + arguments['content'] + "\n")

        dialogs.append(arguments)

    transcript_file.close()
    return (dialogs, transcript_file_name)


dialog_files = []
concat_file = open("concat.txt", "w")

print("Generating transcript")

dialogs, transcript_file_name = generate_dialog(dialog_count)

print("Generating audio")
try:
    for i, dialog in enumerate(dialogs):
        audio = generate(
            text=dialog["content"],
            voice=get_voice(dialog["speaker"], dialog["gender"].lower()),
            model="eleven_monolingual_v1"
        )

        filename = f"dialogs/dialog{i}.wav"
        concat_file.write("file " + filename + "\n")
        dialog_files.append(filename)

        save(audio, filename) # type: ignore
except RateLimitError:
    print("ERROR: ElevenLabs ratelimit exceeded!")

concat_file.close()

podcast_file = f"podcasts/podcast{podcast_id}.wav"

print("Concatenating audio")
subprocess.run(f"ffmpeg -f concat -safe 0 -i concat.txt -c copy {podcast_file}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

os.unlink("concat.txt")

for file in dialog_files:
    os.unlink(file)

print("\n## Podcast is ready! ##")
print("Audio: " + podcast_file)
print("Transcript: " + transcript_file_name)

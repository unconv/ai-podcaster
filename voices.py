#!/usr/bin/env python3

import os
from dotenv import load_dotenv
import elevenlabs
 
 
# Set the ElevenLabs API key.
load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")
 
elevenlabs.set_api_key(api_key)
 
voices_file = open("voices.csv", "w")

# Fetch and write out the id and name of the voice
# NOTE: elevenlabs.voices() returns a pydantic object type
voices = elevenlabs.voices()
for voice in voices:
    print(f'"{voice.name}","{voice.voice_id}","{voice.category}"')
    voices_file.write(f'"{voice.name}","{voice.voice_id}","{voice.category}"\n')
voices_file.close()

# to print out the model
print_voice_object_model = False
if print_voice_object_model:
    print(voices[0].model_dump_json)

# to print a field inside the model
print_voice_object_model_field = False
if print_voice_object_model_field:
    print(voices[0].labels.get("gender"))

# to print all fields on the voice object
print_all_voice_object_fields = False
if print_all_voice_object_fields:
    for field in dir(voices[0]):
        print(field)

# print the number of voices returned from the API call
print(f"len(voices): {len(voices)}")
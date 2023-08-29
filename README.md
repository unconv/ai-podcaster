# AI-Podcaster

Create podcasts about any subject using ChatGPT and ElevenLabs.

## Quick Start

```shell
$ ./ai_podcaster.py [INPUT_FILE] [DIALOG_COUNT]
```

Input file should be a text file with a description of the podcast you want to create. Dialog count determines the length of the podcast.

You can run the script without command line arguments and it will ask you to input them instead.

## API Keys

You need to put your OpenAI API key and ElevenLabs API key into the environment variables `OPENAI_API_KEY` and `ELEVENLABS_API_KEY`:

```shell
$ export OPENAI_API_KEY=YOUR_OPENAI_API_KEY
$ export ELEVENLABS_API_KEY=YOUR_ELEVENLABS_API_KEY
```

Enjoy! (and [buy me a coffee](https://buymeacoffee.com/unconv))

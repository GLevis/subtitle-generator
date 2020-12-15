import io
import os
import os.path
from moviepy.editor import *
from google.cloud import speech
from os import path

while True:
    video = input("video filename: ")
    if not path.exists(video):
        print("invalid filename, please try again.")
        continue
    else:
        break

file_name = video.strip('.')[0] + ".wav"
audioclip = AudioFileClip(video)
if not path.exists(file_name):
    audioclip.write_audiofile(file_name, verbose=True, write_logfile=True)

client = speech.SpeechClient()

with io.open(file_name, "rb") as audio_file:
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=44100,
    language_code="en-US",
    audio_channel_count=2,
)
response = client.recognize(config=config, audio=audio)

transcript = ""
for result in response.results:
    transcript += result.alternatives[0].transcript

print("Transcript: {}".format(transcript))

while True:
    choice = input("Would you like to save the transcript as a text document? (y\\n)")
    print(choice)
    if choice == "y" or choice == "n":
        break
    else:
        print("Please enter either y or n.")
        continue

if(choice == 'y'):
    f = open("transcript.txt", "x")
    f.write(transcript)
    f.close()

print("Goodbye!")

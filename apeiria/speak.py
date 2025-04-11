import json
import requests
import wave
import os
from time import sleep
from playsound import playsound
import pykakasi
import voice

kakasi = pykakasi.kakasi()

class Speak(object):
    def speak_voice(self, input):
        name = ''.join([item['hepburn'] for item in kakasi.convert(input)])
        new_name = ''.join(char for char in name if char.isalnum())

        text = input
        voice_dir = os.path.join("apeiria", "voice")
        wav_path = os.path.join(voice_dir, new_name + ".wav")
        print(wav_path)
        if os.path.exists(wav_path):
            playsound(wav_path)
        else:
            voice.Momory.newspeak(self, text, new_name)

import json
import requests
import wave
import os
from time import sleep
from playsound import playsound
import pykakasi
import os
import voice

kakasi = pykakasi.kakasi()


class Speak(object):

    def speak_voice(self, input):
        name = ''.join([item['hepburn'] for item in kakasi.convert(input)])
        new_name = ''.join(char for char in name if char.isalnum())
        text = input
        if os.path.exists("apeiria/voice/"+new_name+".wav"):
            os.chdir('./apeiria/voice')
            playsound(new_name+".wav")
            os.chdir('../../')

        else:
            voice.Momory.newspeak(self, text, new_name)

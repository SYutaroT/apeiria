import json
import requests
import wave
import os
from time import sleep
from playsound import playsound
import shutil


class Momory(object):
    def newspeak(self, text, name):
        os.chdir("apeiria/voice")
        speaker = 47
        host = 'localhost'
        port = 50021
        params = (
            ('text', text),
            ('speaker', speaker),
        )
        response1 = requests.post(
            f'http://{host}:{port}/audio_query',
            params=params
        )
        headers = {'Content-Type': 'application/json', }
        response2 = requests.post(
            f'http://{host}:{port}/synthesis',
            headers=headers,
            params=params,
            data=json.dumps(response1.json())
        )

        wf = wave.open("audio"+".wav", 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(response2.content)
        wf.close()

        os.rename("audio"+".wav", name+".wav")
        playsound(name + ".wav")
        os.chdir("../../")

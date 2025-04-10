import json
import requests
import wave
import os
from time import sleep
from playsound import playsound
from pathlib import Path


class Momory(object):
    def newspeak(self, text, name):
        # 絶対パスで voice フォルダを取得
        base_path = Path(__file__).resolve().parent
        voice_dir = base_path / "voice"
        voice_dir.mkdir(exist_ok=True)  # 存在しなければ作成

        speaker = 47
        host = 'localhost'
        port = 50021

        params = (
            ('text', text),
            ('speaker', speaker),
        )

        # VOICEVOXに音声合成要求
        response1 = requests.post(
            f'http://{host}:{port}/audio_query',
            params=params
        )
        response1.raise_for_status()

        headers = {'Content-Type': 'application/json'}
        response2 = requests.post(
            f'http://{host}:{port}/synthesis',
            headers=headers,
            params=params,
            data=json.dumps(response1.json())
        )
        response2.raise_for_status()

        # 音声ファイル保存
        output_path = voice_dir / f"{name}.wav"
        with wave.open(str(output_path), 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            wf.writeframes(response2.content)

        # 再生
        playsound(str(output_path))

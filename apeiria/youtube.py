import vlc
from time import sleep
from yt_dlp import YoutubeDL
import os
from pathlib import Path
import mainWindow
from pynput import keyboard


class Player:
    def MP4_saisei():
        musiclist = []
        for p in Path("apeiria/move").rglob("*.mp4"):
            musiclist.append(str(p))
        player = vlc.MediaListPlayer()
        mediaList = vlc.MediaList(musiclist)
        player.set_media_list(mediaList)
        player.set_playback_mode(vlc.PlaybackMode.loop)
        player.play()
        sleep(5)
        data = input()
        while player.is_playing():
            if data == "d":
                player.stop()
                os.chdir("../../")
                break


class Download:
    def youtube_dl(self, url):
        os.chdir("apeiria/move")
        ydl_opts = {'format': 'best'}
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([url])
        os.chdir("../../")
        print(result)

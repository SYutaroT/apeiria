from pynput import keyboard
import vlc
from pathlib import Path
from time import sleep


def on_press(key):
    print(key)
    if key == keyboard.Key.esc:
        exit()
    elif key == keyboard.Key.f9:
        player.next()
    elif key == keyboard.Key.f8:
        player.pause()
    elif key == keyboard.Key.f7:
        player.previous()


    # Collect events until released
mplayer = vlc.Instance()
musiclist = mplayer.media_list_new()
for p in Path("apeiria/move").rglob("*.mp4"):
    media = mplayer.media_new(p)
    musiclist.add_media(media)
print(musiclist)
player = vlc.MediaListPlayer()
mediaList = vlc.MediaList(musiclist)
player.set_media_list(mediaList)
player.set_playback_mode(vlc.PlaybackMode.loop)
player.play()

with keyboard.Listener(
        on_press=on_press) as listener:
    listener.join()

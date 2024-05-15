import vlc
from pathlib import Path
from time import sleep
import vlc
import threading
import keybord
from pynput import keyboard
import music

musicInterrupt = threading.Thread(target="apeiria/music.py")
KeyboardInterrupt = threading.Thread(target=keybord.Keyboard)
musicInterrupt.start()
KeyboardInterrupt.start()

data = keybord.Keyboard

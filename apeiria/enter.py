from pynput import keyboard
import pyautogui


def on_press(key):
    if key == keyboard.Key.enter:
        print('Enter pressed')
        t = pyautogui.locateOnScreen('apeiria/img/talk.jpg', confidence=0.9)
        if t is not None:
            pyautogui.click(t)
    try:

        print('Alphanumeric key pressed: {0} '.format(
            key.char))

    except AttributeError:
        print('special key pressed: {0}'.format(
            key))
    


with keyboard.Listener(
        on_press=on_press) as listener:
    listener.join()

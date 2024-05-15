import speech_recognition as sr
import sys
import tkinter
from time import sleep

r = sr.Recognizer()
mic = sr.Microphone()
while True:
    print("話しかけてください")
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    print("認識中")
    try:
        t = r.recognize_google(audio, language='ja-JP')
        if str(t) == "終了":
            break
    except:
        t = "もう一度お願いします"

    root = tkinter.Tk()
    Static1 = tkinter.Label(root, text=t)
    Static1.pack()
    root.mainloop()
    # mainWindow.MainWindow.set_text(self, t)

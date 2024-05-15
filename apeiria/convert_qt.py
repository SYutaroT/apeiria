from PyQt5 import uic
import shutil

fin = open("apeiria/qt_Apeiria.ui", "r", encoding="UTF-8")
fout = open("apeiria/qt_ApeiriaUI.py", "w", encoding="UTF-8")
uic.compileUi(fin, fout)
fout.close()

import sys
from PyQt5 import QtWidgets
import mainWindow
import subprocess
from getpass import getpass
import tkinter as tk

import ctypes


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# if not is_admin():
#     # Re-run the program with admin rights and exit the original
#     ctypes.windll.shell32.ShellExecuteW(
#         None, "runas", sys.executable, " ".join(sys.argv), None, 1)
#     sys.exit(0)

# 以下のコードは管理者権限で実行される
# subprocess.Popen(
#     r"C:\\Users\\sachy\\AppData\\Local\\Programs\\VOICEVOX\\VOICEVOX.exe")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = mainWindow.MainWindow()
    win.show()
    ret = app.exec_()
    sys.exit(ret)

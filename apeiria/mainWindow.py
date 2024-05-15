from PyQt5 import QtWidgets
from PyQt5 import QtGui
import qt_ApeiriaUI
import apeiria
import datetime
import is_weather
import analyzer
import speak
import youtube
import tkinter as tk
import subprocess
from subprocess import PIPE
root = tk.Tk()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.apeiria = apeiria.Apeiria("apeiria")
        self.action = True
        self.ui = qt_ApeiriaUI.Ui_MainWindow()
        self.weather = is_weather.WeatherResponder()
        self.youtube = youtube.Player()
        self.download = youtube.Download()
        self.ui.setupUi(self)
        self.log = []
        self.question_we = False
        self.question_mp4 = False
        self.question_down = False
        self.speak = speak.Speak()

    def putlog(self, str):
        self.ui.listWidget.addItem(str)
        self.log.append(str+"\n")

    def prompt(self):
        p = self.apeiria.get_name()
        if self.action == True:
            p += ":"+self.apeiria.get_responder_name()
        return p+">"
#!表情

    def change_looks(self):
        em = self.apeiria.emotion.mood
        print("em:", em)

        # *デフォルト
        if -15 <= em <= 5:
            self.ui.labelemotion.setPixmap(QtGui.QPixmap(None))
        # *照れ
        elif 5 < em < 10:
            self.ui.labelemotion.setPixmap(QtGui.QPixmap(":/re/てれる.png"))
        # *すごく照れる
        elif 10 <= em <= 15:
            self.ui.labelemotion.setPixmap(QtGui.QPixmap(":/re/すごくてれる.png"))

    def change_fice(self, input):
        fc=input
        print("fc:", fc)
        if fc == "0":
            self.ui.labelexpression.setPixmap(QtGui.QPixmap("None"))
        elif fc == "1":
            print("Yes")
            self.ui.labelexpression.setPixmap(QtGui.QPixmap(":/re/いかり.png"))
        elif fc == "2":
            self.ui.labelexpression.setPixmap(QtGui.QPixmap(":/re/おどろき.png"))
        elif fc == "3":
            self.ui.labelexpression.setPixmap(QtGui.QPixmap(":/re/かなしい.png"))
        elif fc == "4":
            self.ui.labelexpression.setPixmap(QtGui.QPixmap(":/re/すごい.png"))
        elif fc == "5":
            self.ui.labelexpression.setPixmap(QtGui.QPixmap(":/re/ねむい.png"))
        elif fc == "6":
            self.ui.labelexpression.setPixmap(QtGui.QPixmap(":/re/ほほえみ.png"))
        elif fc == "7":
            self.ui.labelexpression.setPixmap(QtGui.QPixmap(":/re/ゆううつ.png"))
        elif fc == "8":
            self.ui.labelexpression.setPixmap(QtGui.QPixmap(":/re/こまる.png"))
        elif fc == "9":
            self.ui.labelexpression.setPixmap(
                QtGui.QPixmap(":/re/すこしおどろき.png"))
        elif fc == "10":
            self.ui.labelexpression.setPixmap(QtGui.QPixmap(":/re/あきれ.png"))

    def writeLog(self):
        now = "Apeiria System Dialogue Log:" + \
            datetime.datetime.now().strftime("%Y-%m-%d %H:%m:%S")+"\n"
        self.log.insert(0, now)
        with open("apeiria/dics/log.txt", "a", encoding="utf-8") as f:
            f.writelines(self.log)

    def buttonTalkSolt(self):
        value = self.ui.lineEdit.text()
        if not value:
            self.ui.labelResponce.setText("なんでしょうか？")
            fc = "5"
        elif value == "天気予報":
            if self.question_we == False:
                self.ui.labelResponce.setText("どこの天気が知りたいですか?")
                self.question_we = True
                self.ui.lineEdit.clear()
                fc = "5"
        elif self.question_we == True:
            response = self.weather.is_weather(value)
            self.ui.labelResponce.setText(response)
            self.question_we = False
            self.ui.lineEdit.clear()
        elif value == "動画":
            if self.question_mp4 == False:
                self.ui.labelResponce.setText("なにが見たいですか?")
                self.question_mp4 = True
                self.ui.lineEdit.clear()
                fc = "5"
                response2="何が見たいですか"
        elif self.question_mp4 == True:

            subprocess.Popen(['python', 'apeiria/keymusic.py'],
                             stdout=PIPE, stderr=PIPE)
            self.question_mp4 = False
            self.ui.lineEdit.clear()
            # self.youtube.MP4_saisei(value)

            fc = "5"
        elif value == "ダウンロード":
            if self.question_down == False:
                self.ui.labelResponce.setText("urlを入力してください")
                self.question_down = True
                self.ui.lineEdit.clear()
                fc = "5"
        elif self.question_down == True:
            self.download.youtube_dl(value)
            self.question_down = False
            self.ui.lineEdit.clear()
            fc = "5"
        else:
            response = self.apeiria.dialogue(value)
            talkword = response[0]
            fc = response[1]
            response2 = analyzer.keigo(talkword)
            self.ui.labelResponce.setText(response2)
            self.putlog(">"+value)
            self.putlog(self.prompt()+response2)
            self.ui.lineEdit.clear()
            print(fc)
        self.change_looks()
        self.change_fice(fc)
        self.speak.speak_voice(response2)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(
            self, "オーナー", "辞書を更新していいですか?", buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.apeiria.save()
            self.writeLog()
            event.accept()
        else:
            event.accept()

    def voiceON(self):
        self.action = False
        subprocess.Popen(['python', 'apeiria/listen.py'],
                         stdout=PIPE, stderr=PIPE)
        print("voice ON")

    def voiceOFF(self):
        self.action = True
        subprocess.Popen(['python', 'apeiria/enter.py'],
                         stdout=PIPE, stderr=PIPE)

    def set_text(self, value):
        self
        self.ui.lineEdit.setText(value)

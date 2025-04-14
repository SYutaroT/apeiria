from PyQt5 import QtWidgets
from PyQt5 import QtGui,QtCore
import qt_ApeiriaUI
import apeiria
import datetime
import is_weather
import analyzer
import speak
import sys
from shigi import syougi
# import youtube
import tkinter as tk
import subprocess
from subprocess import PIPE
import os

root = tk.Tk()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.apeiria = apeiria.Apeiria("apeiria")
        self.action = True
        self.ui = qt_ApeiriaUI.Ui_MainWindow()
        self.weather = is_weather.WeatherResponder()
        # self.youtube = youtube.Player()
        # self.download = youtube.Download()
        self.ui.setupUi(self)
        self.log = []
        self.question_we = False
        self.question_mp4 = False
        self.question_down = False
        self.speak = speak.Speak()
#!---------------------------------
        self.log_watch_process = QtCore.QProcess(self)
        self.log_watch_process.readyReadStandardOutput.connect(self.handle_log_output)

    def putlog(self, str):
        self.ui.listWidget.addItem(str)
        self.log.append(str+"\n")

    def prompt(self):
        p = self.apeiria.get_name()
        if self.action == True:
            p += ":"+self.apeiria.get_responder_name()
        return p+">"

    def change_looks(self):
        em = self.apeiria.emotion.mood
        print("em:", em)

        if -15 <= em <= 5:
            self.ui.labelemotion.setPixmap(QtGui.QPixmap(None))
        elif 5 < em < 10:
            self.ui.labelemotion.setPixmap(QtGui.QPixmap(":/re/てれる.png"))
        elif 10 <= em <= 15:
            self.ui.labelemotion.setPixmap(QtGui.QPixmap(":/re/すごくてれる.png"))

    def change_fice(self, input):
        fc=input
        print("fc:", fc)
        expressions = {
            "0": "None",
            "1": ":/re/いかり.png",
            "2": ":/re/おどろき.png",
            "3": ":/re/かなしい.png",
            "4": ":/re/すごい.png",
            "5": ":/re/ねむい.png",
            "6": ":/re/ほほえみ.png",
            "7": ":/re/ゆううつ.png",
            "8": ":/re/こまる.png",
            "9": ":/re/すこしおどろき.png",
            "10": ":/re/あきれ.png"
        }
        if fc in expressions:
            self.ui.labelexpression.setPixmap(QtGui.QPixmap(expressions[fc]))

    def writeLog(self):
        now = "Apeiria System Dialogue Log:" + datetime.datetime.now().strftime("%Y-%m-%d %H:%m:%S")+"\n"
        self.log.insert(0, now)
        with open(os.path.join("apeiria", "dics", "log.txt"), "a", encoding="utf-8") as f:
            f.writelines(self.log)

    def buttonTalkSolt(self):
        response2 = ""
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
            subprocess.Popen(['python', os.path.join('apeiria', 'keymusic.py')], stdout=PIPE, stderr=PIPE)
            self.question_mp4 = False
            self.ui.lineEdit.clear()
            fc = "5"
        elif value == "将棋":
            self.ui.labelResponce.setText("勝負です")
            self.speak.speak_voice(" ")
            self.speak.speak_voice("勝負です")
            fc = "1"
            self.ui.lineEdit.clear()
            base_dir = os.path.dirname(__file__)
            log_watch_path = os.path.abspath(os.path.join(base_dir, "Wright_AI", "log", "watch_log.py"))



            # stderrもstdoutとまとめて取得
            self.log_watch_process.setProcessChannelMode(QtCore.QProcess.MergedChannels)

            # 起動
            self.log_watch_process.start(sys.executable, [log_watch_path])

            # 起動チェック
            if not self.log_watch_process.waitForStarted(3000):  # 最大3秒待つ
                print("❌ log_watch.py の起動に失敗しました")
            else:
                print("✅ log_watch.py が正常に起動しました")
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
        subprocess.Popen(['python', os.path.join('apeiria', 'listen.py')], stdout=PIPE, stderr=PIPE)
        print("voice ON")

    def voiceOFF(self):
        self.action = True
        subprocess.Popen(['python', os.path.join('apeiria', 'enter.py')], stdout=PIPE, stderr=PIPE)

    def set_text(self, value):
        self.ui.lineEdit.setText(value)


#-------------------------------------------------------------
    def handle_log_output(self):
        output = bytes(self.log_watch_process.readAllStandardOutput()).decode("utf-8").strip()
        for line in output.splitlines():
            if line:
                self.ui.labelResponce.setText(line)
                self.putlog("log> " + line)
                print(line)
    def closeEvent(self, event):
        self.log_watch_process.kill()
        super().closeEvent(event)


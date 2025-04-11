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
        self.process = QtCore.QProcess(self)

        

        # # 将棋AIからの出力を表示するためのウィジェット（ログ表示用）を追加
        # self.shogiOutput = QtWidgets.QPlainTextEdit(self)
        # self.shogiOutput.setReadOnly(True)
        # self.ui.verticalLayout.addWidget(self.shogiOutput)
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
            python_path = sys.executable
            syougi_path = os.path.join("apeiria","Wright_AI", "shogi_gui.py")
            self.ui.lineEdit.clear()
            from PyQt5.QtCore import QProcess
            self.process = QProcess(self)  # QProcess オブジェクトを明示的に作成

            # 出力・エラー出力をハンドリング（任意）
            self.process.readyReadStandardOutput.connect(self.handle_shogi_output)
            self.process.readyReadStandardError.connect(self.handle_shogi_error)

            # 起動（コマンドラインはリストで）
            self.process.start(python_path, [syougi_path])

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

    def handle_shogi_output(self):
        output = bytes(self.process.readAllStandardOutput()).decode("utf-8").strip()
        for line in output.splitlines():
            if line.startswith("chatbot_output:"):
                content = line.replace("chatbot_output:", "").strip()

                # 例: "move=7g7f value=0.83" を分解して取得
                parts = dict(pair.split('=') for pair in content.split())
                move = parts.get("move")
                value = float(parts.get("value", 0.5))  # デフォルトは0.5に
                from_sq = move[:2]
                to_sq = move[2:4]
                self.speak.speak_voice("")
                self.ui.labelResponce.setText(f"{from_sq} から {to_sq} に指しました")
                self.speak.speak_voice(f"{from_sq} から {to_sq} に指しました")

                # チャットに表示
                print(value)
                # 勝率から疑似感情（例: 期待・不安）を処理
                if value > 0.7:
                    fc = "4"  # 喜び・強気
                    em = "15"
                elif value < 0.3:
                    fc = "3"  # 不安・悲しみ
                    em = "0"
                else:
                    fc = "5"  # 中立
                    em = "7"

                self.change_fice(fc)
                self.change_looks()
                self.speak.speak_voice(" ")
                # self.speak.speak_voice(f"{move} に指しました。現在の評価は {value:.2f} です。")

    def handle_shogi_error(self):
        error = bytes(self.process.readAllStandardError()).decode("utf-8").strip()
        # if error:
        #     self.error_label.setText(f"エラー: {error}")
        #     self.ui.labelResponce.setText(f"⚠️ エラーが発生しました：{error}")
        #     self.speak.speak_voice(" ")
        #     self.speak.speak_voice(f"エラーが発生しました。{error}")
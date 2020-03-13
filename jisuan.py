import os
from random import randint

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QHBoxLayout, QMessageBox, QDialog
import sys


# 生成静态目录
def resource_path(relative_path):
    if getattr(sys, 'frozen', False): #是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    os.path.join(base_path, "static")
    return os.path.join(base_path, relative_path)


class Result(QDialog):
    def __init__(self, status=True):
        super(Result, self).__init__()
        self.resize(200, 200)
        self.setWindowTitle("结果")
        if status:
            pix = QPixmap(resource_path("right.png"))
        else:
            pix = QPixmap(resource_path("wrong.png"))
            print(resource_path("static/wrong.png"))
        self.label = QLabel(self)
        self.label.setPixmap(pix)
        self.label.setScaledContents(True)
        self.setWindowModality(Qt.ApplicationModal)
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)



class Jisuan(QWidget):
    def __init__(self):
        super(Jisuan, self).__init__()
        self.resize(600, 400)

        style_str = "QLabel{font: bold 100px;}" \
                    "QLineEdit{font: bold 100px;}"
        self.setStyleSheet(style_str)

        self.first = QLabel("1")
        self.second = QLabel("2")
        self.add_or_reduce = QLabel("+")
        equal = QLabel("=")
        self.answer = QLineEdit()
        self.answer.returnPressed.connect(self.verify_answer)
        self.result = []
        self.index = 0

        self.create_question()

        layout = QHBoxLayout()
        layout.addWidget(self.first)
        layout.addWidget(self.add_or_reduce)
        layout.addWidget(self.second)
        layout.addWidget(equal)
        layout.addWidget(self.answer)
        layout.setSpacing(50)

        self.setLayout(layout)
        self.dialog = None
        self.dialog_timer = QTimer(self)
        self.dialog_timer.timeout.connect(self.close_dialog)

    # 答案窗口的控制关闭
    def close_dialog(self):
        self.dialog_timer.stop()
        self.dialog.close()

    def create_question(self):
        self.answer.setText("")
        if randint(0, 1):
            first = randint(0, 9)
            self.first.setText(str(first))
            self.add_or_reduce.setText("+")
            self.second.setText(str(randint(0, 10 - first)))
        else:
            first = randint(0, 10)
            self.first.setText(str(first))
            self.add_or_reduce.setText("-")
            self.second.setText(str(randint(0, first)))

    def verify_answer(self):
        first = int(self.first.text())
        second = int(self.second.text())
        add_or_reduce = self.add_or_reduce.text()
        correct = True
        try:
            answer = int(self.answer.text())
        except Exception as e:
            print(e)
            self.answer.setText("")
            self.dialog = Result(status=False)
            self.dialog.show()
            self.dialog_timer.start(2000)
        if add_or_reduce == "+":
            if answer != first + second:
                correct = False
        else:
            if answer != first - second:
                correct = False
        # 正确与否的不同处理
        if correct:
            if self.index == len(self.result):
                self.result.append(True)
            self.index += 1
            self.dialog = Result(status=True)
            self.dialog.show()
            self.dialog_timer.start(1500)
            self.create_question()
        else:
            if self.index == len(self.result):
                self.result.append(False)
            self.answer.setText("")
            self.dialog = Result(status=False)
            self.dialog.show()
            self.dialog_timer.start(1500)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("圆圆学计算")
    filename = resource_path("icon.ico")
    print(filename)
    app.setWindowIcon(QIcon(filename))
    ui = Jisuan()
    ui.show()
    sys.exit(app.exec_())
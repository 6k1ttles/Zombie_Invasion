from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication
from PyQt5.QtGui import QFont
import sys


# финальное окно
class FinalWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Game Over')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        label = QLabel('Поздравляем! Вы убили 1 королевского зараженного!')
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet('color: white; background-color: #333; border-radius: 10px; padding: 10px;')
        label.setFont(QFont('Arial', 16))
        layout.addWidget(label)

        button = QPushButton('Exit Game')
        button.clicked.connect(self.close)
        button.setStyleSheet('color: white; background-color: #555; border-radius: 15px; padding: 10px;')
        button.setFont(QFont('Arial', 14))
        layout.addWidget(button)

        self.setLayout(layout)


def final_show():
    app = QApplication(sys.argv)
    fin = FinalWindow()
    fin.show()
    sys.exit(app.exec_())

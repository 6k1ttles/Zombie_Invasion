import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QWidget, QTextBrowser


class CheatConsole(QMainWindow):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.flag = False
        self.cheatss = False
        self.setWindowTitle("Cheat Console")
        self.setGeometry(100, 100, 600, 400)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.console_output = QTextBrowser(self)
        layout.addWidget(self.console_output)
        self.console_input = QLineEdit(self)
        layout.addWidget(self.console_input)
        self.console_input.returnPressed.connect(self.process_command)

    def toggle_console(self):
        self.cheatss = not self.cheatss
        self.console_output.clear()
        if self.cheatss:
            self.console_output.append("Cheat Console: ON")
        else:
            self.console_output.append("Cheat Console: OFF")

    def process_command(self):
        command = self.console_input.text()
        self.console_input.clear()
        self.console_output.append(f"Command entered: {command}")
        if command.lower() == "god_mode_on":
            self.player.speed *= 5
            self.console_output.append("GOD MOD ACTIVATED")
            self.flag = True
        elif command.lower() == "god_mode_off":
            self.console_output.append("GOD MOD DEACTIVATED")
            self.player.speed /= 5
        else:
            self.console_output.append("Invalid command")


def cheats_mode(player):
    app = QApplication(sys.argv)

    cheats = CheatConsole(player)
    cheats.show()
    cheats.toggle_console()
    if cheats.flag:
        sys.exit(app.exec_())

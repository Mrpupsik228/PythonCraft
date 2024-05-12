from PyQt5 import QtCore, QtWidgets
from re import sub as regex_sub
from network.server import *

DEFAULT_PORT = 25565

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.resize(662, 415)

        self.server = Server()

        self.centralwidget = QtWidgets.QWidget(self)
        self.central_layout = QtWidgets.QHBoxLayout(self.centralwidget)

        self.player_list = QtWidgets.QListView(self.centralwidget)
        self.player_list.setMaximumSize(QtCore.QSize(180, 16777215))

        self.central_layout.addWidget(self.player_list)
        self.console = QtWidgets.QWidget(self.centralwidget)

        self.console_layout = QtWidgets.QVBoxLayout(self.console)
        self.console_layout.setContentsMargins(0, 0, 0, 0)
        self.console_layout.setSpacing(0)

        self.port_input = QtWidgets.QLineEdit(self.console)
        self.port_input.setPlaceholderText(str(DEFAULT_PORT))
        self.port_input.textChanged.connect(self.on_port_input_text_changed)

        self.start_button = QtWidgets.QPushButton(self.console)
        self.start_button.clicked.connect(self.on_start_button_pressed)

        self.update_start_button_text()

        self.console_layout.addWidget(self.start_button)
        self.central_layout.addWidget(self.console)

        self.setCentralWidget(self.centralwidget)
    
    def on_start_button_pressed(self) -> None:
        if self.server.is_running():
            self.server.stop()
        else:
            if len(self.port_input.text()) > 0:
                print(int(self.port_input.text()))
            self.server.start(DEFAULT_PORT if len(self.port_input.text()) == 0 else int(self.port_input.text()))
        
        self.update_start_button_text()
    
    def on_port_input_text_changed(self) -> None:
        self.port_input.setText(regex_sub(r'[^0-9]', '', self.port_input.text()))
    
    def update_start_button_text(self) -> None:
        self.start_button.setText('Stop' if self.server.is_running() else 'Start')

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()
    
    app.exec()

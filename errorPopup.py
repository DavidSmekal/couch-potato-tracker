from PyQt5.QtWidgets import QMessageBox

# I could have the function take an int, and change the type of error
def show_error_pop_up():
    print("DELETE PRESSED")
    msg = QMessageBox()
    msg.setStyleSheet(open("stylesheet.qss", "r").read())

    msg.setText("This is a message boxThis is a message boxThis is a message boxThis is a message box")
    msg.setWindowTitle("Error")
    msg.setObjectName("background")
    msg.exec_()

    #msg.clicked.connect(self.show_error_pop_up)
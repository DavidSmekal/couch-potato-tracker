from PyQt5.QtWidgets import QMessageBox

# Shows an error popup dialogue box
# Method takes an int, which will change the type of error
def show_error_pop_up(code):
    print("DELETE PRESSED")
    msg = QMessageBox()
    msg.setStyleSheet(open("stylesheet.qss", "r").read())

    if code == 1:
        msg.setText("Stock doesn't exist")

    msg.setWindowTitle("Error")
    msg.setObjectName("background")
    msg.exec_()
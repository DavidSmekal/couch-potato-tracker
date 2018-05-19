from PyQt5.QtWidgets import QMessageBox

# Shows an error popup dialogue box
# Method takes an int, which will change the type of error
def show_error_pop_up(code):
    print("DELETE PRESSED")
    msg = QMessageBox()
    msg.setStyleSheet(open("stylesheet.qss", "r").read())

    if code == 1:
        msg.setText("Stock doesn't exist")
    elif code == 2:
        msg.setText("You must enter an amount")
    elif code == 3:
        msg.setText("You must enter a stock")
    elif code == 4:
        msg.setText("Value cannot be less than 0")

    msg.setWindowTitle("Error")
    msg.setObjectName("background")
    msg.exec_()
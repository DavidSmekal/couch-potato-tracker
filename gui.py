import sys
import sqlite3
import math
from PyQt5.QtWidgets import QWidget, QDialog, QComboBox, QPushButton, QLabel, QLineEdit, QTableWidgetItem, QCompleter
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot

import database
import helperMethods
import errorPopup
import plotCanvas


class MainPage(QWidget):

    def __init__(self):
        super().__init__()
       # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(300, 200, 1250, 750)
        self.setObjectName("background")

        # loads up the stylesheet
        self.setStyleSheet(open("stylesheet.qss", "r").read())

        self.initUI()

    @pyqtSlot()
    def initUI(self):
        # retrieves how much money is in the user's portfolio
        money_in_portfolio = database.current_money_function()
        # if user has nothing in their portfolio, the database returns a NoneType value, so we need
        # to make the variable a 0.
        if money_in_portfolio is None:
            money_in_portfolio = 0

        # this is to add a stock
        button1 = QPushButton("Add Stock", self)
        button1.move(1000, 560)
        button1.clicked.connect(self.add_stock_page)
        # this sets the object name so I can change the styling in the QSS
        button1.setObjectName("button1")

        # this is a to edit a stock
        button2 = QPushButton("Edit Stocks", self)
        button2.move(1100, 560)
        button2.clicked.connect(self.edit_stock)

        # this is the line to enter how much money you want to add
        self.enterMoney = QLineEdit(self)
        self.enterMoney.move(100, 560)
        self.enterMoney.resize(180, 30)

        # this button will add the money from the previous line
        button2 = QPushButton("Add money", self)
        button2.move(310, 560)
        button2.clicked.connect(self.add_money)

        # this is the label for stock ticker
        self.moneyLine = QLabel(self)
        self.moneyLine.move(100, 500)
        self.moneyLine.setText("Enter amount to rebalance: ")

        # this is the label for how much money you have
        self.moneyLine = QLabel(self)
        self.moneyLine.move(100, 40)
        self.moneyLine.resize(400, 35)
        self.moneyLine.setText("Total cost of portfolio: %.2f" % (money_in_portfolio,))

        # this is the label for how much money you have PLUS money you want to add
        # when the user opens up the program, the default will be with no money added
        # and that's why I repeated this as the same as above
        self.moneyLine2 = QLabel(self)
        self.moneyLine2.move(100, 80)
        self.moneyLine2.resize(400, 35)
        self.moneyLine2.setText("Total cost of portfolio (after rebalance): %.2f" % (0,))

        # this block of code creates a table
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 100, 1100, 300))

        self.tableWidget.move(80, 130)
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setObjectName("tableWidget")

        # creating all the labels for horizontal headers
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Stock"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Desired %"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Current Shares"))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Share Price"))
        self.tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem("Share Total"))
        self.tableWidget.setHorizontalHeaderItem(5, QTableWidgetItem("Portfolio Percentage"))
        self.tableWidget.setHorizontalHeaderItem(6, QTableWidgetItem("Variation"))
        self.tableWidget.setHorizontalHeaderItem(7, QTableWidgetItem("Price Round Down"))
        self.tableWidget.setHorizontalHeaderItem(8, QTableWidgetItem("Cost To Purchase"))

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(8, QtWidgets.QHeaderView.Stretch)

        self.load_data_from_database(0)

        self.show_graph()
        self.show()

    # this function creates the pie chart graph
    def show_graph(self):

        # show the graph on the GUI

        m = plotCanvas.PlotCanvas(self, width=3, height=3)
        m.move(500, 440)

    # this function populates the table from values from the database
    @pyqtSlot()
    def load_data_from_database(self, money):
        database.update_values(money)
        conn = sqlite3.connect('database.db')
        query = "SELECT * FROM usersStock"
        result = conn.execute(query)
        self.tableWidget.setRowCount(0)

        for row, row_data in enumerate(result):
            self.tableWidget.insertRow(row)
            for column, data in enumerate(row_data):
                if data is None:
                    data = 0
                if column == 1 or column == 5 or column == 6:
                    self.tableWidget.setItem(row, column,
                                             QtWidgets.QTableWidgetItem(helperMethods.decimal_to_percentage(data)))
                    # changes the background color of 'variation'
                    if column == 6:
                        self.tableWidget.item(row, column).setBackground(helperMethods.decide_variation_color(data))
                        # if the background is colored, change the text color to black
                        # to see the number easier
                        if not 0.98 <= data <= 1.02:
                            self.tableWidget.item(row, column).setForeground(QtGui.QColor(0, 0, 0))
                elif column == 4 or column == 8:
                    self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(helperMethods.int_to_currency(math.ceil(data))))
                elif column == 3 or column == 7:
                    self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(helperMethods.int_to_currency(data)))
                else:
                    self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(data)))
        conn.close()

    # this opens up a dialog and user enters a value
    # this will store the value into the database
    @pyqtSlot()
    def add_stock_page(self):

        # opens the actual dialog
        self.addStockDialog = QDialog()
        self.addStockDialog.setStyleSheet(open("stylesheet.qss", "r").read())
        self.addStockDialog.setObjectName("background")
        self.addStockDialog.setGeometry(700, 400, 420, 300)
        self.addStockDialog.setWindowTitle("Dialog")

        # this is the line to enter your stock
        self.stock = QLineEdit(self.addStockDialog)
        self.stock.move(230, 20)
        self.stock.resize(180, 30)

        # Stock autocompletion. List retrieved from http://investexcel.net/.
        # The List is scraped from Yahoo, which works with my JSON requests from Yahoo
        # List has been updated on September 2017
        # Tickers used: Stock, ETF, and Index
        # reads the file and stores the values in an array
        file = open("stock_list.txt", "r")
        lines = file.read().split('\n')
        self.completer = QCompleter(lines)
        # connecting the completer with the enter stock line
        self.stock.setCompleter(self.completer)
        self.completer.setCaseSensitivity(0)

        # this is the second line to enter how much stock you have
        self.stockAmount = QLineEdit(self.addStockDialog)
        self.stockAmount.move(230, 70)
        self.stockAmount.resize(180, 30)

        # this is the label for stock ticker
        self.line1 = QLabel(self.addStockDialog)
        self.line1.move(10, 20)
        self.line1.setText("Enter stock ticker: ")

        # this is the label for stock amount
        self.line1 = QLabel(self.addStockDialog)
        self.line1.move(10, 70)
        self.line1.setText("Enter amount of stock: ")

        # this is the label for desired % of stock
        self.line1 = QLabel(self.addStockDialog)
        self.line1.move(10, 120)
        self.line1.setText("Enter desired % of stock: ")

        # this is the box to pick your desired percentage
        self.comboBox = QComboBox(self.addStockDialog)
        self.comboBox.move(230, 120)
        self.comboBox.resize(180, 30)
        self.comboBox.addItems(["5%", "10%", "15%", "20%", "25%", "30%", "35%", "40%",
                                "45%", "50%", "55%", "60%", "65%", "70%", "75%", "80%",
                                "85%", "90%", "95%", "100%"])

        # this is the button
        b1 = QPushButton("Add Stock", self.addStockDialog)
        b1.move(300, 180)
        b1.setObjectName("random")

        # the button will connect to clickedButton function
        b1.clicked.connect(self.clicked_add)
        self.addStockDialog.exec_()

    @pyqtSlot()
    def clicked_add(self):
        # if value is empty, ignore the whole function and return 0
        if not self.stockAmount.text():
            errorPopup.show_error_pop_up(2)
            return 0
        if not self.stock.text():
            errorPopup.show_error_pop_up(3)
            return 0

        # these 2 values grab what is in the text boxes
        stock_value = self.stock.text()
        stock_amount_value = self.stockAmount.text()
        stock_desired_value = self.comboBox.currentText()

        # shows an error if user enters a value less than 0
        if int(stock_amount_value) <= -1:
            errorPopup.show_error_pop_up(4)
            return 0

        # 5% and 100% don't work, so I have to do these manually
        if stock_desired_value == "5%":
            stock_desired_value = .05
        elif stock_desired_value == "100%":
            stock_desired_value = 1.0
        else:
            # need to convert stockDesiredValue from 5% to .5 int
            stock_desired_value = "." + stock_desired_value[:-1]

        # inserts the text into the database
        database.insert_into_database(stock_value, float(stock_desired_value), stock_amount_value)
        print(stock_value)
        print(stock_amount_value)
        print(float(stock_desired_value))

        # this will clear the text when the user presses okay
        self.stock.setText("")
        self.stockAmount.setText("")
        self.load_data_from_database(0)

        # updating total value
        self.update_money_values()

    # this function adds the total money the user has with
    # the amount of money they want to add
    # I will also have to refresh the whole database after doing this
    @pyqtSlot()
    def add_money(self):
        # if value is empty, ignore the whole function and return 0
        if not self.enterMoney.text():
            errorPopup.show_error_pop_up(2)
            return 0
        money = float(self.enterMoney.text())
        # if the money entered is 0, we need to clear the text back to 0.
        if money == 0:
            self.moneyLine2.setText("Total cost of portfolio (after rebalance): %.2f" % (0,))
        else:
            temp_money = money + database.current_money_function()
            self.moneyLine2.setText("Total cost of portfolio (after rebalance): %.2f" % (temp_money,))
        # we will need to send the money value to the database to get the calculations.
        # database.addingMoneyTotal(money)
        # to reload the database
     #   database.update_values(money)
        # need to refresh the database now
        self.load_data_from_database(money)

        return money

    @pyqtSlot()
    def edit_stock(self):

        # opens the actual dialog
        self.editStockDialog = QDialog()
        self.editStockDialog.setStyleSheet(open("stylesheet.qss", "r").read())
        self.editStockDialog.setObjectName("background")
        self.editStockDialog.setGeometry(700, 400, 420, 300)
        self.editStockDialog.setWindowTitle("Edit Stock")

        # this is the label to show stock to edit
        self.line1 = QLabel(self.editStockDialog)
        self.line1.move(10, 20)
        self.line1.setText("Select stock to edit: ")

        # this box will have the stocks that you own.
        # I will query the database to retrieve the stocks you own
        self.comboBox2 = QComboBox(self.editStockDialog)
        self.comboBox2.move(230, 20)
        self.comboBox2.resize(180, 30)
        conn = sqlite3.connect('database.db')
        query = "SELECT stockTicker FROM usersStock;"
        result = conn.execute(query)
        new_result = result.fetchall()
        for i in new_result:
            print(i[0])
            self.comboBox2.addItem(i[0])

        # this is the second line to enter how much stock you have
        self.stockAmount2 = QLineEdit(self.editStockDialog)
        self.stockAmount2.resize(180, 30)
        self.stockAmount2.move(230, 70)

        # this is the label for stock amount
        self.line2 = QLabel(self.editStockDialog)
        self.line2.move(10, 70)
        self.line2.setText("Enter amount of stock: ")

        # this is the label for desired % of stock
        self.line2 = QLabel(self.editStockDialog)
        self.line2.move(10, 120)
        self.line2.setText("Enter desired % of stock: ")

        # this is the box to pick your desired percentage
        self.comboBox3 = QComboBox(self.editStockDialog)
        self.comboBox3.move(230, 120)
        self.comboBox3.resize(180, 30)
        self.comboBox3.addItems(["5%", "10%", "15%", "20%", "25%", "30%", "35%", "40%",
                                 "45%", "50%", "55%", "60%", "65%", "70%", "75%", "80%",
                                 "85%", "90%", "95%", "100%"])

        # this is the button
        b1 = QPushButton("Confirm", self.editStockDialog)
        b1.move(300, 180)
        # the button will connect to clickedButton function
        b1.clicked.connect(self.clicked_edit)

        # this is the delete button
        b2 = QPushButton("Delete", self.editStockDialog)
        b2.move(190, 180)
        # this button will connect to delete stock function
        b2.clicked.connect(self.delete_stock)

        # comboBox.currentIndexChanged()

        self.editStockDialog.exec_()

    @pyqtSlot()
    def clicked_edit(self):
        # these 2 values grab what is in the text boxes
        stock_value = self.comboBox2.currentText()
        stock_amount_value = self.stockAmount2.text()
        stock_desired_value = self.comboBox3.currentText()

        if not stock_amount_value:
            errorPopup.show_error_pop_up(2)
            return 0

        # shows an error if user enters a value less than 0
        if int(stock_amount_value) <= -1:
            errorPopup.show_error_pop_up(4)
            return 0

        # 5% and 100% don't work, so I have to do these manually
        if stock_desired_value == "5%":
            stock_desired_value = .05
        elif stock_desired_value == "100%":
            stock_desired_value = 1.0
        else:
            # need to convert stock_desired_value from 5% to .5 int
            stock_desired_value = "." + stock_desired_value[:-1]

        # inserts the text into the database
        database.update_desired_value(stock_value, float(stock_desired_value), stock_amount_value)

        # this will clear the text when the user presses edit
        self.stockAmount2.setText("")

    #    database.update_values(0)
        self.load_data_from_database(0)
        self.update_money_values()

    @pyqtSlot()
    def delete_stock(self):
        stock_value = self.comboBox2.currentText()
        database.delete_stock(stock_value)
        self.load_data_from_database(0)
        self.update_money_values()

    # this function will update the total money you have (on the main screen on the top)
    @pyqtSlot()
    def update_money_values(self):
        money_in_portfolio = database.current_money_function()
        # if user has nothing in their portfolio, the database returns a NoneType value, so we need
        # to make the variable a 0.
        if money_in_portfolio is None:
            money_in_portfolio = 0
        self.moneyLine.setText("Total money you have: %.2f" % (money_in_portfolio,))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainPage()
    exit = app.exec_()
    print("Application closed, and 'money' is set to 0")
    sys.exit(exit)

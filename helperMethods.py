from PyQt5 import QtGui
import math

# decides the color of the table cell depending on the
# % of variation
def decide_variation_color(data):
    # red
    if not (0.9 <= data <= 1.1):
        return QtGui.QColor(255, 0, 0)
    # orange
    elif not (0.95 <= data <= 1.05):
        return QtGui.QColor(255, 128, 0)
    # yellow
    elif not (0.98 <= data <= 1.02):
        return QtGui.QColor(255, 255, 0)
    # gray
    else:
        return QtGui.QColor(58, 62, 70)


# this method will take in a decimal and return a string in percentage form
def decimal_to_percentage(decimal):
    decimal = math.ceil(decimal * 100)
    new_string = str(decimal) + "%"
    return new_string

# this method converts a number to a $$$ number.
# Method will add a comma, and a "$" sign in front of the new number
def int_to_currency(amount):
    if amount >= 0:
        return '${:,.2f}'.format(amount)
    else:
        # if the number is negative:
        return '-${:,.2f}'.format(-amount)

from PyQt5 import QtGui

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



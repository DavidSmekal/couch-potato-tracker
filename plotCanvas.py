import sqlite3

from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# this class creates the pie chart
# for this graph to update, user MUST reload the entire program
class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=3, height=3, dpi=110):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        # SQL statement to retrieve all the labels from database
        conn = sqlite3.connect('database.db')
        query = "SELECT stockTicker, currentPercentage FROM usersStock;"
        result = conn.execute(query)
        stock_results = result.fetchall()

        # creating empty arrays to store info from the database
        labels = []
        explode = []
        sizes = []

        for label, percent in stock_results:
            # adding labels to an array
            labels.append(label)
            # for each label, explode needs to be set at 0.05
            explode.append(0.05)
            # each label will also have a size.
            sizes.append(percent)

        self.axes.pie(sizes, labels=labels, autopct='%1.1f%%', explode=explode, pctdistance=10, labeldistance=.5)

        self.axes.set_aspect('1')

        self.axes = fig.set_facecolor('#2B2C31')

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

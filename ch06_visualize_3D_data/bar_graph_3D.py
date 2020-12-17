"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Import necessary modules
import sys, csv
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtDataVisualization import (Q3DBars, QBarDataItem, QBar3DSeries, 
    QValue3DAxis, Q3DCamera)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class SimpleBarGraph(QWidget):

    def __init__(self):
        super().__init__() 
        self.initializeUI() 

    def initializeUI(self):
        """Initialize the window and display its contents."""
        self.setMinimumSize(800, 700)
        self.setWindowTitle('Ex 6.1 - 3D Bar Graph')

        self.setupGraph()
        self.show()

    def setupGraph(self):
        """Load data and set up the window for the bar graph."""
        header_label = QLabel("Average Monthly Temperatures in Reykjavík, Iceland 1990-2000 (˚C)")
        header_label.setAlignment(Qt.AlignCenter)

        # Load the data about average temperatures in Reykjavík from the CSV file
        temperature_data = self.loadCSVFile()
        # Select 11 sample years: 1990-2000. Don't select the first and last columns 
        rows, columns = temperature_data.shape
        years = temperature_data[rows - 11:rows, 1]
        monthly_temps = temperature_data[rows - 11:rows, 2:columns - 1].astype(float)

        bar_graph = Q3DBars() # Create instance for bar graph
        bar_graph.scene().activeCamera().setCameraPreset(Q3DCamera.CameraPresetFront)

        # Create a list of QBarDataItem objects
        data_items = []
        for row in monthly_temps:
            data_items.append([QBarDataItem(value) for value in row])

        months = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"]

        # Create instance of QBar3DSeries, change the base color and color of 
        # selected items, and add data and labels to the series
        series = QBar3DSeries()
        series.setBaseColor(QColor("#17A4D9"))
        series.setSingleHighlightColor(QColor("#F8A307"))
        series.dataProxy().addRows(data_items)
        series.dataProxy().setRowLabels(years) # rowLabel
        series.dataProxy().setColumnLabels(months) # colLabel
        
        # Create the valueLabel. Use QValue3dAxis so we can format the axis's label
        temperature_axis = QValue3DAxis()
        temperature_axis.setRange(-10, 20)
        temperature_axis.setLabelFormat(u"%.1f \N{degree sign}C")
        bar_graph.setValueAxis(temperature_axis)

        # When items in the graph are selected, a label appears overhead with information 
        # about that item. Set the format of information in the label
        series.setItemLabelFormat("Reykjavík - @colLabel @rowLabel: @valueLabel")

        bar_graph.addSeries(series)# Add the series to the bar graph

        # 3D graph classes inherit QWindow, so we must use createWindowContainer() to 
        # create a holder for the 3D graph in our window since they can't be used
        # as a normal widget
        container = self.createWindowContainer(bar_graph)
        v_box = QVBoxLayout()
        v_box.addWidget(header_label)
        v_box.addWidget(container, 1)
        self.setLayout(v_box)

    def loadCSVFile(self):
        """Load the data from a CSV-formatted file using csv and numpy."""
        file_name = "files/Reykjavik_temp.csv"

        with open(file_name, "r") as csv_f:
            reader = csv.reader(csv_f)
            header_labels = next(reader)
            data = np.array(list(reader))
        return data

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleBarGraph()
    sys.exit(app.exec_())
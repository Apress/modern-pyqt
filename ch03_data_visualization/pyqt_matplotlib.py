"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Import necessary modules
import sys, csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout

import numpy as np
import matplotlib
matplotlib.use('Qt5Agg') # Configure the backend to use Qt5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
 
class CreateCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, nrow=1, ncol=1):
        # Create Matplotlib Figure object
        figure = Figure(figsize=(6, 5), dpi=100)
        # Reserve width and height space for subplots
        figure.subplots_adjust(wspace= 0.3, hspace=0.4)
        # Create the axes and set the number of rows/columns for the subplot(s)
        self.axes = figure.subplots(nrow, ncol)
        super(CreateCanvas, self).__init__(figure)

class DisplayGraph(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Initialize the window and display its contents."""
        self.setMinimumSize(1000, 800)
        self.setWindowTitle("3.2 - PyQt5 + Matplotlib")

        self.setupChart()
        self.show()

    def setupChart(self):
        """Set up the GUI's window and widgets that are embedded with Matplotlib figures."""
        # Load the iris dataset from the CSV file
        iris_data = self.loadCSVFile()

        # Create the different feature variables for each of the columns in the iris dataset
        sepal_length, sepal_width = iris_data[:, 0].astype(float), iris_data[:, 1].astype(float)
        petal_length, petal_width = iris_data[:, 2].astype(float), iris_data[:, 3].astype(float)
        labels = iris_data[:, 4].astype(str)
        
        # Convert target labels to encoded labels that will be used for color coding the 
        # points in the scatter plots
        encoded_labels = []

        for label in labels:
            if label == "Setosa":
                encoded_labels.append(0)
            elif label == "Versicolor":
                encoded_labels.append(1)
            elif label == "Virginica":
                encoded_labels.append(2)

        # Create a canvas object for the scatter plot that visualizes the relationship 
        # between sepal_length and sepal_width
        scatter_canvas = CreateCanvas(self)
        scatter_canvas.axes.set_title('Sepal Length vs. Sepal Width', fontsize=16)
        scatter_canvas.axes.scatter(sepal_length, sepal_width, s=100 * petal_width,
            c=encoded_labels, cmap='viridis', alpha=0.4)
        scatter_canvas.axes.set_xlabel("Sepal length (cm)", fontsize=12)
        scatter_canvas.axes.set_ylabel("Sepal width (cm)", fontsize=12)
        self.addToolBar(NavigationToolbar2QT(scatter_canvas, self))

        # Regression line for petal length vs. petal width
        reg_line = np.polyfit(petal_length, petal_width, 1)
        poly_reg_line = np.poly1d(reg_line)

        # Create a canvas object for the scatter plot and histogram that visualize the 
        # relationship between petal_length and petal_width
        mixed_canvas = CreateCanvas(self, nrow=2, ncol=1)
        mixed_canvas.axes[0].scatter(petal_length, petal_width, alpha=0.5, 
            c=encoded_labels, cmap='viridis')
        mixed_canvas.axes[0].set_title("Regression Analysis for Iris Petals", fontsize=14)
        mixed_canvas.axes[0].plot(petal_length, poly_reg_line(petal_length), c='black')
        mixed_canvas.axes[0].set_xlabel("Petal length (cm)", fontsize=12)
        mixed_canvas.axes[0].set_ylabel("Petal width (cm)", fontsize=12)
        mixed_canvas.axes[0].grid(True)

        # Create histogram for petal length
        mixed_canvas.axes[1].hist(petal_length[:50], bins=15, color='purple', alpha=0.6, label="Setosa")
        mixed_canvas.axes[1].hist(petal_length[51:100], bins=15, color='lightgreen', alpha=0.6, label="Versicolor")
        mixed_canvas.axes[1].hist(petal_length[101:149], bins=15, color='yellow', alpha=0.6, label="Virginica")    

        mixed_canvas.axes[1].set_title("Histogram for Iris Petals", fontsize=14,)
        mixed_canvas.axes[1].set_xlabel("Petal length (cm)", fontsize=12)
        mixed_canvas.axes[1].set_ylabel("Petal width (cm)", fontsize=12)
        mixed_canvas.axes[1].legend()
        self.addToolBar(NavigationToolbar2QT(mixed_canvas, self))

        charts_h_box = QHBoxLayout()
        charts_h_box.addWidget(scatter_canvas)
        charts_h_box.addWidget(mixed_canvas)

        main_v_box = QVBoxLayout()
        main_v_box.addLayout(charts_h_box)

        container = QWidget()
        container.setLayout(main_v_box)
        self.setCentralWidget(container)

    def loadCSVFile(self):
        """Load the iris dataset and store the data in a numpy array."""
        file_name = "files/iris.csv"

        with open(file_name, "r") as csv_f:
            reader = csv.reader(csv_f)
            header_labels = next(reader)
            data = np.array(list(reader))
        return data

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DisplayGraph()
    sys.exit(app.exec_())
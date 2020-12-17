"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Import necessary modules
import sys, csv
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QScatterSeries, QLineSeries
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

def linearRegression(x_values, y_values):
    """Find the regression line that fits best to the data.
    Calculate the values for m, the slope of a line, and b, the 
    y-intercept in the equation Y = a + bX."""
    # Calculate the avarage values for x and y
    mean_x, mean_y = np.mean(x_values), np.mean(y_values)

    # Calculate the covariance and variance for the slope coefficient; 
    # covariance_xy describes the linear relationship of the variables 
    # as they change; variance_x calculates how far observed x_values 
    # differs from the mean_x
    covariance_xy = np.sum((x_values - mean_x) * (y_values - mean_y))
    variance_x = np.sum((x_values - mean_x) ** 2)

    # Calculate the slope, m, and the y-intercept, b
    b_slope = covariance_xy / variance_x
    a_intercept = mean_y - b_slope * mean_x

    return (a_intercept, b_slope)

class DisplayGraph(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Initialize the window and display its contents."""
        self.setMinimumSize(700, 500)
        self.setWindowTitle("Ex 3.2 - Combining Charts")

        self.row_count = 0

        self.setupChart()
        self.show()

    def setupChart(self):
        """Set up the GUI's series and chart."""
        # Collect x and y data values from the CSV file
        x_values, y_values = self.loadCSVFile()

        # Get the largest x and y values; Used for setting the chart's axes 
        x_max, y_max = max(x_values), max(y_values)
        
        # Create numpy arrays from the x and y values 
        x_values = np.array(x_values)
        y_values = np.array(y_values)

        # Calculate the regression line 
        coefficients = linearRegression(x_values, y_values)

        # Create chart object
        chart = QChart()
        chart.setTitle("Auto Insurance for Geographical Zones in Sweden")
        chart.legend().hide()
        
        # Create scatter series and add points to the series
        scatter_series = QScatterSeries()
        scatter_series.setName("DataPoints")
        scatter_series.setMarkerSize(9.0)
        scatter_series.hovered.connect(self.displayPointInfo)

        for value in range(0, self.row_count - 1):
            scatter_series.append(x_values[value], y_values[value])
            scatter_series.setBorderColor(QColor('#000000'))

        # Create line series and add points to the series
        line_series = QLineSeries()
        line_series.setName("RegressionLine")

        # Calculate the regression line
        for x in x_values:
            y_pred = coefficients[0] + coefficients[1] * x
            line_series.append(x, y_pred)

        # Add both series to the chart and create x and y axes
        chart.addSeries(scatter_series)
        chart.addSeries(line_series)
        chart.createDefaultAxes()

        axis_x = chart.axes(Qt.Horizontal)
        axis_x[0].setTitleText("Number of Claims")
        axis_x[0].setRange(0, x_max)
        axis_x[0].setLabelFormat("%i")

        axis_y = chart.axes(Qt.Vertical)
        axis_y[0].setTitleText("Total Payment in Swedish Kronor (in thousands)")
        axis_y[0].setRange(0, y_max + 20)

        # Create QChartView object for displaying the chart 
        chart_view = QChartView(chart)

        v_box = QVBoxLayout()
        v_box.addWidget(chart_view)
        self.setLayout(v_box)

    def displayPointInfo(self, point):
        """Demonstration that series can be interacted with."""
        print("(X: {}, Y: {})".format(point.x(), point.y()))

    def loadCSVFile(self):
        """Load data from CSV file for the scatter chart. 
        Select and store x and y values into Python list objects.
        Return the x_values and y_values lists."""
        x_values, y_values = [], []
        file_name = "files/auto_insurance_sweden.csv"
 
        with open(file_name, "r") as csv_f:
            reader = csv.reader(csv_f) 
            for row in reader:
                x = float(row[0])
                x_values.append(x)
                y = float(row[1]) 
                y_values.append(y)  

            # Count the number of rows in the CSV file. Reset the 
            # reader's current position back to the top of the file
            csv_f.seek(0)
            self.row_count = len(list(reader))
        return x_values, y_values

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DisplayGraph()
    sys.exit(app.exec_())
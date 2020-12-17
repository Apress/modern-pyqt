"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Import necessary modules
import sys, csv, random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
    QComboBox, QCheckBox, QFormLayout, QDockWidget, QTableView, QHeaderView, QGraphicsView)
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QStandardItemModel, QStandardItem

class ChartView(QChartView):
    
    def __init__(self, chart):
        super().__init__(chart)
        self.chart = chart   

        # Starting position for mouse press event
        self.start_pos = None 

    def wheelEvent(self, event):
        """Reimplement the scroll wheel on the mouse for zooming in and out on the chart."""
        zoom_factor = 1.0 # Simple way to control the total amount zoomed in or out
        scale_factor = 1.10 # How much to scale into or out of the chart

        if event.angleDelta().y() >= 120 and zoom_factor < 3.0:
            zoom_factor *= 1.25
            self.chart.zoom(scale_factor)
        elif event.angleDelta().y() <= -120 and zoom_factor > 0.5:
            zoom_factor *= 0.8
            self.chart.zoom(1 / scale_factor)
            
    def mousePressEvent(self, event):
        """If the mouse button is pressed, change the mouse cursor and 
        get the coordinates of the click."""
        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.start_pos = event.pos()

    def mouseMoveEvent(self, event):
        """Reimplement the mouseMoveEvent so that the user can scroll the chart area."""
        if (event.buttons() == Qt.LeftButton):
            delta = self.start_pos - event.pos()
            self.chart.scroll(delta.x(), -delta.y())
            self.start_pos = event.pos()

    def mouseReleaseEvent(self, event):
        self.setDragMode(QGraphicsView.NoDrag) # Don't display mouse cursor

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Initialize the window and display its contents."""
        self.setMinimumSize(1200, 600)
        self.setWindowTitle("3.1 - Data Visualization GUI")

        self.setupChart()
        self.setupToolsDockWidget()
        self.setupMenu()
        self.show()

    def setupChart(self):
        """Set up the GUI's graph series type, chart instance, chart axes, 
        and chart view widget."""
        random.seed(50) # Create seed for random numbers

        # Create the model instance and set the headers
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        self.model.setHorizontalHeaderLabels(["Year", "Social Exp. %GDP", "Country"])

        # Collect x and y data values and labels from the CSV file
        xy_data_and_labels = self.loadCSVFile()

        # Create the individual lists for x, y and labels values
        x_values, y_values, labels = [], [], []
        # Append items to the corresponding lists
        for item in range(len(xy_data_and_labels)):
            x_values.append(xy_data_and_labels[item][0])
            y_values.append(xy_data_and_labels[item][1])
            labels.append(xy_data_and_labels[item][2])

        # Remove all duplicates from the labels list using list comprehension. 
        # This list will be used to create the labels in the chart's legend.
        set_of_labels = []
        [set_of_labels.append(x) for x in labels if x not in set_of_labels]  
    
        # Create chart object
        self.chart = QChart()
        self.chart.setTitle("Public Social Spending as a Share of GDP, 1880 to 2016")
        self.chart.legend().hide() # Hide legend at the start

        # Specify parameters for the x and y axes
        self.axis_x = QValueAxis()
        self.axis_x.setLabelFormat("%i")
        self.axis_x.setTickCount(10)
        self.axis_x.setRange(1880, 2016)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)

        self.axis_y = QValueAxis()
        self.axis_y.setLabelFormat("%i" + "%")
        self.axis_y.setRange(0, 40)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        # Create a Python dict to associate the labels with the individual line series
        series_dict = {}

        for label in set_of_labels:
            # Create labels from data and add them to a Python dictionary
            series_label = 'series_{}'.format(label)
            series_dict[series_label] = label # Create label value for each line series

        # For each of the keys in the dict, create a line series
        for keys in series_dict.keys():
            # Use get() to access the corresponding value for a key
            label = series_dict.get(keys)

            # Create line series instance and set its name and color values
            line_series = QLineSeries()
            line_series.setName(label)
            line_series.setColor(QColor(random.randint(10, 254), random.randint(10, 254), random.randint(10, 254)))

            # Append x and y coordinates to the series
            for value in range(len(xy_data_and_labels)):
                if line_series.name() == xy_data_and_labels[value][2]:
                    line_series.append(x_values[value], y_values[value])

                    # Create and add items to the model (for displaying the table)
                    items = [QStandardItem(str(item)) for item in xy_data_and_labels[value]]
                    color = line_series.pen().color()
                    for item in items:
                        item.setBackground(color)
                    self.model.insertRow(value, items)

            self.chart.addSeries(line_series)
            line_series.attachAxis(self.axis_x)
            line_series.attachAxis(self.axis_y)   

        # Create QChartView object for displaying the chart 
        self.chart_view = ChartView(self.chart)
        self.setCentralWidget(self.chart_view)

    def setupMenu(self):
        """Create a simple menu to manage the dock widget."""
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        # Create view menu and add actions
        view_menu = menu_bar.addMenu('View')
        view_menu.addAction(self.toggle_dock_tools_act)

    def setupToolsDockWidget(self):
        """Set up the dock widget that displays different tools and themes for 
        interacting with the chart. Also displays the data values in a table view object."""
        tools_dock = QDockWidget()
        tools_dock.setWindowTitle("Tools")
        tools_dock.setMinimumWidth(400)
        tools_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        # Create widgets for dock widget area
        themes_cb = QComboBox()
        themes_cb.addItems(["Light", "Cerulean Blue", "Dark", "Sand Brown", 
            "NCS Blue", "High Contrast", "Icy Blue", "Qt"])
        themes_cb.currentTextChanged.connect(self.changeChartTheme)

        self.animations_cb = QComboBox()
        self.animations_cb.addItem("No Animation", QChart.NoAnimation)
        self.animations_cb.addItem("Grid Animation", QChart.GridAxisAnimations)
        self.animations_cb.addItem("Series Animation", QChart.SeriesAnimations)
        self.animations_cb.addItem("All Animations", QChart.AllAnimations)
        self.animations_cb.currentIndexChanged.connect(self.changeAnimations)

        self.legend_cb = QComboBox()
        self.legend_cb.addItem("No Legend")
        self.legend_cb.addItem("Align Left", Qt.AlignLeft)
        self.legend_cb.addItem("Align Top", Qt.AlignTop)
        self.legend_cb.addItem("Align Right", Qt.AlignRight)
        self.legend_cb.addItem("Align Bottom", Qt.AlignBottom)
        self.legend_cb.currentTextChanged.connect(self.changeLegend)

        self.antialiasing_check_box = QCheckBox()
        self.antialiasing_check_box.toggled.connect(self.toggleAntialiasing)

        reset_button = QPushButton("Reset Chart Axes")
        reset_button.clicked.connect(self.resetChartZoom)

        # Create table view and set its model
        data_table_view = QTableView()
        data_table_view.setModel(self.model)
        data_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        data_table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)   

        dock_form = QFormLayout()
        dock_form.setAlignment(Qt.AlignTop)
        dock_form.addRow("Themes:", themes_cb)
        dock_form.addRow("Animations:", self.animations_cb)
        dock_form.addRow("Legend:", self.legend_cb)
        dock_form.addRow("Anti-Aliasing", self.antialiasing_check_box)
        dock_form.addRow(reset_button)
        dock_form.addRow(data_table_view)

        # Create QWidget object to act as a container for dock widgets
        tools_container = QWidget()
        tools_container.setLayout(dock_form)
        tools_dock.setWidget(tools_container)

        self.addDockWidget(Qt.LeftDockWidgetArea, tools_dock)
        # Handles the visibility of the dock widget
        self.toggle_dock_tools_act = tools_dock.toggleViewAction()

    def changeChartTheme(self, text):
        """Slot for changing the theme of the chart."""
        themes_dict = {"Light": 0, "Cerulean Blue": 1, "Dark": 2, "Sand Brown": 3, 
            "NCS Blue": 4, "High Contrast": 5, "Icy Blue": 6, "Qt": 7}
        theme = themes_dict.get(text)
        if theme == 0:
            self.setupChart()
        else:
            self.chart.setTheme(theme)
        
    def changeAnimations(self):
        """Slot for changing the animation style of the chart."""        
        animation = QChart.AnimationOptions(
            self.animations_cb.itemData(self.animations_cb.currentIndex()))
        self.chart.setAnimationOptions(animation)

    def changeLegend(self, text):
        """Slot for turning off the legend, or changing its location."""
        alignment = self.legend_cb.itemData(self.legend_cb.currentIndex())

        if text == "No Legend":
            self.chart.legend().hide()
        else:
            self.chart.legend().setAlignment(Qt.Alignment(alignment))
            self.chart.legend().show()

    def toggleAntialiasing(self, state):
        """If self.antialiasing_check_box.isChecked() is True, turn on antialiasing."""
        if state:
            self.chart_view.setRenderHint(QPainter.Antialiasing, on=True)
        else:
            self.chart_view.setRenderHint(QPainter.Antialiasing, on=False)

    def resetChartZoom(self):
        """Reset the chart and the axes."""
        self.chart.zoomReset()
        self.axis_x.setRange(1880, 2016)
        self.axis_y.setRange(0, 40)
            
    def loadCSVFile(self):
        """Load data from CSV file for the chart. 
        Select and store x and y values and labels into Python list objects.
        Return the xy_data_and_labels list."""
        file_name = "files/social_spending_simplified.csv"

        with open(file_name, "r") as csv_f:
            reader = csv.reader(csv_f)
            header_labels = next(reader)

            row_values = [] # Store current row values
            xy_data_and_labels = [] # Store all values

            for i, row in enumerate(reader):
                x = int(row[2])  
                y = float(row[3])   
                label = row[0]

                row_values.append(x)
                row_values.append(y)  
                row_values.append(label)

                # Add row_values to xy_data_and_labels, then reset row_values
                xy_data_and_labels.append(row_values)
                row_values = []

        return xy_data_and_labels

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
# README

Information related to installing various packages for *"Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"*

**NOTE** - Code for this text has been tested on the following platforms:

* MacOS Mojave
* Windows 10
* Linux (Ubuntu) versions 18.04 and 20.04

## Prerequisites 

* Python 3
Information for downloading [Python](https://python.org/downloads/) can be found on their website.

* All chapters in the text require the latest version of PyQt5, version 5.15.
More information about [PyQt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/) can be found on the Riverbank Computing Limited website.

Code throughout this book is installed using the the Python Package Installer, [pip](https://pip.pypa.io/en/stable/), and was tested on Ubuntu, but should also work for other Linux distributions, as well. 

To install PyQt5 using pip, run:
```bash
$ pip3 install PyQt5
```

Installation on Ubuntu, can also be performed using the [APT](https://wiki.debian.org/Apt) package manager by:
```bash
$ sudo apt install python3-pyqt5
```
Different versions of Linux will require different Debian package managers. If pip is not working on your version of Linux, you will need to search online for assistance. 

## Additional Packages

A few of the chapters may require additional Python packages or PyQt5 modules. The following section goes over installing them. Additional information can also be found in each chapter of the text. 

### Chapter 3 - Data Visualization and Analysis

Installing the [PyQtChart](https://riverbankcomputing.com/software/pyqtchart) module is done by:
```bash
$ pip3 install PyQtChart
```

The [NumPy](https://numpy.org) library is also needed and can be installed by:
```bash
$ pip3 install numpy
```

Finally, [Matplotlib](https://matplotlib.org) is needed for one of the projects. The library can be installed by:
```bash
$ pip3 install matplotlib
```

### Chapter 4 - Database Handling in PyQt

PyQt5 already comes installed with the QtSql module for working with SQL databases. However, if you find that the module is missing on Ubuntu, QtSql can be installed by:
```bash
$ sudo apt install python3-pyqt5.qtsql
```

### Chapter 5 - GUIs for Computer Vision

There are a number of issues that can occur when using PyQt and the [OpenCV](https://opencv.org) library. This is because OpenCV also has Qt dependencies built into it. The best way to avoid any issues between Qt and OpenCV is to install the headless versions of OpenCV (with no GUI functionality built in). To install the basic OpenCV modules (minus GUI functionality), run:
```bash
$ pip3 install opencv-python-headless
```
To install all of the OpenCV modules (minus GUI functionality), enter:
```bash
$ pip3 install opencv-contrib-python-headless
```
For Linux users, namely Ubuntu, you can try and use the APT package manager if you are still having issues with PyQt and OpenCV working together. Run:
```bash
$ sudo apt install python3-opencv
```
Additional information about installing OpenCV for Linux distributions can be found [here](https://docs.opencv.org/master/df/d65/tutorial_table_of_content_introduction.html).


### Chapter 6 - Visualizing 3D Data

Installing the [PyQtDataVisualization](https://www.riverbankcomputing.com/software/pyqtdatavisualization/intro) module is performed by:
```bash
$ pip3 install PyQtDataVisualization
```

### Chapter 7 - Introduction to Networking with PyQt

This chapter only briefly requires the [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) package. To install, run:
```bash
$ pip3 install beautifulsoup4
```
To install on Ubuntu, you can also run:
```bash
$ sudo apt-get install python3-bs4
```

### Chapter 8 - Creating a Chatbot

To create this chapter's chatbot logic, you will need to install the [ChatterBot](https://chatterbot.readthedocs.io/en/stable/index.html) library. This is done by:
```bash
$ pip3 install chatterbot
```
The ChatterBot library has a number of dependencies. You may run into issues with a few of them. Let's first install the ChatterBot Corpus from GitHub:
```bash
$ pip3 install chatterbot-corpus
```
If you run into issues with the PyYAML package, use the following command instead to install the Corpus:
```bash
$ pip3 install chatterbot-corpus --ignore-installed
```
To install [spaCy](https://spacy.io), run:
```bash
$ pip3 install spacy
```
And finally, to download the English spaCy model, run:
```bash
$ python3 -m spacy download en
```

### Chapter 9 - Deploying PyQt Applications

For this chapter, you'll need to install [PyInstaller](http://www.pyinstaller.org). To install, run:
```bash
$ pip3 install pyinstaller
```

## Authors

* **Joshua Willman** - [redhuli.io](https://redhuli.io)
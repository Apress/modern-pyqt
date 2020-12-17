# Listing 9-1 
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"

A simple audio recorder GUI that demonstrates how to use PyQt's QtMultimedia classes.

## Prerequisites

[PyQt](https://www.riverbankcomputing.com/static/Docs/PyQt5/) 
[PyInstaller](http://www.pyinstaller.org) - For creating the .spec file

## Breakdown of the Files

* audio_recorder.py - Creates GUI. Program is to be from here. 
* AudioRecorder.spec - Specification file for building executable with PyInstaller
* AudioRecorderStyleSheet.py - The style sheet for the GUI
* resources.py - Binary file containing information about the application's resources. Created with pyrcc5 
* resources.qrc - Qt resource system file (XML syntax)

## Usage

To run the application from the command line: 

```bash
python3 audio_recorder.py
```

To create the resources.py from the resources.qrc file using pyrcc5: 

```bash
pyrcc5 resources.qrc -o resources.py
```

To create the executable file using the .spec file, first change the source path to this directory on your local system.

```bash
pyinstaller AudioRecorder.spec
```

## Authors

* **Joshua Willman** - [redhuli.io](https://redhuli.io)
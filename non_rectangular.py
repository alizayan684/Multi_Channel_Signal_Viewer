import csv
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from PySide6.QtWidgets import QPushButton, QColorDialog, QFileDialog, QComboBox
from PySide6.QtWidgets import QHBoxLayout
import pandas as pd
from pathlib import Path

def read_csv(file_name):
    """this module is used to read and prepare the  ECG signal"""
    signal = {}
    with open(f'{file_name}', 'r') as file:
        reader = csv.reader(file)
        magnitudes = list(reader)[0]
        magnitude_values = [float(magnitude) for magnitude in magnitudes]
        time = list(range(1, len(magnitude_values)+1))
        signal['time'] = time
        signal['magnitude'] = magnitude_values
    return signal
def transform_signal(signal):
    """this function is used to transform the ECG signal to polar coordinates"""
    r =  np.sqrt(np.array(signal['magnitude'])**2 + np.array(signal['time'])**2)
    theta = np.arctan(np.array(signal['magnitude'])/np.array(signal['time']))
    return r, theta
    
class PolarPlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111, projection='polar')
        super().__init__(fig)
        self.setParent(parent)

        # Initialize polar plot line
        self.line, = self.ax.plot([], [], lw=2)
        self.lines = []
        self.ax.set_ylim(0, 2)  # Set radius limits
        self.signals = {}
        self.signal_colors = {}
        self.signal = None

    def init_plot(self):
        """Initialize plot settings"""
        self.lines.clear()  # Clear old lines
        if not self.signal:
            return
        if isinstance(self.signal[0], list):  # Multiple signals
            for _ in self.signal:
                line, = self.ax.plot([], [], lw=2)
                self.lines.append(line)
        else:
            self.line, = self.ax.plot([], [], lw=2)
        return self.lines if self.lines else [self.line]


    def update_plot(self, frame):
        """Update the polar plot data for each frame"""
        if not self.signal:
            return
        # check if the signal is a list of signals or a single signal
        if isinstance(self.signal[0], list):
            for i, sig in enumerate(self.signal):
                self.lines[i].set_data(sig[0][:frame], sig[1][:frame])
            return self.lines
        else:
            self.line.set_data(self.signal[0][:frame], self.signal[1][:frame])
            return self.line,

class Window(QMainWindow):
    def __init__(self, main_window):
        super().__init__()

        self.setWindowTitle("Polar Plot in Cine Mode with PyQt6")
        self.setGeometry(100, 100, 800, 600)
        self.ylim = 1
        self.main_window = main_window
        self.setStyleSheet("QPushButton {\n"
"    background-color: #5E81AC; /* Background color on hover */\n"
"\n"
"    color: #D8DEE9; /* Light text color */\n"
"    font-size: 16px; /* Font size */\n"
"    padding: 10px 20px; /* Padding around the text */\n"
"    border: 2px solid #2E3440; /* Border color */\n"
"    border-radius: 5px; /* Rounded corners */\n"
"    font-family: \"Segoe UI\", \"Helvetica Neue\", \"Arial\", sans-serif; /* Font family */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(137, 220, 255);\n"
"	color: rgb(0, 0, 0);\n"
"    border: 2px solid #81A1C1; /* Border color on hover */\n"
"\n"
"    font-size: 16px; /* Font size */\n"
"    padding: 10px 20px; /* Padding around the text */\n"
"    border-radius: 5px; /* Rounded corners */\n"
"    font-family: "
                        "\"Segoe UI\", \"Helvetica Neue\", \"Arial\", sans-serif; /* Font family */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #3B4252; /* Background color when pressed */\n"
"    border: 2px solid #4C566A; /* Border color when pressed */\n"
"}\n")

        # Set up main widget
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Set up layout
        layout = QVBoxLayout(self.main_widget)

        # Create Matplotlib canvas
        self.canvas = PolarPlotCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.canvas)
        hlayout = QHBoxLayout()
        layout.addLayout(hlayout)

        # add a button to change the color of the signal
        self.colorButton = QPushButton("Color", self)
        self.colorButton.clicked.connect(self.change_color)
        hlayout.addWidget(self.colorButton)
        # add a button to browse the file
        self.browseButton = QPushButton("Browse", self)
        self.browseButton.clicked.connect(self.browse_file)
        hlayout.addWidget(self.browseButton)
        # add a button to start the animation
        self.startButton = QPushButton("Start", self)
        self.startButton.clicked.connect(self.start_animation)
        hlayout.addWidget(self.startButton)
        # add a button to stop the animation
        self.stopButton = QPushButton("Stop", self)
        self.stopButton.clicked.connect(self.stop_animation)
        hlayout.addWidget(self.stopButton)
        # add a button to zoom in the plot
        self.zoomInButton = QPushButton("Zoom In", self)
        self.zoomInButton.clicked.connect(self.zoom_in)
        hlayout.addWidget(self.zoomInButton)
        # add a button to zoom out the plot
        self.zoomOutButton = QPushButton("Zoom Out", self)
        self.zoomOutButton.clicked.connect(self.zoom_out)
        hlayout.addWidget(self.zoomOutButton)
        # add a button to rewind the animation
        self.rewindButton = QPushButton("Rewind", self)
        self.rewindButton.clicked.connect(self.rewind)
        hlayout.addWidget(self.rewindButton)
        # add a button to speed up the animation
        self.speedUpButton = QPushButton("Speed Up", self)
        self.speedUpButton.clicked.connect(self.speed_up)
        hlayout.addWidget(self.speedUpButton)
        # add a button to slow down the animation
        self.slowDownButton = QPushButton("Slow Down", self)
        self.slowDownButton.clicked.connect(self.slow_down)
        hlayout.addWidget(self.slowDownButton)
        # add a combo box to select the signal to change its name or color
        self.signalComboBox = QComboBox(self)
        self.signalComboBox.addItem("All Signals")

        self.signalComboBox.activated.connect(self.change_signal)

        hlayout.addWidget(self.signalComboBox)
    def run_animation(self):
        # Start animation
        self.anim = FuncAnimation(self.canvas.figure, self.canvas.update_plot, 
                                  init_func=self.canvas.init_plot, frames=200, 
                                  interval=50, blit=True)

    def change_name(self):
        pass
    
    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            signal_name = self.signalComboBox.currentText()
            if signal_name == 'All Signals':
                return
            self.canvas.signal_colors[signal_name] = color.name()
            self.canvas.line.set_color(color.name())
            self.canvas.draw()

    def browse_file(self):
        # find csv file
        file_name = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        currSignalName = Path(file_name[0]).name[0 : -4]
        self.signalComboBox.addItem(currSignalName)
        self.signalComboBox.setCurrentText(currSignalName)
        signal = read_csv(file_name[0])
        r, theta =  transform_signal(signal)
        self.canvas.signal = [r ,theta]
        self.canvas.signals[currSignalName] = [r, theta]
        self.run_animation()


    def change_signal(self):

        signal_name = self.signalComboBox.currentText()
        
        if signal_name == "All Signals":
            if self.canvas.signals:
                # Collect all signals (assumes each signal is in [r, theta] format)
                self.canvas.signal = [self.canvas.signals[sn] for sn in self.canvas.signals]
                self.canvas.init_plot()
            else:
                print("No signals available.")
                return
        else:
            if signal_name in self.canvas.signals:
                self.canvas.signal = self.canvas.signals[signal_name]
                self.canvas.init_plot()
            else:
                print(f"Signal '{signal_name}' not found.")
                return

        self.canvas.draw()

            
        
    
    def start_animation(self):
        # check if the animation is running
        if hasattr(self, 'anim') and self.anim.event_source is not None:
            self.anim.event_source.start()
            return 
    
    def stop_animation(self):
        # check if the animation is running
        if hasattr(self, 'anim') and self.anim.event_source is not None:
            self.anim.event_source.stop()
            return
    def zoom_in(self):
        self.canvas.ax.set_ylim(0, self.ylim - 0.1)
        self.ylim -= 0.1
        self.canvas.draw()
    
    def zoom_out(self):
        self.canvas.ax.set_ylim(0,  self.ylim + 0.1)
        self.ylim += 0.1
        self.canvas.draw()
    
    def rewind(self):
        # check if the animation is running
        if hasattr(self, 'anim') and self.anim.event_source is not None:
            self.anim.frame_seq = self.anim.new_frame_seq()
            return

    def speed_up(self):
        if hasattr(self, 'anim') and self.anim.event_source is not None:
           self.anim.event_source.interval /= 10
           return
    
    def slow_down(self):
        if hasattr(self, 'anim') and self.anim.event_source is not None:
           self.anim.event_source.interval *= 10
           return
    
    def closeEvent(self, event):
        # show the main window again
        self.main_window.show()
        event.accept()


import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from PyQt6.QtWidgets import QPushButton, QColorDialog, QFileDialog
from PyQt6.QtWidgets import QHBoxLayout

class PolarPlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111, projection='polar')
        super().__init__(fig)
        self.setParent(parent)

        # Initialize polar plot line
        self.line, = self.ax.plot([], [], lw=2)
        self.ax.set_ylim(0, 2)  # Set radius limits

    def init_plot(self):
        """Initialize plot settings"""
        self.line.set_data([], [])
        return self.line,

    def update_plot(self, frame):
        """Update the polar plot data for each frame"""
        theta = np.linspace(0, 2 * np.pi, 100)
        r = 1 + np.sin(2 * theta + 0.1 * frame)  # Example function
        self.line.set_data(theta, r)
        return self.line,

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Polar Plot in Cine Mode with PyQt6")
        self.setGeometry(100, 100, 800, 600)
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

        # Start animation
        self.anim = FuncAnimation(self.canvas.figure, self.canvas.update_plot, 
                                  init_func=self.canvas.init_plot, frames=200, 
                                  interval=50, blit=True)
        # add start, stop, zoom in, zoom out, rewind, speed up , slow down , change color , browse button , change signal name
        # add a button to change the signal name
        button = QPushButton("Name", self)
        button.clicked.connect(self.change_name)
        hlayout.addWidget(button)
        # add a button to change the color of the signal
        button = QPushButton("Color", self)
        button.clicked.connect(self.change_color)
        hlayout.addWidget(button)
        # add a button to browse the file
        button = QPushButton("Browse", self)
        button.clicked.connect(self.browse_file)
        hlayout.addWidget(button)
        # add a button to start the animation
        button = QPushButton("Start", self)
        button.clicked.connect(self.start_animation)
        hlayout.addWidget(button)
        # add a button to stop the animation
        button = QPushButton("Stop", self)
        button.clicked.connect(self.stop_animation)
        hlayout.addWidget(button)
        # add a button to zoom in the plot
        button = QPushButton("Zoom In", self)
        button.clicked.connect(self.zoom_in)
        hlayout.addWidget(button)
        # add a button to zoom out the plot
        button = QPushButton("Zoom Out", self)
        button.clicked.connect(self.zoom_out)
        hlayout.addWidget(button)
        # add a button to rewind the animation
        button = QPushButton("Rewind", self)
        button.clicked.connect(self.rewind)
        hlayout.addWidget(button)
        # add a button to speed up the animation
        button = QPushButton("Speed Up", self)
        button.clicked.connect(self.speed_up)
        hlayout.addWidget(button)
        # add a button to slow down the animation
        button = QPushButton("Slow Down", self)
        button.clicked.connect(self.slow_down)
        hlayout.addWidget(button)
    
    def change_name(self):
        print("Change the name of the signal")
    
    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            print(color.name())
    
    def browse_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if file:
            print(file)
    
    def start_animation(self):
        self.anim.event_source.start()
    
    def stop_animation(self):
        self.anim.event_source.stop()
    
    def zoom_in(self):
        self.canvas.ax.set_ylim(0, 1)
        self.canvas.draw()
    
    def zoom_out(self):
        self.canvas.ax.set_ylim(0, 2)
        self.canvas.draw()
    
    def rewind(self):
        self.anim.frame_seq = self.anim.new_frame_seq()

    def speed_up(self):
        self.anim.event_source.interval /= 2

    def slow_down(self):
        self.anim.event_source.interval *= 2
    


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

import sys
from PyQt6 import QtWidgets, QtCore
from test_graph_dsp_trans import Ui_MainWindow
import pyqtgraph as pg
import numpy as np
import pandas as pd

class MainWindow(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.df = None  # No data initially
        self.browsedData_y = []
        self.timer = QtCore.QTimer()
        self.current_index = 0
        self.chunk_size = 100  # Number of points to plot at a time
        
        # Applying button functionalities
        self.browseBtn.clicked.connect(self.browseTheSignal)
        self.startBtn.clicked.connect(self.startTheSignal)
        self.timer.timeout.connect(self.updatePlot)
        self.pauseBtn.clicked.connect(self.pauseTheSignal)
        self.rewindBtn.clicked.connect(self.rewindTheSignal)
        

    def browseTheSignal(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption="Select a CSV file", directory="/D", filter="(*.csv)"
        )
        print(filePath)
        if filePath:
            self.df = pd.read_csv(filePath, header=None)

    def startTheSignal(self):
        if self.df is not None and not self.df.empty and not len(self.browsedData_y):
            self.browsedData_y = self.df.to_numpy().flatten()
            # print(self.browsedData_y)
            # print(self.browsedData_y.shape)
            data_x = np.arange(len(self.browsedData_y))
            self.data_x = data_x
            self.graphwidget.clear()  # Clear the existing plot            
        self.graphwidget.plotItem.setXRange(self.current_index, self.current_index + self.chunk_size , padding=0)  # Set initial x-axis range
        self.graphwidget.plotItem.setYRange(-2, 2, padding = 0)
        self.timer.start(100)  # Start the timer with a 100 ms interval (Note: the timer times out every 100ms(as given in the argument) and starts another 100ms, which leads to invoking the "updatePlot" every timeout until the timer stops "self.timer.stop()")

    def updatePlot(self):
        if self.current_index < len(self.browsedData_y):
            # Determine the range of data to plot in this frame
            end_index = min(self.current_index + self.chunk_size, len(self.browsedData_y))
            segment_x = self.data_x[self.current_index:end_index]
            segment_y = self.browsedData_y[self.current_index:end_index]

            # Update the plot with new data
            self.graphwidget.plot(segment_x, segment_y, pen='b', clear=False)
            self.current_index+=10
            # self.current_index += self.chunk_size

            # Optionally, adjust the view to follow the plot
            # self.graphwidget.plotItem.setXRange(
            #     max(0, self.current_index - self.chunk_size),
            #     self.current_index,
            #     padding=0
            # )
            self.graphwidget.plotItem.setXRange(
                self.current_index,
                end_index,
                padding=0
            )
            self.graphwidget.plotItem.setYRange(-1, 1, padding = 0)
        else:
            self.timer.stop()  # Stop the timer when the end is reached
            self.current_index = 0
            
            
            
    def pauseTheSignal(self):
        
        self.timer.stop()   # stop the timer to stop the graph from updating itself
        
    
    
    
    def rewindTheSignal(self):
        self.current_index = 0
        self.graphwidget.clear()
        self.startTheSignal()
            



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

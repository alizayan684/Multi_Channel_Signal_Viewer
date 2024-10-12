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
        self.df_1 = None  # No data initially
        self.df_2 = None
        self.browsedData_y = []
        self.browsedData_y_2 = []
        self.timer = QtCore.QTimer()
        self.timer_2 = QtCore.QTimer()
        self.current_index = 0   # the current index in the graph
        self.current_index_2 = 0
        self.chunk_size = 0  # initializing number of points to plot at a time
        self.isPaused = False
        self.isPaused_2 = False
        self.isLinked = False # initializing both graphs not to be linked.
        
        # Applying button functionalities for first graph
        self.browseBtn.clicked.connect(self.browseTheSignal)
        self.startBtn.clicked.connect(self.startTheSignal)
        self.timer.timeout.connect(self.updatePlot_1)
        self.pauseBtn.clicked.connect(self.pauseTheSignal)
        self.rewindBtn.clicked.connect(self.rewindTheSignal)
        # Applying button functionalities for second graph
        self.browseBtn2.clicked.connect(self.browseTheSignal)
        self.startBtn2.clicked.connect(self.startTheSignal)
        self.timer_2.timeout.connect(self.updatePlot_2)
        self.pauseBtn2.clicked.connect(self.pauseTheSignal)
        self.rewindBtn2.clicked.connect(self.rewindTheSignal)
        # Applying the linking functionality
        self.linkBtn.clicked.connect(self.linkGraphs)

    def browseTheSignal(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption="Select a CSV file", directory="/D", filter="(*.csv)"
        )
        print(filePath)
        if filePath:
            # check whether the clicked btn is for graph_1 or graph_2
            if self.sender() == self.browseBtn:
                self.df_1 = pd.read_csv(filePath, header=None)
                self.browsedData_y = [] # clearing the self.browsedData_y to use the new data of a newly browsed file
                self.isPaused = False
                self.current_index = 0 # to start plotting from the beginning every time I browse a new file.
            else:
                self.df_2 = pd.read_csv(filePath, header=None)
                self.browsedData_y2 = [] 
                self.isPaused2 = False
                self.current_index_2 = 0
                
                

    def startTheSignal(self):
        if not self.isLinked:
            if self.sender() == self.startBtn or self.sender() == self.rewindBtn:
                if self.df_1 is not None and not self.df_1.empty and not len(self.browsedData_y) and not self.isPaused:
                    self.browsedData_y = self.df_1.to_numpy().flatten()
                    self.chunk_size = int(len(self.browsedData_y)/3.0)
                    data_x = np.arange(len(self.browsedData_y))
                    self.data_x = data_x
                    self.graphWidget.clear()  # Clear the existing plot            
                    self.graphWidget.plotItem.setXRange(self.current_index, self.current_index + self.chunk_size , padding=0)  # Set initial x-axis range
                    self.graphWidget.plotItem.setYRange(-2, 2, padding = 0)
                self.timer.start(100)  # Start the timer with a 100 ms interval (Note: the timer times out every 100ms(as given in the argument) and starts another 100ms, which leads to invoking the "updatePlot" every timeout until the timer stops "self.timer.stop()")
            
            else:
                if self.df_2 is not None and not self.df_2.empty and not len(self.browsedData_y_2) and not self.isPaused_2:
                    self.browsedData_y_2 = self.df_2.to_numpy().flatten()
                    self.chunk_size = int(len(self.browsedData_y_2)/3.0)
                    data_x_2 = np.arange(len(self.browsedData_y_2))
                    self.data_x_2 = data_x_2
                    self.graphWidget_2.clear()  # Clear the existing plot            
                    self.graphWidget_2.plotItem.setXRange(self.current_index_2, self.current_index_2 + self.chunk_size , padding=0)  # Set initial x-axis range
                    self.graphWidget_2.plotItem.setYRange(-2, 2, padding = 0)
                self.timer_2.start(100)
        
        # graphs are linked:  
        else:
            # adjusting the current index to make the 2 graphs at the same time frame as the delayed one (the one with the smaller current index)
            if self.current_index > self.current_index_2:
                self.current_index = self.current_index_2
            else:
                self.current_index_2 = self.current_index
                
            if self.df_1 is not None and not self.df_1.empty:  # if dataframe of first graph contains data:
                if not len(self.browsedData_y) and not self.isPaused:
                    self.browsedData_y = self.df_1.to_numpy().flatten()
                    self.chunk_size = int(len(self.browsedData_y)/3.0)
                    data_x = np.arange(len(self.browsedData_y))
                    self.data_x = data_x
                    self.graphWidget.clear()  # Clear the existing plot            
                    self.graphWidget.plotItem.setXRange(self.current_index, self.current_index + self.chunk_size , padding=0)  # Set initial x-axis range
                    self.graphWidget.plotItem.setYRange(-2, 2, padding = 0)
                if self.df_2 is not None and not self.df_2.empty:  # if dataframe of first graph contains data:
                    if not len(self.browsedData_y_2) and not self.isPaused_2:
                        self.browsedData_y_2 = self.df_2.to_numpy().flatten()
                    
                        data_x_2 = np.arange(len(self.browsedData_y_2))
                        self.data_x_2 = data_x_2
                        self.graphWidget_2.clear()  # Clear the existing plot            
                        self.graphWidget_2.plotItem.setXRange(self.current_index_2, self.current_index_2 + self.chunk_size , padding=0)  # Set initial x-axis range
                        self.graphWidget_2.plotItem.setYRange(-2, 2, padding = 0)   
            self.timer.start(100)
            self.timer_2.start(100)
            print("both signals started moving now")

    # for updating the first graph for the cine mode.
    def updatePlot_1(self):
        if self.current_index < len(self.browsedData_y):
            # Determine the range of data to plot in this frame
            end_index = min(self.current_index + self.chunk_size, len(self.browsedData_y))
            segment_x = self.data_x[self.current_index:end_index]
            segment_y = self.browsedData_y[self.current_index:end_index]
            # Update the plot with new data
            self.graphWidget.plot(segment_x, segment_y, pen='b', clear=False)
            # updating the view to follow the signal until reaching the end of the signal so the graph wouldn't expand
            if end_index != len(self.browsedData_y):
                self.graphWidget.plotItem.setXRange(
                    self.current_index,
                    end_index,
                    padding=0
                )
                updateViewStep = 10
                self.current_index+= updateViewStep
            else:
                self.timer.stop()
                self.current_index = 0    
            self.graphWidget.plotItem.setYRange(-1, 1, padding = 0)
        
        else:
            self.timer.stop()  # Stop the timer when the end is reached
            self.current_index = 0  # resetting the starting index

    
    # for updating the second graph for the cine mode.     
    def updatePlot_2(self):
        if self.current_index_2 < len(self.browsedData_y_2):
            # Determine the range of data to plot in this frame
            end_index_2 = min(self.current_index_2 + self.chunk_size, len(self.browsedData_y_2))
            segment_x_2 = self.data_x_2[self.current_index_2:end_index_2]
            segment_y_2 = self.browsedData_y_2[self.current_index_2:end_index_2]
            # Update the plot with new data
            self.graphWidget_2.plot(segment_x_2, segment_y_2, pen='b', clear=False)
            # updating the view to follow the signal until reaching the end of the signal so the graph wouldn't expand
            if end_index_2 != len(self.browsedData_y_2):
                self.graphWidget_2.plotItem.setXRange(
                    self.current_index_2,
                    end_index_2,
                    padding=0
                )
                updateViewStep_2 = 10
                self.current_index_2+= updateViewStep_2
            else:
                self.timer_2.stop()
                self.current_index_2 = 0    
                self.graphWidget_2.plotItem.setYRange(-1, 1, padding = 0)
        
        else:
            self.timer_2.stop()  # Stop the timer when the end is reached
            self.current_index_2 = 0
            
            
            
    
            
            
    def pauseTheSignal(self):
        # graphs not linked:
        if not self.isLinked:
            if self.sender() == self.pauseBtn:
                self.timer.stop()   # stop the timer to stop the graph from updating itself
                self.isPaused = True
            else:
                self.timer_2.stop()   # stop the timer to stop the graph from updating itself
                self.isPaused_2 = True
        # graphs linked:
        else:
            self.timer.stop()
            self.timer_2.stop()
            self.isPaused = True
            self.isPaused_2 = True
    
    
    
    def rewindTheSignal(self):
        # graphs not linked:
        if not self.isLinked:
            #checking the pressed btn(first or second graph)
            if self.sender() == self.rewindBtn:
                self.current_index = 0
                self.graphWidget.clear()
                self.startTheSignal()
            else:
                self.current_index_2 = 0
                self.graphWidget_2.clear()
                self.startTheSignal()
        # graphs linked:
        else:
            self.current_index = 0
            self.current_index_2 = 0
            self.graphWidget.clear()
            self.graphWidget_2.clear()
            self.startTheSignal()
            
            
    def linkGraphs(self):
        if self.isLinked == True:
            self.isLinked = False
        else:
            self.isLinked = True
            # at linking if the first is moving and the second is paused, change them to be both moving and from the smaller time frame without needing to press start:
            if not self.isPaused and self.isPaused_2:
                self.isPaused_2 = False
                self.startTheSignal()
            # same thing if the second is moving and the first is paused:
            elif not self.isPaused_2 and self.isPaused:
                self.isPaused = False
                self.startTheSignal()
            # if both are moving, let them keep moving but from the same time frame without needing to press the start btn.
            elif not self.isPaused and not self.isPaused_2:
                self.timer.stop()
                self.timer_2.stop()  # we stopped both timers to avoid conflicts between them during updating so when they start again, they timeout at the same time and update the graph at the same time.
                self.startTheSignal() # start again 



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

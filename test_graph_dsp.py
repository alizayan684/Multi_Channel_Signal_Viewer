import sys
from   PyQt6 import QtWidgets, QtCore
from main_window import Ui_SignalViewer
import pyqtgraph as pg
import numpy as np
import pandas as pd

class MainWindow(Ui_SignalViewer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.df_1 = None  # No data initially
        self.df_2 = None
        self.browsedData_y = []
        self.browsedData_y_2 = []
        self.pastSignalsY_1 = []
        self.pastSignalsY_2 = []
        self.pastSignalsX_1 = []
        self.pastSignalsX_2 = []
        self.timer = QtCore.QTimer()
        self.timer_2 = QtCore.QTimer()
        self.current_index = 0   # the current index in the graph
        self.current_index_2 = 0
        self.chunk_size = 0  # initializing number of points to plot at a time
        self.isPaused = False
        self.isPaused_2 = False
        self.isLinked = False # initializing both graphs not to be linked.
        
        # Applying button functionalities for first graph
        self.addFileButton.clicked.connect(self.browseTheSignal)
        self.startButton_1.clicked.connect(self.startTheSignal)
        self.timer.timeout.connect(self.updatePlot_1)
        self.stopButton_1.clicked.connect(self.pauseTheSignal)
        self.rewindButton_1.clicked.connect(self.rewindTheSignal)
        
        # Applying button functionalities for second graph
        self.addFileButton.clicked.connect(self.browseTheSignal) # TODO : change the function of the second graph's add file button
        self.startButton_2.clicked.connect(self.startTheSignal)
        self.timer_2.timeout.connect(self.updatePlot_2)
        self.stopButton_2.clicked.connect(self.pauseTheSignal)
        self.rewindButton_2.clicked.connect(self.rewindTheSignal)
        # Applying the linking functionality
        self.linkButton.clicked.connect(self.linkGraphs)

    def browseTheSignal(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption="Select a CSV file", directory="/D", filter="(*.csv)"
        )
        print(filePath)
        if filePath:
            # check whether the clicked btn is for graph_1 or graph_2
            if self.sender() == self.addFileButton:
                self.df_1 = pd.read_csv(filePath, header=None)
                self.browsedData_y = [] # clearing the self.browsedData_y to use the new data of a newly browsed file
                self.isPaused = False
                self.current_index = 0 # to start plotting from the beginning every time I browse a new file.
            else:
                self.df_2 = pd.read_csv(filePath, header=None)
                self.browsedData_y_2 = [] 
                self.isPaused_2 = False
                self.current_index_2 = 0
                
                

    def startTheSignal(self):
        if not self.isLinked:
            if self.sender() == self.startButton_1 or self.sender() == self.rewindButton_1:
                if self.df_1 is not None and not self.df_1.empty and not len(self.browsedData_y) and not self.isPaused:
                    self.browsedData_y = self.df_1.to_numpy().flatten()
                    self.pastSignalsY_1.append(self.browsedData_y)
                    self.chunk_size = int(len(self.browsedData_y)/3.0)
                    data_x = np.arange(len(self.browsedData_y))
                    self.data_x = data_x
                    self.plotWidget_1.clear()  # Clear the existing plot            
                    self.plotWidget_1.plotItem.setXRange(self.current_index, self.current_index + self.chunk_size , padding=0)  # Set initial x-axis range
                    self.plotWidget_1.plotItem.setYRange(-2, 2, padding = 0)
                self.timer.start(100)  # Start the timer with a 100 ms interval (Note: the timer times out every 100ms(as given in the argument) and starts another 100ms, which leads to invoking the "updatePlot" every timeout until the timer stops "self.timer.stop()")
            
            else:
                if self.df_2 is not None and not self.df_2.empty and len(self.browsedData_y_2) == 0 and not self.isPaused_2:
                    self.browsedData_y_2 = self.df_2.to_numpy().flatten()
                    self.pastSignalsY_2.append(self.browsedData_y_2)
                    self.chunk_size = int(len(self.browsedData_y_2)/3.0)
                    data_x_2 = np.arange(len(self.browsedData_y_2))
                    self.data_x_2 = data_x_2
                    self.plotWidget_2.clear()  # Clear the existing plot            
                    self.plotWidget_2.plotItem.setXRange(self.current_index_2, self.current_index_2 + self.chunk_size , padding=0)  # Set initial x-axis range
                    self.plotWidget_2.plotItem.setYRange(-2, 2, padding = 0)
                self.timer_2.start(100)
        
        # graphs are linked:  
        else:
            # adjusting the current index to make the 2 graphs at the same time frame as the delayed one (the one with the smaller current index)
            if self.current_index > self.current_index_2:
                self.current_index = self.current_index_2
            else:
                self.current_index_2 = self.current_index
                
            if self.df_1 is not None and not self.df_1.empty:  # if dataframe of first graph contains data:
                if len(self.browsedData_y) == 0 and not self.isPaused:
                    self.browsedData_y = self.df_1.to_numpy().flatten()
                    self.pastSignalsY_1.append(self.browsedData_y)
                    self.chunk_size = int(len(self.browsedData_y)/3.0)
                    data_x = np.arange(len(self.browsedData_y))
                    self.data_x = data_x
                    self.plotWidget_1.clear()  # Clear the existing plot            
                    self.plotWidget_1.plotItem.setXRange(self.current_index, self.current_index + self.chunk_size , padding=0)  # Set initial x-axis range
                    self.plotWidget_1.plotItem.setYRange(-2, 2, padding = 0)
                if self.df_2 is not None and not self.df_2.empty:  # if dataframe of first graph contains data:
                    if not len(self.browsedData_y_2) and not self.isPaused_2:
                        self.browsedData_y_2 = self.df_2.to_numpy().flatten()
                        self.pastSignalsY_2.append(self.browsedData_y_2)
                        data_x_2 = np.arange(len(self.browsedData_y_2))
                        self.data_x_2 = data_x_2
                        self.plotWidget_2.clear()  # Clear the existing plot            
                        self.plotWidget_2.plotItem.setXRange(self.current_index_2, self.current_index_2 + self.chunk_size , padding=0)  # Set initial x-axis range
                        self.plotWidget_2.plotItem.setYRange(-2, 2, padding = 0)   
            self.timer.start(100)
            self.timer_2.start(100)
            print("both signals started moving now")

    # for updating the first graph for the cine mode.
    def updatePlot_1(self):
        maxLength = len(self.browsedData_y) # initializing length of the longest signal to move until its end if there are more than one signal plotted
        for signalIdx in range (len(self.pastSignalsY_1)):   # getting the longest signal in the plotted signals and its idx.
            maxLength = max(len(self.pastSignalsY_1[signalIdx]), maxLength)
            if len(self.pastSignalsY_1[signalIdx]) >= maxLength:
                maxLengthIdx = signalIdx  
            
        if self.current_index < maxLength:
            # Determine the range of data to plot in this frame
            end_index = min(self.current_index + self.chunk_size, len(self.browsedData_y))
            segment_x = self.data_x[self.current_index:end_index]
            segment_y = self.browsedData_y[self.current_index:end_index]
            # Update the plot with new data
            self.plotWidget_1.plot(segment_x, segment_y, pen='b', clear=False)
            # updating the view to follow the signal until reaching the end of the signal so the graph wouldn't expand
            if end_index != maxLength:
                self.plotWidget_1.plotItem.setXRange(
                    self.current_index,
                    end_index,
                    padding=0
                )
                updateViewStep = 10
                self.current_index+= updateViewStep
            else:
                self.timer.stop()
                self.current_index = 0    
            self.plotWidget_1.plotItem.setYRange(-1, 1, padding = 0)
        
        else:
            self.timer.stop()  # Stop the timer when the end is reached
            self.current_index = 0  # resetting the starting index

    
    # for updating the second graph for the cine mode.     
    def updatePlot_2(self):
        maxLength = len(self.browsedData_y_2) # initializing length of the longest signal to move until its end if there are more than one signal plotted
        for signalIdx in range (len(self.pastSignalsY_2)):   # getting the longest signal in the plotted signals and its idx.
            maxLength = max(len(self.pastSignalsY_2[signalIdx]), maxLength)
            if len(self.pastSignalsY_2[signalIdx]) >= maxLength:
                maxLengthIdx = signalIdx  # we will use it to in plotting to use the y-coordinates of the longest signal with its correct x-coordinates.
                
        if self.current_index_2 < maxLength:
            # Determine the range of data to plot in this frame
            end_index_2 = min(self.current_index_2 + self.chunk_size, maxLength)
            
            for signalIdx in range (len(self.pastSignalsY_2)):  # plotting all stored signals on the graph
                segment_x = self.pastSignalsX_2[signalIdx][self.current_index_2:end_index_2]
                segment_y = self.pastSignalsY_2[signalIdx][self.current_index_2:end_index_2]
                self.plotWidget_2.plot(segment_x, segment_y, pen='b', clear=False)
            
            # updating the view to follow the signal until reaching the end of the signal so the graph wouldn't expand
            if end_index_2 != maxLength:
                self.plotWidget_2.plotItem.setXRange(
                    self.current_index_2,
                    end_index_2,
                    padding=0
                )
                updateViewStep_2 = 10
                self.current_index_2+= updateViewStep_2
            else:
                self.timer_2.stop()
                self.current_index_2 = 0    
                self.plotWidget_2.plotItem.setYRange(-1, 1, padding = 0)
        
        else:
            self.timer_2.stop()  # Stop the timer when the end is reached
            self.current_index_2 = 0
            
            
            
    
            
            
    def pauseTheSignal(self):
        # graphs not linked:
        if not self.isLinked:
            if self.sender() == self.stopButton_1:
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
            if self.sender() == self.rewindButton_1:
                self.current_index = 0
                self.plotWidget_1.clear()
                self.startTheSignal()
            else:
                self.current_index_2 = 0
                self.plotWidget_2.clear()
                self.startTheSignal()
        # graphs linked:
        else:
            self.current_index = 0
            self.current_index_2 = 0
            self.plotWidget_1.clear()
            self.plotWidget_2.clear()
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
import sys
from   PySide6 import QtWidgets, QtCore
from   PySide6.QtWidgets import QColorDialog, QApplication
from main_window import Ui_SignalViewer
import pyqtgraph as pg
import numpy as np
import pandas as pd
from pathlib import Path

class CheckableLabelItem(QtWidgets.QWidget):
    def __init__(self, index, text, color, graphObj, graphNum, parent=None):
        super().__init__(parent)
        # Initial variables needed for updating the new label onto the choice boxes and the signal names
        self.index = index
        self.graphObj = graphObj
        self.graphNum = graphNum

        # Create a checkbox for showing and hiding the signal
        self.checkbox = QtWidgets.QCheckBox()
        if(self.graphNum == 1):
            self.checkbox.setChecked(not self.graphObj.hidden_1[self.index])
        else:
            self.checkbox.setChecked(not self.graphObj.hidden_2[self.index])
        self.setCheckboxColor(color)
        self.checkbox.setFixedWidth(16)
        self.checkbox.setFixedHeight(16)

        # Create a label using the signal's name
        self.label = QtWidgets.QLabel(text)

        # Set Horizontal layout
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Set height for our object to allow the label's text to be completely visible
        self.setFixedHeight(38)

        # Enable edit text by double clicking
        self.label.mouseDoubleClickEvent = self.editText

        self.checkbox.stateChanged.connect(self.onToggle)
    
    def setCheckboxColor(self, color):
        formattedColor = f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}" # Format the rgb tuple into a hex string so that stylesheet can read their properties
        self.checkbox.setStyleSheet(f"""
            QCheckBox {{
                spacing: 5px;
                padding: 0px;
            }}
            QCheckBox::indicator {{
                width: 10px;
                height: 10px;
                border: 2px solid #888;
                padding: 0px;
            }}
            QCheckBox::indicator:checked {{
                background-color: {formattedColor};
                border: 2px solid {formattedColor};
            }}
            QCheckBox::indicator:unchecked {{
                background-color: #FFF;
            }}
        """)

    def editText(self, event):
        new_text, ok = QtWidgets.QInputDialog.getText(self, "Edit Signal Label", f"Enter New Label For {self.label.text()}:", text=self.label.text())
        if ok and new_text:
            self.label.setText(new_text)
            if(self.graphNum == 1):
                self.graphObj.signalNames_1[self.index] = new_text
                self.graphObj.titleChannelBox_1.setItemText(self.index + 1, new_text)
                self.graphObj.colorMoveBox_1.setItemText(self.index + 1, new_text)
            else:
                self.graphObj.signalNames_2[self.index] = new_text
                self.graphObj.titleChannelBox_2.setItemText(self.index + 1, new_text)
                self.graphObj.colorMoveBox_2.setItemText(self.index + 1, new_text)
    
    def onToggle(self):
        if(self.graphNum == 1):
            if(self.checkbox.isChecked()):
                self.graphObj.showTheSignal_1(self.index)
            else:
                self.graphObj.hideTheSignal_1(self.index)
        else:
            if(self.checkbox.isChecked()):
                self.graphObj.showTheSignal_2(self.index)
            else:
                self.graphObj.hideTheSignal_2(self.index)

    # Needed for the case of moving some signals to a new graph, the old signals count will change and thus some of them will have their index decremented by 1
    def updateIndex(self, newIndex):
        self.index = newIndex

from non_rectangular import Window
class MainWindow(Ui_SignalViewer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.df_1 = None  # No data initially
        self.df_2 = None
        self.filePaths_1 = []
        self.filePaths_2 = []
        self.non_rect_window = None
        self.browsedData_y = []
        self.browsedData_y_2 = []
        self.pastSignalsY_1 = []
        self.pastSignalsY_2 = []
        self.pastSignalsX_1 = []
        self.pastSignalsX_2 = []
        self.plotCurves_1 = []
        self.plotCurves_2 = []
        self.signalNames_1 = []
        self.signalNames_2 = []
        self.plotColors_1 = []
        self.plotColors_2 = []
        self.labelItems_1 = []
        self.labelItems_2 = []
        self.widgetItems_1 = []
        self.widgetItems_2 = []
        self.timer = QtCore.QTimer()
        self.timer_2 = QtCore.QTimer()
        self.current_index = 0   # the current index in the graph
        self.current_index_2 = 0
        self.chunk_size = 0  # initializing number of points to plot at a time
        self.isPaused = False
        self.isPaused_2 = False
        self.isLinked = False # initializing both graphs not to be linked.
        self.hidden_1 = []
        self.hidden_2 = []
        self.maxPanningValue_1 = 0
        self.maxPanningValue_2 = 0
        self.minY = -2
        self.maxY = 2
        
        self.hidden = False
        self.zoom_level = 0  # Default zoom level
        self.zoom_level_2 = 0
        self.min_zoom_level = 0
        self.max_zoom_level = 100  # Maximum zoom level
        self.nonRectGraphButton.clicked.connect(self.openNonRectGraph)
        # Applying button functionalities for first graph #############################
        self.addFileButton.clicked.connect(self.browseTheSignal)
        self.linkButton.clicked.connect(self.linkGraphs)

        # Applying button functionalities for first graph
        self.startButton_1.clicked.connect(self.startTheSignal)
        self.timer.timeout.connect(self.updatePlot_1)
        self.stopButton_1.clicked.connect(self.pauseTheSignal)
        self.rewindButton_1.clicked.connect(self.rewindTheSignal)
        self.moveButton_1.clicked.connect(self.moveTheSignal_1)
        
        # Applying button functionalities for second graph
        self.speedSlider_1.valueChanged.connect(self.updateSpeed_1)
        self.colorButton_1.clicked.connect(self.colorSignal_1)
        self.zoomInButton_1.clicked.connect(self.zoom_1)
        self.zoomOutButton_1.clicked.connect(self.zoom_out_1)
        self.titleButton_1.clicked.connect(self.labelSignal_1)

        self.horizontalScrollBar_1.setRange(0, self.maxPanningValue_1)  # Scroll range based on data
        self.horizontalScrollBar_1.setValue(0)  # Start at the beginning
        # Connect the scrollbar's valueChanged signal to the update function
        self.horizontalScrollBar_1.valueChanged.connect(self.updateHorizontalScroll_1)

        self.verticalScrollBar_1.setRange(-2, 2)  # Scroll range based on data
        self.verticalScrollBar_1.setValue(0)  # Start at the beginning
        # Connect the scrollbar's valueChanged signal to the update function
        self.verticalScrollBar_1.valueChanged.connect(self.updateVerticalScroll_1)

        # Applying button functionalities for second graph ###############################
        self.startButton_2.clicked.connect(self.startTheSignal)
        self.timer_2.timeout.connect(self.updatePlot_2)
        self.stopButton_2.clicked.connect(self.pauseTheSignal)
        self.rewindButton_2.clicked.connect(self.rewindTheSignal)
        self.colorButton_2.clicked.connect(self.colorTheSignal_2)
        self.moveButton_2.clicked.connect(self.moveTheSignal_2)

        self.speedSlider_2.valueChanged.connect(self.updateSpeed_2)
        self.zoomInButton_2.clicked.connect(self.zoom_2)
        self.zoomOutButton_2.clicked.connect(self.zoom_out_2)

        self.horizontalScrollBar_2.setRange(0, self.maxPanningValue_2)  # Scroll range based on data
        self.horizontalScrollBar_2.setValue(0)  # Start at the beginning
        # Connect the scrollbar's valueChanged signal to the update function
        self.horizontalScrollBar_2.valueChanged.connect(self.updateHorizontalScroll_2)

        self.verticalScrollBar_2.setRange(-2, 2)  # Scroll range based on data
        self.verticalScrollBar_2.setValue(0)  # Start at the beginning
        # Connect the scrollbar's valueChanged signal to the update function
        self.verticalScrollBar_2.valueChanged.connect(self.updateVerticalScroll_2)

        # Applying the linking functionality
        self.linkButton.clicked.connect(self.linkGraphs)

    def browseTheSignal(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption="Select a CSV file", dir="/D", filter="(*.csv)"
        )
        if filePath:
            currSignalName = Path(filePath).name[0 : -4]
            currColor = self.generateRandomColor()
            # Check whether the clicked btn is for graph_1 or graph_2
            if self.graphSelectBox.currentIndex() == 0:
                self.signalNames_1.append(currSignalName)
                self.plotCurves_1.append(self.plotWidget_1.plotItem.plot())
                self.plotColors_1.append(currColor)
                self.hidden_1.append(False)
                self.titleChannelBox_1.addItem(currSignalName)
                self.colorMoveBox_1.addItem(currSignalName)
                
                self.filePaths_1.append(filePath)
                self.df_1 = pd.read_csv(filePath, header=None)
                self.browsedData_y = [] # clearing the self.browsedData_y to use the new data of a newly browsed file
                self.isPaused = False
                self.current_index = 0 # to start plotting from the beginning every time I browse a new file.
                
                # Adding Signal Name To Our Labels List
                labelItem = CheckableLabelItem(len(self.labelItems_1), currSignalName, currColor, self, 1)
                self.labelItems_1.append(labelItem)
                listWidgetItem = QtWidgets.QListWidgetItem()
                listWidgetItem.setSizeHint(labelItem.sizeHint())  # Set the size hint
                self.listChannelsWidget_1.addItem(listWidgetItem)
                self.listChannelsWidget_1.setItemWidget(listWidgetItem, labelItem)  # Set the widget
                self.widgetItems_1.append(listWidgetItem)

            else:   
                self.signalNames_2.append(currSignalName)
                self.plotCurves_2.append(self.plotWidget_1.plotItem.plot())
                self.plotColors_2.append(currColor)
                self.hidden_2.append(False)
                self.titleChannelBox_2.addItem(currSignalName)
                self.colorMoveBox_2.addItem(currSignalName)

                self.filePaths_2.append(filePath)
                self.df_2 = pd.read_csv(filePath, header=None)
                self.browsedData_y_2 = [] 
                self.isPaused_2 = False
                self.current_index_2 = 0

                # Adding Signal Name To Our Labels List
                labelItem = CheckableLabelItem(len(self.labelItems_2), currSignalName, currColor, self, 2)
                self.labelItems_2.append(labelItem)
                listWidgetItem = QtWidgets.QListWidgetItem()
                listWidgetItem.setSizeHint(labelItem.sizeHint())  # Set the size hint
                self.listChannelsWidget_2.addItem(listWidgetItem)
                self.listChannelsWidget_2.setItemWidget(listWidgetItem, labelItem)  # Set the widget
                self.widgetItems_2.append(listWidgetItem)

            self.startTheSignal()
                
    def startTheSignal(self):
        if not self.isLinked:
            if self.graphSelectBox.currentIndex() == 0 or self.sender() == self.startButton_1 or self.sender() == self.rewindButton_1:
                if self.df_1 is not None and not self.df_1.empty and not len(self.browsedData_y) and not self.isPaused:
                    self.browsedData_y = self.df_1.to_numpy().flatten()
                    self.pastSignalsY_1.append(self.browsedData_y)
                    self.chunk_size = int(len(self.browsedData_y)/3.0)
                    data_x = np.arange(len(self.browsedData_y))
                    self.data_x = data_x
                    self.pastSignalsX_1.append(self.data_x)            
                    self.plotWidget_1.plotItem.setXRange(self.current_index, self.current_index + self.chunk_size , padding=0)  # Set initial x-axis range
                    self.maxPanningValue_1 = max(self.current_index + self.chunk_size, self.maxPanningValue_1)
                    self.plotWidget_1.plotItem.setYRange(-2, 2, padding = 0)
                # Start the timer with a 100 ms interval (Note: the timer times out every 100ms(as given in the argument) and starts another 100ms, which leads to invoking the "updatePlot" every timeout until the timer stops "self.timer.stop()")
                self.timer.start(100)
            
            else:
                if self.df_2 is not None and not self.df_2.empty and len(self.browsedData_y_2) == 0 and not self.isPaused_2:
                    self.browsedData_y_2 = self.df_2.to_numpy().flatten()
                    self.pastSignalsY_2.append(self.browsedData_y_2)
                    self.chunk_size = int(len(self.browsedData_y_2)/3.0)
                    data_x_2 = np.arange(len(self.browsedData_y_2))
                    self.data_x_2 = data_x_2
                    self.pastSignalsX_2.append(self.data_x_2)            
                    self.plotWidget_2.plotItem.setXRange(self.current_index_2, self.current_index_2 + self.chunk_size , padding=0)  # Set initial x-axis range
                    self.maxPanningValue_2 = max(self.current_index_2 + self.chunk_size, self.maxPanningValue_2)
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
                    self.pastSignalsX_1.append(self.data_x)             
                    self.plotWidget_1.plotItem.setXRange(self.current_index, self.current_index + self.chunk_size , padding=0)  # Set initial x-axis range
                    self.maxPanningValue_1 = max(self.current_index + self.chunk_size, self.maxPanningValue_1)
                    self.plotWidget_1.plotItem.setYRange(-2, 2, padding = 0)
                if self.df_2 is not None and not self.df_2.empty:  # if dataframe of first graph contains data:
                    if not len(self.browsedData_y_2) and not self.isPaused_2:
                        self.browsedData_y_2 = self.df_2.to_numpy().flatten()
                        self.pastSignalsY_2.append(self.browsedData_y_2)
                        data_x_2 = np.arange(len(self.browsedData_y_2))
                        self.data_x_2 = data_x_2
                        self.pastSignalsX_2.append(self.data_x_2)            
                        self.plotWidget_2.plotItem.setXRange(self.current_index_2, self.current_index_2 + self.chunk_size , padding=0)  # Set initial x-axis range
                        self.maxPanningValue_2 = max(self.current_index_2 + self.chunk_size, self.maxPanningValue_2)
                        self.plotWidget_2.plotItem.setYRange(-2, 2, padding = 0)   
            self.timer.start(100)
            self.timer_2.start(100)
            
    # for updating the first graph for the cine mode.
    def updatePlot_1(self):
        maxLength = len(self.browsedData_y) # initializing length of the longest signal to move until its end if there are more than one signal plotted
        for signalIdx in range (len(self.pastSignalsY_1)):   # getting the longest signal in the plotted signals and its idx.
            maxLength = max(len(self.pastSignalsY_1[signalIdx]), maxLength)
            if len(self.pastSignalsY_1[signalIdx]) >= maxLength:
                maxLengthIdx = signalIdx  
            
        if self.current_index < maxLength:
            end_index = min(self.current_index + self.chunk_size, maxLength) # Determine the range of data to plot in this frame
            self.maxPanningValue_1 = max(end_index, self.maxPanningValue_1)  
            self.plotWidget_1.clear() # Clear the graph first so that the widget only contains the latest plots (needed for show and hide functionality)

            for signalIdx in range (len(self.pastSignalsY_1)):  # Plotting all stored signals on the graph
                if not self.hidden_1[signalIdx]:
                    segment_x = self.pastSignalsX_1[signalIdx][self.current_index:end_index]
                    segment_y = self.pastSignalsY_1[signalIdx][self.current_index:end_index]
                    self.plotCurves_1[signalIdx] = self.plotWidget_1.plot(
                        segment_x, segment_y, pen=self.plotColors_1[signalIdx], clear=False, name=self.signalNames_1[signalIdx]
                        )
            
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

        else:
            self.timer.stop()  # Stop the timer when the end is reached
            self.current_index = 0  # resetting the starting index
            self.maxPanningValue_1 = max(maxLength, self.maxPanningValue_1)  

        self.horizontalScrollBar_1.setRange(0, self.maxPanningValue_1)  # Scroll range based on data

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
            self.maxPanningValue_2 = max(end_index_2, self.maxPanningValue_2)
            self.plotWidget_2.clear()
            
            for signalIdx in range (len(self.pastSignalsY_2)):  # plotting all stored signals on the graph
                if not self.hidden_2[signalIdx]:
                    segment_x = self.pastSignalsX_2[signalIdx][self.current_index_2:end_index_2]
                    segment_y = self.pastSignalsY_2[signalIdx][self.current_index_2:end_index_2]
                    self.plotCurves_2[signalIdx] = self.plotWidget_2.plot(
                        segment_x, segment_y, pen=self.plotColors_2[signalIdx], clear=False, name=self.signalNames_2[signalIdx]
                        )
            
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
        
        else:
            self.timer_2.stop()  # Stop the timer when the end is reached
            self.current_index_2 = 0
            self.maxPanningValue_2 = max(maxLength, self.maxPanningValue_2)
        
        self.horizontalScrollBar_2.setRange(0, self.maxPanningValue_2)  # Scroll range based on data
                  
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
                self.maxPanningValue_1 = 0
            else:
                self.current_index_2 = 0
                self.plotWidget_2.clear()
                self.startTheSignal()
                self.maxPanningValue_2 = 0
        # graphs linked:
        else:
            self.current_index = 0
            self.current_index_2 = 0
            self.plotWidget_1.clear()
            self.plotWidget_2.clear()
            self.maxPanningValue_1 = 0
            self.maxPanningValue_2 = 0
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

    def showTheSignal_1(self, index):
        if(self.df_1 is not None):
            self.hidden_1[index] = False
            self.plotCurves_1[index].setVisible(True)

    def hideTheSignal_1(self, index):
        if(self.df_1 is not None):
            self.hidden_1[index] = True
            self.plotCurves_1[index].setVisible(False)
    
    def showTheSignal_2(self, index):
        if(self.df_2 is not None):
            self.hidden_2[index] = False
            self.plotCurves_2[index].setVisible(True)

    def hideTheSignal_2(self, index):
        if(self.df_2 is not None):
            self.hidden_2[index] = True
            self.plotCurves_2[index].setVisible(False)

    def colorTheSignal_1(self):
        if(self.df_1 is not None):
            color = QColorDialog.getColor()
            if color.isValid():
                currIdx = self.colorMoveBox_1.currentIndex() - 1
                currColor = pg.mkPen(color.name())
                if currIdx == -1:
                    for i in range(len(self.plotColors_1)):
                        self.plotColors_1[i] = currColor
                        self.plotCurves_1[i].setPen(currColor)
                        self.labelItems_1[i].setCheckboxColor((color.red(), color.green(), color.blue()))
                else:
                    self.plotColors_1[currIdx] = currColor
                    self.plotCurves_1[currIdx].setPen(currColor)
                    self.labelItems_1[currIdx].setCheckboxColor((color.red(), color.green(), color.blue()))
    
    def colorTheSignal_2(self):
        if(self.df_2 is not None):
            color = QColorDialog.getColor()
            if color.isValid():
                currIdx = self.colorMoveBox_2.currentIndex() - 1
                currColor = pg.mkPen(color.name())
                if currIdx == -1:
                    for i in range(len(self.plotColors_2)):
                        self.plotColors_2[i] = currColor
                        self.plotCurves_2[i].setPen(currColor)
                        self.labelItems_2[i].setCheckboxColor((color.red(), color.green(), color.blue()))
                else:
                    self.plotColors_2[currIdx] = currColor
                    self.plotCurves_2[currIdx].setPen(currColor)
                    self.labelItems_2[currIdx].setCheckboxColor((color.red(), color.green(), color.blue()))

    def moveTheSignal_1(self):
        if(self.df_1 is not None):
            self.graphSelectBox.setCurrentIndex(1) # Needed so that when we call start the signal later in the function it starts the second graph
            currIdx = self.colorMoveBox_1.currentIndex() - 1
            if(currIdx == -1):
                for signalIdx in range(len(self.pastSignalsY_1)):
                    self.signalNames_2.append(self.signalNames_1[signalIdx])
                    self.plotCurves_2.append(self.plotWidget_2.plotItem.plot())
                    self.plotColors_2.append(self.plotColors_1[signalIdx])
                    self.hidden_2.append(self.hidden_1[signalIdx])
                    self.titleChannelBox_2.addItem(self.signalNames_1[signalIdx])
                    self.colorMoveBox_2.addItem(self.signalNames_1[signalIdx])

                    self.filePaths_2.append(self.filePaths_1[signalIdx])
                    self.df_2 = pd.read_csv(self.filePaths_1[signalIdx], header=None)
                    self.browsedData_y_2 = [] 
                    self.isPaused_2 = False
                    self.current_index_2 = 0

                    # Adding Signal Name To Our Labels List
                    labelItem = CheckableLabelItem(len(self.labelItems_2), self.signalNames_2[-1], self.plotColors_2[-1], self, 2)
                    self.labelItems_2.append(labelItem)
                    listWidgetItem = QtWidgets.QListWidgetItem()
                    listWidgetItem.setSizeHint(labelItem.sizeHint())  # Set the size hint
                    self.listChannelsWidget_2.addItem(listWidgetItem)
                    self.listChannelsWidget_2.setItemWidget(listWidgetItem, labelItem)  # Set the widget
                    self.widgetItems_2.append(listWidgetItem)

                    self.startTheSignal()

                self.plotWidget_1.plotItem.clear()
                self.df_1 = None
                self.browsedData_y = []
                self.pastSignalsY_1 = []
                self.pastSignalsX_1 = []
                self.current_index = 0
                self.signalNames_1 = []
                self.plotColors_1 = []
                self.plotCurves_1 = []
                self.hidden_1 = []
                self.filePaths_1 = []
                self.labelItems_1 = []
                self.listChannelsWidget_1.clear()
                self.titleChannelBox_1.clear()
                self.titleChannelBox_1.addItem("All Channels")
                self.colorMoveBox_1.clear()
                self.colorMoveBox_1.addItem("All Channels")

            else:
                self.signalNames_2.append(self.signalNames_1[currIdx])
                self.plotCurves_2.append(self.plotWidget_2.plotItem.plot())
                self.plotColors_2.append(self.plotColors_1[currIdx])
                self.hidden_2.append(self.hidden_1[currIdx])
                self.titleChannelBox_2.addItem(self.signalNames_1[currIdx])
                self.colorMoveBox_2.addItem(self.signalNames_1[currIdx])

                self.filePaths_2.append(self.filePaths_1[currIdx])
                self.df_2 = pd.read_csv(self.filePaths_1[currIdx], header=None)
                self.browsedData_y_2 = [] 
                self.isPaused_2 = False
                self.current_index_2 = 0

                # Adding Signal Name To Our Labels List
                labelItem = CheckableLabelItem(len(self.labelItems_2), self.signalNames_2[-1], self.plotColors_2[-1], self, 2)
                self.labelItems_2.append(labelItem)
                listWidgetItem = QtWidgets.QListWidgetItem()
                listWidgetItem.setSizeHint(labelItem.sizeHint())  # Set the size hint
                self.listChannelsWidget_2.addItem(listWidgetItem)
                self.listChannelsWidget_2.setItemWidget(listWidgetItem, labelItem)  # Set the widget
                self.widgetItems_2.append(listWidgetItem)

                self.plotWidget_1.plotItem.removeItem(self.plotCurves_1[currIdx])
                self.listChannelsWidget_1.takeItem(self.listChannelsWidget_1.row(self.widgetItems_1[currIdx]))  # Remove it
                self.titleChannelBox_1.removeItem(currIdx + 1)
                self.colorMoveBox_1.removeItem(currIdx + 1)
                
                for signalIdx in range(currIdx, len(self.pastSignalsY_1) - 1):
                    self.pastSignalsY_1[signalIdx] = self.pastSignalsY_1[signalIdx + 1]
                    self.pastSignalsX_1[signalIdx] = self.pastSignalsX_1[signalIdx + 1]
                    self.signalNames_1[signalIdx] = self.signalNames_1[signalIdx + 1]
                    self.plotColors_1[signalIdx] = self.plotColors_1[signalIdx + 1]
                    self.plotCurves_1[signalIdx] = self.plotCurves_1[signalIdx + 1]
                    self.hidden_1[signalIdx] = self.hidden_1[signalIdx + 1]
                    self.filePaths_1[signalIdx] = self.filePaths_1[signalIdx + 1]
                    self.widgetItems_1[signalIdx] = self.widgetItems_1[signalIdx + 1]
                    self.labelItems_1[signalIdx] = self.labelItems_1[signalIdx + 1]
                    self.labelItems_1[signalIdx].updateIndex(signalIdx)
                
                self.pastSignalsY_1.pop()
                self.pastSignalsX_1.pop()
                self.signalNames_1.pop()
                self.plotColors_1.pop()
                self.plotCurves_1.pop()
                self.hidden_1.pop()
                self.filePaths_1.pop()
                self.widgetItems_1.pop()
                self.labelItems_1.pop()

                if(len(self.pastSignalsY_1) == 0):
                    self.df_1 = None
                    self.browsedData_y = []
                    self.current_index = 0

                self.startTheSignal()

    def moveTheSignal_2(self):
        if(self.df_2 is not None):
            self.graphSelectBox.setCurrentIndex(0) # Needed so that when we call start the signal later in the function it starts the first graph
            currIdx = self.colorMoveBox_2.currentIndex() - 1
            if(currIdx == -1):
                for signalIdx in range(len(self.pastSignalsY_2)):
                    self.signalNames_1.append(self.signalNames_2[signalIdx])
                    self.plotCurves_1.append(self.plotWidget_1.plotItem.plot())
                    self.plotColors_1.append(self.plotColors_2[signalIdx])
                    self.hidden_1.append(self.hidden_2[signalIdx])
                    self.titleChannelBox_1.addItem(self.signalNames_2[signalIdx])
                    self.colorMoveBox_1.addItem(self.signalNames_2[signalIdx])

                    self.filePaths_1.append(self.filePaths_2[signalIdx])
                    self.df_1 = pd.read_csv(self.filePaths_2[signalIdx], header=None)
                    self.browsedData_y = [] 
                    self.isPaused_1 = False
                    self.current_index = 0

                    # Adding Signal Name To Our Labels List
                    labelItem = CheckableLabelItem(len(self.labelItems_1), self.signalNames_1[-1], self.plotColors_1[-1], self, 1)
                    self.labelItems_1.append(labelItem)
                    listWidgetItem = QtWidgets.QListWidgetItem()
                    listWidgetItem.setSizeHint(labelItem.sizeHint())  # Set the size hint
                    self.listChannelsWidget_1.addItem(listWidgetItem)
                    self.listChannelsWidget_1.setItemWidget(listWidgetItem, labelItem)  # Set the widget
                    self.widgetItems_1.append(listWidgetItem)

                    self.startTheSignal()

                self.plotWidget_2.plotItem.clear()
                self.df_2 = None
                self.browsedData_y_2 = []
                self.pastSignalsY_2 = []
                self.pastSignalsX_2 = []
                self.current_index_2 = 0
                self.signalNames_2 = []
                self.plotColors_2 = []
                self.plotCurves_2 = []
                self.hidden_2 = []
                self.filePaths_2 = []
                self.labelItems_2 = []
                self.listChannelsWidget_2.clear()
                self.titleChannelBox_2.clear()
                self.titleChannelBox_2.addItem("All Channels")
                self.colorMoveBox_2.clear()
                self.colorMoveBox_2.addItem("All Channels")

            else:
                self.signalNames_1.append(self.signalNames_2[currIdx])
                self.plotCurves_1.append(self.plotWidget_1.plotItem.plot())
                self.plotColors_1.append(self.plotColors_2[currIdx])
                self.hidden_1.append(self.hidden_2[currIdx])
                self.titleChannelBox_1.addItem(self.signalNames_2[currIdx])
                self.colorMoveBox_1.addItem(self.signalNames_2[currIdx])

                self.filePaths_1.append(self.filePaths_2[currIdx])
                self.df_1 = pd.read_csv(self.filePaths_2[currIdx], header=None)
                self.browsedData_y = [] 
                self.isPaused_1 = False
                self.current_index = 0

                # Adding Signal Name To Our Labels List
                labelItem = CheckableLabelItem(len(self.labelItems_1), self.signalNames_1[-1], self.plotColors_1[-1], self, 1)
                self.labelItems_1.append(labelItem)
                listWidgetItem = QtWidgets.QListWidgetItem()
                listWidgetItem.setSizeHint(labelItem.sizeHint())  # Set the size hint
                self.listChannelsWidget_1.addItem(listWidgetItem)
                self.listChannelsWidget_1.setItemWidget(listWidgetItem, labelItem)  # Set the widget
                self.widgetItems_1.append(listWidgetItem)

                self.plotWidget_2.plotItem.removeItem(self.plotCurves_2[currIdx])
                self.listChannelsWidget_2.takeItem(self.listChannelsWidget_2.row(self.widgetItems_2[currIdx]))  # Remove it
                self.titleChannelBox_2.removeItem(currIdx + 1)
                self.colorMoveBox_2.removeItem(currIdx + 1)
                
                for signalIdx in range(currIdx, len(self.pastSignalsY_2) - 1):
                    self.pastSignalsY_2[signalIdx] = self.pastSignalsY_2[signalIdx + 1]
                    self.pastSignalsX_2[signalIdx] = self.pastSignalsX_2[signalIdx + 1]
                    self.signalNames_2[signalIdx] = self.signalNames_2[signalIdx + 1]
                    self.plotColors_2[signalIdx] = self.plotColors_2[signalIdx + 1]
                    self.plotCurves_2[signalIdx] = self.plotCurves_2[signalIdx + 1]
                    self.hidden_2[signalIdx] = self.hidden_2[signalIdx + 1]
                    self.filePaths_2[signalIdx] = self.filePaths_2[signalIdx + 1]
                    self.widgetItems_2[signalIdx] = self.widgetItems_2[signalIdx + 1]
                    self.labelItems_2[signalIdx] = self.labelItems_2[signalIdx + 1]
                    self.labelItems_2[signalIdx].updateIndex(signalIdx)
                
                self.pastSignalsY_2.pop()
                self.pastSignalsX_2.pop()
                self.signalNames_2.pop()
                self.plotColors_2.pop()
                self.plotCurves_2.pop()
                self.hidden_2.pop()
                self.filePaths_2.pop()
                self.widgetItems_2.pop()
                self.labelItems_2.pop()

                if(len(self.pastSignalsY_2) == 0):
                    self.df_2 = None
                    self.browsedData_y_2 = []
                    self.current_index_2 = 0

                self.startTheSignal()

    def generateRandomColor(self):
        r = np.random.randint(0, 256)
        g = np.random.randint(0, 256)
        b = np.random.randint(0, 256)
        return (r, g, b)
    
    ###################################################################################################
    def showTheSignal(self):
        if(self.df is not None):
            self.plotCurve.setVisible(True)
            self.hidden = False
    ###################################################################################################
    def hideTheSignal(self):
        if(self.df is not None):
            self.plotCurve.setVisible(False)
            self.hidden = True
    ##################################################################################################
    def labelSignal_1(self): # TODO : not finished 
        if(self.df_1 is not None):
            self.signalName = self.titleEdit_1.text()
    ##################################################################################################
    
    def labelSignal_2(self): # TODO : not finished 
        if(self.df_2 is not None):
            self.signalName = self.titleEdit_2.text()
    ##################################################################################################
    def updateSpeed_1(self):
        """ Adjust the speed of the signal based on the slider value and update the label. """
        speed = self.speedSlider_1.value()
     
        # Adjust the timer interval based on the slider value
        self.timer.start(101 - speed)  # Reverse the speed so a higher slider value means faster updates
    #################################################################################################
    
    def updateSpeed_2(self):
        """ Adjust the speed of the signal based on the slider value and update the label. """
        speed = self.speedSlider_2.value()
     
        # Adjust the timer interval based on the slider value
        self.timer_2.start(101 - speed)  # Reverse the speed so a higher slider value means faster updates
    #################################################################################################
    
    def zoom_1(self):
        """ Zoom in on the plot by 10%."""
        if self.zoom_level < self.max_zoom_level:
            self.zoom_level += 10  # Increase zoom level by 10%
            self.plotWidget_1.getViewBox().scaleBy((0.9, 0.9))
    #################################################################################################
    
    def zoom_2(self):
        """ Zoom in on the plot by 10%."""
        if self.zoom_level_2 < self.max_zoom_level:
            self.zoom_level_2 += 10  # Increase zoom level by 10%
            self.plotWidget_2.getViewBox().scaleBy((0.9, 0.9))
    #################################################################################################
    def zoom_out_1(self):
        """ Zoom out of the plot by 10%. """
        if self.zoom_level > self.min_zoom_level:
            self.zoom_level -= 10  # Decrease zoom level by 10%
            self.plotWidget_1.getViewBox().scaleBy((1.1, 1.1))  # Scale the plot by 110%
    #################################################################################################
    def zoom_out_2(self):
        """ Zoom out of the plot by 10%. """
        if self.zoom_level_2 > self.min_zoom_level:
            self.zoom_level_2 -= 10  # Decrease zoom level by 10%
            self.plotWidget_2.getViewBox().scaleBy((1.1, 1.1))  # Scale the plot by 110%
    #################################################################################################
    def openNonRectGraph(self):
        self.hide()
        if self.non_rect_window is None:
            self.non_rect_window = Window(self)
        self.non_rect_window.show()
    #################################################################################################
    # Functions to update the view based on the scrollbar value
    def updateHorizontalScroll_1(self):
        offset = self.horizontalScrollBar_1.value()
        if(offset + 550 < self.maxPanningValue_1):
            self.plotWidget_1.setXRange(offset, offset + 650, padding=0)

    def updateHorizontalScroll_2(self):
        offset = self.horizontalScrollBar_2.value()
        if(offset + 550 < self.maxPanningValue_2):
            self.plotWidget_2.setXRange(offset, offset + 650, padding=0)

    def updateVerticalScroll_1(self):
        offset = self.verticalScrollBar_1.value()
        if(offset + 1 < 2):
            self.plotWidget_1.setYRange(offset, offset + 3, padding=0)
    
    def updateVerticalScroll_2(self):
        offset = self.verticalScrollBar_2.value()
        if(offset + 1 < 2):
            self.plotWidget_2.setYRange(offset, offset + 3, padding=0)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

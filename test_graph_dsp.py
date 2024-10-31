import sys
from dotenv import load_dotenv
import os
import requests
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QColorDialog, QApplication
from main_window import Ui_SignalViewer
import pyqtgraph as pg
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d, CubicSpline
from pathlib import Path
from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
from non_rectangular import Window



class GlueSignalsPopup(QtWidgets.QWidget):
    def __init__(self, plotNames, plotCurves, plotColors, mainObj):
        super().__init__()
        self.setWindowTitle("Gluing Two Signals")
        self.setGeometry(100, 100, 800, 600)

        self.plotCurves = plotCurves
        self.plotColors = plotColors
        self.mainObj = mainObj
        self.layout = QtWidgets.QVBoxLayout()
        self.alreadyGlued = False
        self.isClosed = False

        # Create the first PlotWidget
        self.plotWidget_1 = pg.PlotWidget()
        self.plotWidget_1.setTitle(plotNames[0])
        xData_1 = []
        yData_1 = []
        for plot in self.plotCurves[0]:
            tempList_1, tempList_2 = plot.getData()
            if tempList_1 is None or tempList_2 is None:
                continue
            for i in range(len(tempList_1)):
                xData_1.append(tempList_1[i])
                yData_1.append(tempList_2[i])
        self.plotWidget_1.setXRange(xData_1[0] - 20, xData_1[-1] + 20, padding=0)
        self.plotWidget_1.setYRange(min(yData_1) - 2, max(yData_1) + 2, padding=0)
        self.plotWidget_1.plotItem.getViewBox().setLimits(xMin=xData_1[0] - 20, xMax=xData_1[-1] + 20, yMin=min(yData_1) - 2, yMax=max(yData_1) + 2)
        self.layout.addWidget(self.plotWidget_1)

        # Plot the data for the first plot
        for plot in plotCurves[0]:
            self.plotWidget_1.addItem(plot)

        # Create LinearRegionItem for the first plot
        self.region_1 = pg.LinearRegionItem([xData_1[0], xData_1[0] + 150], movable=True)
        self.region_1.setBounds([int(xData_1[0] + 10), int(xData_1[-1] - 10)])
        self.plotWidget_1.addItem(self.region_1)

        # Create a label for the first region
        self.label_1 = QtWidgets.QLabel(f"Region 1: [{xData_1[0]}, {xData_1[0] + 150}]")
        self.layout.addWidget(self.label_1)

        # Connect the region's signal to a method
        self.region_1.sigRegionChanged.connect(self.updateRegion_1)

        # Create the second PlotWidget
        self.plotWidget_2 = pg.PlotWidget()
        self.plotWidget_2.setTitle(plotNames[1])
        xData_2 = []
        yData_2 = []
        for plot in self.plotCurves[1]:
            tempList_1, tempList_2 = plot.getData()
            if tempList_1 is None or tempList_2 is None:
                continue
            for i in range(len(tempList_1)):
                xData_2.append(tempList_1[i])
                yData_2.append(tempList_2[i])
        self.plotWidget_2.setXRange(xData_2[0] - 20, xData_2[-1] + 20, padding=0)
        self.plotWidget_2.setYRange(min(yData_2) - 2, max(yData_2) + 2, padding=0)
        self.plotWidget_2.plotItem.getViewBox().setLimits(xMin=xData_2[0] - 20, xMax=xData_2[-1] + 20, yMin=min(yData_2) - 2, yMax=max(yData_2) + 2)
        self.layout.addWidget(self.plotWidget_2)

        # Plot the data for the second plot
        for plot in plotCurves[1]:
            self.plotWidget_2.addItem(plot)

        # Create LinearRegionItem for the second plot
        self.region_2 = pg.LinearRegionItem([xData_2[0], xData_2[0] + 150], movable=True)
        self.region_2.setBounds([int(xData_2[0] + 10), int(xData_2[-1] - 10)])
        self.plotWidget_2.addItem(self.region_2)

        # Create a label for the second region
        self.label_2 = QtWidgets.QLabel(f'Region 2: [{xData_2[0]}, {xData_2[0] + 150}]')
        self.layout.addWidget(self.label_2)

        # Connect the region's signal to a method
        self.region_2.sigRegionChanged.connect(self.updateRegion_2)

        # Create radio buttons
        self.radio_nearest = QtWidgets.QRadioButton("Nearest")
        self.radio_quadratic = QtWidgets.QRadioButton("Quadratic")
        self.radio_cubic = QtWidgets.QRadioButton("Cubic")
        
        # Set default selection
        self.radio_nearest.setChecked(True)

        # Connect the toggled signal to the event handler
        self.radio_nearest.toggled.connect(self.updateResult)
        self.radio_quadratic.toggled.connect(self.updateResult)
        self.radio_cubic.toggled.connect(self.updateResult)

        # Create button group for radio buttons
        self.button_group = QtWidgets.QHBoxLayout()
        self.button_group.addWidget(self.radio_nearest)
        self.button_group.addWidget(self.radio_quadratic)
        self.button_group.addWidget(self.radio_cubic)

        # Add radio buttons to layout
        self.layout.addLayout(self.button_group)

        self.plotWidget_3 = pg.PlotWidget()
        self.plotWidget_3.setTitle("Result")
        self.layout.addWidget(self.plotWidget_3)
        
        # adding the "screenshot" button to the layout
        self.screenshotBtn = QtWidgets.QPushButton("screenshot")
        self.screenshotBtn.clicked.connect(self.takeScreenShot)
        self.screenshotBtn.setStyleSheet(u"QPushButton {\n"
        "	background-color: #5e80ad;\n"
        "\n"
        "   color: #d9dee8; /* Light text color */\n"
        "   font-size: 16px; /* Font size */\n"
        "   padding: 10px 20px; /* Padding around the text */\n"
        "	border-top-color: transparent;\n"
        "	border-right-color: transparent;\n"
        "	border-left-color: transparent;\n"
        "	border-bottom-color: transparent;\n"
        "	border-width: 1px;\n"
        "	border-style: solid;\n"
        "    border-radius: 5px; /* Rounded corners */\n"
        "    font-family: \"Segoe UI\", \"Helvetica Neue\", \"Arial\", sans-serif; /* Font family */\n"
        "}\n"
        "\n"
        "QPushButton:hover {\n"
        "	background-color: #89dcff;\n"
        "	color: #010100;\n"
        "    border: 3px solid #81A1C1; /* Border color on hover */\n"
        "\n"
        "    font-size: 16px; /* Font size */\n"
        "    padding: 10px 20px; /* Padding around the text */\n"
        "    border-radius: 5px; /* Rounded corners */\n"
        "    font-family: \"Segoe UI\", \"Helvetica Neue\", \"Arial\", sans-serif; /* Font family */\n"
        "}\n"
        "\n"
        "QPushButton:pressed {\n"
        "    background-color: #3B4252; /* Background color when pressed */\n"
        "    border: 2px solid #4C566A; /* Border color when pressed */\n"
        "}\n"
        "")
        self.layout.addWidget(self.screenshotBtn)

        
        # adding the "export pdf" button to the layout
        self.exportBtn = QtWidgets.QPushButton("export PDF")
        self.exportBtn.clicked.connect(self.exportPDF)
        self.exportBtn.setStyleSheet(u"QPushButton {\n"
        "	background-color: #5e80ad;\n"
        "\n"
        "   color: #d9dee8; /* Light text color */\n"
        "   font-size: 16px; /* Font size */\n"
        "   padding: 10px 20px; /* Padding around the text */\n"
        "	border-top-color: transparent;\n"
        "	border-right-color: transparent;\n"
        "	border-left-color: transparent;\n"
        "	border-bottom-color: transparent;\n"
        "	border-width: 1px;\n"
        "	border-style: solid;\n"
        "    border-radius: 5px; /* Rounded corners */\n"
        "    font-family: \"Segoe UI\", \"Helvetica Neue\", \"Arial\", sans-serif; /* Font family */\n"
        "}\n"
        "\n"
        "QPushButton:hover {\n"
        "	background-color: #89dcff;\n"
        "	color: #010100;\n"
        "    border: 3px solid #81A1C1; /* Border color on hover */\n"
        "\n"
        "    font-size: 16px; /* Font size */\n"
        "    padding: 10px 20px; /* Padding around the text */\n"
        "    border-radius: 5px; /* Rounded corners */\n"
        "    font-family: \"Segoe UI\", \"Helvetica Neue\", \"Arial\", sans-serif; /* Font family */\n"
        "}\n"
        "\n"
        "QPushButton:pressed {\n"
        "    background-color: #3B4252; /* Background color when pressed */\n"
        "    border: 2px solid #4C566A; /* Border color when pressed */\n"
        "}\n"
        "")
        self.layout.addWidget(self.exportBtn)
        self.isPdfCreated = False

        self.setLayout(self.layout)
        self.onGlue()

    def updateRegion_1(self):
        # Get the current range of region 1
        regionRange = self.region_1.getRegion()
        self.label_1.setText(f'Region 1: {regionRange}')
        self.onGlue()

    def updateRegion_2(self):
        # Get the current range of region 2
        regionRange = self.region_2.getRegion()
        self.label_2.setText(f'Region 2: {regionRange}')
        self.onGlue()

    def onGlue(self):
        # Get the x and y data from the plot item
        xData_1 = []
        yData_1 = []
        for plot in self.plotCurves[0]:
            tempList_1, tempList_2 = plot.getData()
            if tempList_1 is None or tempList_2 is None:
                continue
            for i in range(len(tempList_1)):
                xData_1.append(tempList_1[i])
                yData_1.append(tempList_2[i])
        
        xData_2 = []
        yData_2 = []
        for plot in self.plotCurves[1]:
            tempList_1, tempList_2 = plot.getData()
            if tempList_1 is None or tempList_2 is None:
                continue
            for i in range(len(tempList_1)):
                xData_2.append(tempList_1[i])
                yData_2.append(tempList_2[i])
        
        xData_1 = np.array(xData_1)
        yData_1 = np.array(yData_1)
        xData_2 = np.array(xData_2)
        yData_2 = np.array(yData_2)

        x1 = np.linspace(self.region_1.getRegion()[0], self.region_1.getRegion()[1], int(self.region_1.getRegion()[1] - self.region_1.getRegion()[0]))
        x2 = np.linspace(self.region_2.getRegion()[0], self.region_2.getRegion()[1], int(self.region_2.getRegion()[1] - self.region_2.getRegion()[0]))

        y1 = []
        y2 = []

        for x in x1:
            # Find the index of the closest x value
            index = (np.abs(xData_1 - x)).argmin()
            # Retrieve the corresponding y value
            y1.append(yData_1[index])

        self.firstSignalMean = np.mean(y1)
        self.firstSignalStdDeviation = np.std(y1)
                
        for x in x2:
            # Find the index of the closest x value
            index = (np.abs(xData_2 - x)).argmin()
            # Retrieve the corresponding y value
            y2.append(yData_2[index])
            
        self.secondSignalMean = np.mean(y2)
        self.secondSignalStdDeviation = np.std(y2)
        
        # Create interpolation functions
        LinearInterp_1 = interp1d(x1, y1, kind="nearest", fill_value="extrapolate")
        LinearInterp_2 = interp1d(x2, y2, kind="nearest", fill_value="extrapolate")
        QuadraticInterp_1 = interp1d(x1, y1, kind="quadratic", fill_value="extrapolate")
        QuadraticInterp_2 = interp1d(x2, y2, kind="quadratic", fill_value="extrapolate")
        CubicInterp_1 = CubicSpline(x1, y1)
        CubicInterp_2 = CubicSpline(x2, y2)

        # Interpolation for overlapping region (we will get the average value for each y in the overlapping region)
        self.x_overlap = []
        self.y_overlap = []
        # Initialize lists to hold non-overlapping points
        self.non_overlap_x1 = []
        self.non_overlap_y1 = []
        self.non_overlap_x2 = []
        self.non_overlap_y2 = []
        # If there is an overlapping part, its starting point will be the bigger starting index between the two ranges, while its end is the smaller ending
        self.x_overlap_start = max(x1[0], x2[0])
        self.x_overlap_end = min(x1[-1], x2[-1])

        if self.x_overlap_start < self.x_overlap_end:
            self.x_overlap = np.linspace(self.x_overlap_start, self.x_overlap_end, int(self.x_overlap_end - self.x_overlap_start))
            
            self.y_overlap = []
            for x in self.x_overlap:
                index1 = (np.abs(xData_1 - x)).argmin()
                index2 = (np.abs(xData_2 - x)).argmin()
                self.y_overlap.append((yData_1[index1] + yData_2[index2]) / 2)  # Average of both y values

            # Identify non-overlapping points for the first dataset
            for x, y in zip(x1, y1):
                if not (self.x_overlap_start <= x <= self.x_overlap_end):
                    self.non_overlap_x1.append(x)
                    self.non_overlap_y1.append(y)

            # Identify non-overlapping points for the second dataset
            for x, y in zip(x2, y2):
                if not (self.x_overlap_start <= x <= self.x_overlap_end):
                    self.non_overlap_x2.append(x)
                    self.non_overlap_y2.append(y)
            
            self.non_overlap_x1 = np.array(self.non_overlap_x1)
            self.non_overlap_y1 = np.array(self.non_overlap_y1)
            self.non_overlap_x2 = np.array(self.non_overlap_x2)
            self.non_overlap_y2 = np.array(self.non_overlap_y2)
        
        else:
            self.non_overlap_x1 = x1
            self.non_overlap_y1 = y1
            self.non_overlap_x2 = x2
            self.non_overlap_y2 = y2

        # Interpolation for the gap between the two ranges
        self.x_gap = []
        self.y_gap_linear = []
        self.y_gap_quadratic = []
        self.y_gap_cubic = []

        x_gap_start = x1[-1]
        x_gap_end = x2[0]
        if(x2[-1] <= x1[0]):
            x_gap_start = x2[-1]
            x_gap_end = x1[0]
    
        if x_gap_start < x_gap_end:
            self.x_gap = np.linspace(x_gap_start, x_gap_end, int(x_gap_end - x_gap_start))

            y_gap_linear_1 = LinearInterp_1(self.x_gap)
            y_gap_linear_2 = LinearInterp_2(self.x_gap)

            y_gap_quadratic_1 = QuadraticInterp_1(self.x_gap)
            y_gap_quadratic_2 = QuadraticInterp_2(self.x_gap)

            y_gap_cubic_1 = CubicInterp_1(self.x_gap)
            y_gap_cubic_2 = CubicInterp_2(self.x_gap)

            # Average the results or choose a method that suits your needs
            weights_1 = (x_gap_end - self.x_gap) / (x_gap_end - x_gap_start)
            weights_2 = (self.x_gap - x_gap_start) / (x_gap_end - x_gap_start)
            if(x_gap_start == x1[-1]):
                self.y_gap_linear = weights_1 * y_gap_linear_1 + weights_2 * y_gap_linear_2
                self.y_gap_quadratic = weights_1 * y_gap_quadratic_1 + weights_2 * y_gap_quadratic_2
                self.y_gap_cubic = weights_1 * y_gap_cubic_1 + weights_2 * y_gap_cubic_2
            else:
                self.y_gap_linear = weights_2 * y_gap_linear_1 + weights_1 * y_gap_linear_2
                self.y_gap_quadratic = weights_2 * y_gap_quadratic_1 + weights_1 * y_gap_quadratic_2
                self.y_gap_cubic = weights_2 * y_gap_cubic_1 + weights_1 * y_gap_cubic_2

        self.x_combined = []
        self.y_combined_linear = []
        self.y_combined_quadratic = []
        self.y_combined_cubic = []
        if(x1[0] <= x2[0]):
            self.x_combined = np.concatenate((self.non_overlap_x1, self.x_overlap, self.x_gap, self.non_overlap_x2))
            self.y_combined_linear = np.concatenate((self.non_overlap_y1, self.y_overlap, self.y_gap_linear, self.non_overlap_y2))
            self.y_combined_quadratic = np.concatenate((self.non_overlap_y1, self.y_overlap, self.y_gap_quadratic, self.non_overlap_y2))
            self.y_combined_cubic = np.concatenate((self.non_overlap_y1, self.y_overlap, self.y_gap_cubic, self.non_overlap_y2))
        else:
            self.x_combined = np.concatenate((self.non_overlap_x2, self.x_overlap, self.x_gap, self.non_overlap_x1))
            self.y_combined_linear = np.concatenate((self.non_overlap_y2, self.y_overlap, self.y_gap_linear, self.non_overlap_y1))
            self.y_combined_quadratic = np.concatenate((self.non_overlap_y2, self.y_overlap, self.y_gap_quadratic, self.non_overlap_y1))
            self.y_combined_cubic = np.concatenate((self.non_overlap_y2, self.y_overlap, self.y_gap_cubic, self.non_overlap_y1))

        self.alreadyGlued = True
        self.updateResult()
    
    def updateResult(self):
        if self.alreadyGlued:
            self.plotWidget_3.plotItem.clear()
            self.plotWidget_3.setXRange(self.x_combined[0] - 50, self.x_combined[-1] + 50, padding=0)

            if(self.radio_nearest.isChecked()):
                self.plotWidget_3.setYRange(min(self.y_combined_linear) - 5, max(self.y_combined_linear) + 5, padding=0)
                self.plotWidget_3.plotItem.getViewBox().setLimits(xMin=self.x_combined[0] - 50, xMax=self.x_combined[-1] + 50, 
                                                                yMin=min(self.y_combined_linear) - 5, yMax=max(self.y_combined_linear) + 5)
                self.plotWidget_3.plot(self.non_overlap_x1, self.non_overlap_y1, pen=self.plotColors[0])
                self.plotWidget_3.plot(self.non_overlap_x2, self.non_overlap_y2, pen=self.plotColors[1])
                self.plotWidget_3.plot(self.x_overlap, self.y_overlap, pen='y')
                self.plotWidget_3.plot(self.x_gap, self.y_gap_linear, pen='y')

                self.glueMean = np.mean(self.y_combined_linear)
                self.glueStdDeviation = np.std(self.y_combined_linear)

            elif(self.radio_quadratic.isChecked()):
                self.plotWidget_3.setYRange(min(self.y_combined_quadratic) - 5, max(self.y_combined_quadratic) + 5, padding=0)
                self.plotWidget_3.plotItem.getViewBox().setLimits(xMin=self.x_combined[0] - 50, xMax=self.x_combined[-1] + 50, 
                                                                yMin=min(self.y_combined_quadratic) - 5, yMax=max(self.y_combined_quadratic) + 5)
                self.plotWidget_3.plot(self.non_overlap_x1, self.non_overlap_y1, pen=self.plotColors[0])
                self.plotWidget_3.plot(self.non_overlap_x2, self.non_overlap_y2, pen=self.plotColors[1])
                self.plotWidget_3.plot(self.x_overlap, self.y_overlap, pen='y')
                self.plotWidget_3.plot(self.x_gap, self.y_gap_quadratic, pen='y')

                self.glueMean = np.mean(self.y_combined_quadratic)
                self.glueStdDeviation = np.std(self.y_combined_quadratic)

            elif(self.radio_cubic.isChecked()):
                self.plotWidget_3.setYRange(min(self.y_combined_cubic) - 5, max(self.y_combined_cubic) + 5, padding=0)
                self.plotWidget_3.plotItem.getViewBox().setLimits(xMin=self.x_combined[0] - 50, xMax=self.x_combined[-1] + 50, 
                                                                yMin=min(self.y_combined_cubic) - 5, yMax=max(self.y_combined_cubic) + 5)
                
                self.plotWidget_3.plot(self.non_overlap_x1, self.non_overlap_y1, pen=self.plotColors[0])
                self.plotWidget_3.plot(self.non_overlap_x2, self.non_overlap_y2, pen=self.plotColors[1])
                self.plotWidget_3.plot(self.x_overlap, self.y_overlap, pen='y')
                self.plotWidget_3.plot(self.x_gap, self.y_gap_cubic, pen='y')

                self.glueMean = np.mean(self.y_combined_cubic)
                self.glueStdDeviation = np.std(self.y_combined_cubic)
    
    # taking screenshot method ///////////////////////////////////////////////////
    
    def takeScreenShot(self):
        if self.isPdfCreated == False:
            self.pdf_filename = "signals_photos.pdf"
            self.pdf_file = canvas.Canvas(self.pdf_filename, pagesize= pagesizes.A4)
            self.isPdfCreated = True
            self.pdf_page_width, self.pdf_page_height = pagesizes.A4
            self.margin = 40  # left space between each screenshot
            self.start_y = self.pdf_page_height - self.margin   # starting y position in the page
            self.current_y = self.start_y  # intializing y to be at the starting y position and it will keep being updated as long as we add content to the page
            self.pdf_file.setFont("Times-Roman", 20)      # Change font to Times-Roman
            self.pdf_file.setFillColor(colors.black)        # Change color to black
            self.pdf_file.drawString(130, self.current_y, " Gluing signals screenshots and statistics")
            self.current_y-= self.margin
        else:
            self.pdf_file.showPage() # adding a new page in the pdf for every time we take a screenshot
            self.current_y = self.start_y  # adjusting current y position to be at the start of the new page
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")    # used to make each screensht have a unique name
        screenshot_1_filename = f'screenshot1_{timestamp}.png'    
        self.screenshot_1 = self.plotWidget_1.grab()
        self.screenshot_1.save(screenshot_1_filename, 'PNG')
        screenshot_2_filename = f'screenshot2_{timestamp}.png'
        self.screenshot_2 = self.plotWidget_2.grab()
        self.screenshot_2.save(screenshot_2_filename, 'PNG')
        screenshot_3_filename = f'screenshot3_{timestamp}.png'  
        self.screenshot_3 = self.plotWidget_3.grab()
        self.screenshot_3.save(screenshot_3_filename, 'PNG')
        
        if self.current_y - 200 <=  self.margin:  # checks if there is not enough space in the page to add a screenshot of height 200, it creates a new page.
            self.pdf_file.showPage()  # Create a new page if needed
            self.current_y = self.start_y  # Reset y position for the new page
        
        self.pdf_file.drawImage(screenshot_1_filename, x = 30, y = self.current_y - 200, width = 350, height = 200 )
        self.pdf_file.setFont("Helvetica-Bold", 12)  # Set bold font
        self.pdf_file.setFillColor(colors.red)        # Set text color to red    
        self.pdf_file.drawString(400, self.current_y - 40, "First Signal Analysis Results:")
        
        self.pdf_file.setFont("Times-Roman", 12)      # Change font to Times-Roman
        self.pdf_file.setFillColor(colors.black)        # Change color to black
        self.pdf_file.drawString(400, self.current_y - 80, f"Mean: {self.firstSignalMean:.2f}")
        self.pdf_file.drawString(400, self.current_y - 110, f"Standard Deviation: {self.firstSignalStdDeviation:.2f}")
        self.current_y -= (self.margin + 200)
        
        if self.current_y - 200 <=  self.margin:
            self.pdf_file.showPage()  # Create a new page if needed
            self.current_y = self.start_y  # Reset y position for the new page
            
        self.pdf_file.drawImage(screenshot_2_filename, x = 30, y = self.current_y - 200, width = 350, height = 200 )
        self.pdf_file.setFont("Helvetica-Bold", 12)  # Set bold font
        self.pdf_file.setFillColor(colors.red)        # Set text color to red
        self.pdf_file.drawString(400, self.current_y - 40, "Second Signal Analysis Results:")
        
        self.pdf_file.setFont("Times-Roman", 12)      # Change font to Times-Roman
        self.pdf_file.setFillColor(colors.black)        # Change color to black
        self.pdf_file.drawString(400, self.current_y - 80, f"Mean: {self.secondSignalMean:.2f}")
        self.pdf_file.drawString(400, self.current_y - 110, f"Standard Deviation: {self.secondSignalStdDeviation:.2f}")
        self.current_y -= (self.margin + 200)
        
        if self.current_y - 200 <=  self.margin:
            self.pdf_file.showPage()  # Create a new page if needed
            self.current_y = self.start_y  # Reset y position for the new page

        self.pdf_file.drawImage(screenshot_3_filename, x = 30, y = self.current_y - 200, width = 350, height = 200 )
        self.pdf_file.setFont("Helvetica-Bold", 12)  # Set bold font
        self.pdf_file.setFillColor(colors.red)        # Set text color to red
        self.pdf_file.drawString(400, self.current_y - 40, "Glued Signal Analysis Results:")
        
        self.pdf_file.setFont("Times-Roman", 12)      # Change font to Times-Roman
        self.pdf_file.setFillColor(colors.black)        # Change color to black
        self.pdf_file.drawString(400, self.current_y - 80, f"Mean: {self.glueMean:.2f}")
        self.pdf_file.drawString(400, self.current_y - 110, f"Standard Deviation: {self.glueStdDeviation:.2f}")
        self.current_y -= (self.margin + 200)

        # deleting image files after adding them
        os.remove(screenshot_1_filename) 
        os.remove(screenshot_2_filename)
        os.remove(screenshot_3_filename)

        
    
    # exporting the pdf method ///////////////////////////////////////////////////
    def exportPDF(self):
        
        if self.pdf_file:
            self.pdf_file.save()
            os.startfile(self.pdf_filename)
            print(f"Results exported to {self.pdf_filename}")
            self.isPdfCreated = False # to start a new pdf the next time we take a screenshot after exporting this one.
    
    def closeEvent(self, event):
        self.isClosed = True
        self.mainObj.graphSelectBox.setCurrentIndex(0)
        self.mainObj.startTheSignal()
        self.mainObj.graphSelectBox.setCurrentIndex(1)
        self.mainObj.startTheSignal()
        event.accept()  # Accept the close event to close the widget
            

class LiveSignalPopup(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Temperature In Cairo")
        self.setGeometry(100, 100, 800, 600)

        self.plotWidget = pg.PlotWidget()
        self.plotWidget.setTitle("Temperature In Cairo")
        self.plotWidget.setLabel('left', 'Temperature (Kelvin)')
        self.plotWidget.setLabel('bottom', 'Time (s)')

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.plotWidget)
        self.setLayout(layout)

        # Create a button and add it to the layout
        self.isPaused = False

        horizontalLayout = QtWidgets.QHBoxLayout()

        self.resumeButton = QtWidgets.QPushButton("Resume")
        self.resumeButton.clicked.connect(self.onResume)
        self.resumeButton.setStyleSheet(u"QPushButton {\n"
        "	background-color: #5e80ad;\n"
        "\n"
        "   color: #d9dee8; /* Light text color */\n"
        "   font-size: 16px; /* Font size */\n"
        "   padding: 10px 20px; /* Padding around the text */\n"
        "	border-top-color: transparent;\n"
        "	border-right-color: transparent;\n"
        "	border-left-color: transparent;\n"
        "	border-bottom-color: transparent;\n"
        "	border-width: 1px;\n"
        "	border-style: solid;\n"
        "    border-radius: 5px; /* Rounded corners */\n"
        "    font-family: \"Segoe UI\", \"Helvetica Neue\", \"Arial\", sans-serif; /* Font family */\n"
        "}\n"
        "\n"
        "QPushButton:hover {\n"
        "	background-color: #89dcff;\n"
        "	color: #010100;\n"
        "    border: 3px solid #81A1C1; /* Border color on hover */\n"
        "\n"
        "    font-size: 16px; /* Font size */\n"
        "    padding: 10px 20px; /* Padding around the text */\n"
        "    border-radius: 5px; /* Rounded corners */\n"
        "    font-family: \"Segoe UI\", \"Helvetica Neue\", \"Arial\", sans-serif; /* Font family */\n"
        "}\n"
        "\n"
        "QPushButton:pressed {\n"
        "    background-color: #3B4252; /* Background color when pressed */\n"
        "    border: 2px solid #4C566A; /* Border color when pressed */\n"
        "}\n"
        "")

        self.pauseButton = QtWidgets.QPushButton("Pause")
        self.pauseButton.clicked.connect(self.onPause)
        self.pauseButton.setStyleSheet(u"QPushButton {\n"
        "	background-color: #5e80ad;\n"
        "\n"
        "   color: #d9dee8; /* Light text color */\n"
        "   font-size: 16px; /* Font size */\n"
        "   padding: 10px 20px; /* Padding around the text */\n"
        "	border-top-color: transparent;\n"
        "	border-right-color: transparent;\n"
        "	border-left-color: transparent;\n"
        "	border-bottom-color: transparent;\n"
        "	border-width: 1px;\n"
        "	border-style: solid;\n"
        "    border-radius: 5px; /* Rounded corners */\n"
        "    font-family: \"Segoe UI\", \"Helvetica Neue\", \"Arial\", sans-serif; /* Font family */\n"
        "}\n"
        "\n"
        "QPushButton:hover {\n"
        "	background-color: #89dcff;\n"
        "	color: #010100;\n"
        "    border: 3px solid #81A1C1; /* Border color on hover */\n"
        "\n"
        "    font-size: 16px; /* Font size */\n"
        "    padding: 10px 20px; /* Padding around the text */\n"
        "    border-radius: 5px; /* Rounded corners */\n"
        "    font-family: \"Segoe UI\", \"Helvetica Neue\", \"Arial\", sans-serif; /* Font family */\n"
        "}\n"
        "\n"
        "QPushButton:pressed {\n"
        "    background-color: #3B4252; /* Background color when pressed */\n"
        "    border: 2px solid #4C566A; /* Border color when pressed */\n"
        "}\n"
        "")

        horizontalLayout.addWidget(self.pauseButton)
        horizontalLayout.addWidget(self.resumeButton)
        layout.addLayout(horizontalLayout)

        self.temperatures = []
        self.timePoints = []

        # Needed For Boundaries Of The Plot
        self.minTemp = 999999999
        self.maxTemp = -99999999

    def updatePlot(self, temperature):
        # Update the data lists
        if(temperature < self.minTemp):
            self.minTemp = temperature
        
        if(temperature > self.maxTemp):
            self.maxTemp = temperature

        self.temperatures.append(temperature)
        self.timePoints.append(len(self.temperatures))

        # Update the plot
        self.plotWidget.clear()
        self.plotWidget.setXRange(0, self.timePoints[-1] + 3, padding=0)
        self.plotWidget.setYRange(self.minTemp - 20, self.maxTemp + 20, padding=0)
        self.plotWidget.plotItem.getViewBox().setLimits(xMin=0, xMax=self.timePoints[-1] + 3, yMin=self.minTemp - 20, yMax=self.maxTemp + 20)
        self.plotWidget.plot(self.timePoints, self.temperatures, pen='r')
    
    def onPause(self):
        self.isPaused = True
    
    def onResume(self):
        self.isPaused = False

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
        formattedColor = ""
        if isinstance(color, QtGui.QPen):
            formattedColor = f"#{color.color().red():02X}{color.color().green():02X}{color.color().blue():02X}" 
        else:
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
                self.graphObj.colorMoveBox_1.setItemText(self.index + 1, new_text)
            else:
                self.graphObj.signalNames_2[self.index] = new_text
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

class MainWindow(Ui_SignalViewer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        load_dotenv()
        # Coordinates of cairo found by gecoding api provided by openweather map
        self.lat=30.0443879
        self.lon=31.2357257
        self.API_KEY = os.getenv('API_KEY')
        self.URL = f'https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.API_KEY}'
        self.liveSignal = LiveSignalPopup()
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
        self.minY_1 = 0
        self.maxY_1 = 0
        self.minY_2 = 0
        self.maxY_2 = 0
        
        self.hidden = False
        self.zoom_level = 0  # Default zoom level
        self.zoom_level_2 = 0
        self.min_zoom_level = 0
        self.max_zoom_level = 100  # Maximum zoom level
        self.nonRectGraphButton.clicked.connect(self.openNonRectGraph)
        # Applying button functionalities for first graph #############################
        self.addFileButton.clicked.connect(self.browseTheSignal)
        self.connectOnlineButton.clicked.connect(self.openLiveSignal)
        self.glueButton.clicked.connect(self.glueSignals)

        # Applying button functionalities for first graph
        self.startButton_1.clicked.connect(self.startTheSignal)
        self.timer.timeout.connect(self.updatePlot_1)
        self.stopButton_1.clicked.connect(self.pauseTheSignal)
        self.rewindButton_1.clicked.connect(self.rewindTheSignal)
        self.moveButton_1.clicked.connect(self.moveTheSignal_1)
        
        # Applying button functionalities for second graph
        self.speedSlider_1.valueChanged.connect(self.updateSpeed_1)
        self.colorButton_1.clicked.connect(self.colorTheSignal_1)
        self.zoomInButton_1.clicked.connect(self.zoom_1)
        self.zoomOutButton_1.clicked.connect(self.zoom_out_1)

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

        self.plotWidget_1.plotItem.getViewBox().sigRangeChanged.connect(self.syncViewBoxes_1)
        self.plotWidget_2.plotItem.getViewBox().sigRangeChanged.connect(self.syncViewBoxes_2)

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
                self.plotCurves_1.append([self.plotWidget_1.plotItem.plot()])
                self.plotColors_1.append(currColor)
                self.hidden_1.append(False)
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
                self.plotCurves_2.append([self.plotWidget_1.plotItem.plot()])
                self.plotColors_2.append(currColor)
                self.hidden_2.append(False)
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
                    self.maxPanningValue_1 = max(self.current_index + self.chunk_size, self.maxPanningValue_1)
                    self.minY_1 = min(min(self.browsedData_y), self.minY_1)
                    self.maxY_1 = max(max(self.browsedData_y), self.maxY_1)
                    self.plotWidget_1.plotItem.setXRange(self.current_index, self.current_index + self.chunk_size , padding=0)  # Set initial x-axis range
                    self.plotWidget_1.plotItem.setYRange(self.minY_1 - 2, self.maxY_1 + 2, padding = 0)
                    self.plotWidget_1.plotItem.getViewBox().setLimits(xMin=0, xMax=self.maxPanningValue_1 + 50, yMin=self.minY_1 - 2, yMax=self.maxY_1 + 2)
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
                    self.maxPanningValue_2 = max(self.current_index_2 + self.chunk_size, self.maxPanningValue_2)
                    self.minY_2 = min(min(self.browsedData_y_2), self.minY_2)
                    self.maxY_2 = max(max(self.browsedData_y_2), self.maxY_2)
                    self.plotWidget_2.plotItem.setXRange(self.current_index_2, self.current_index_2 + self.chunk_size , padding=0)  # Set initial x-axis range
                    self.plotWidget_2.plotItem.setYRange(self.minY_2 - 2, self.maxY_2 + 2, padding = 0)
                    self.plotWidget_2.plotItem.getViewBox().setLimits(xMin=0, xMax=self.maxPanningValue_2 + 50, yMin=self.minY_2 - 2, yMax=self.maxY_2 + 2)
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
                    self.maxPanningValue_1 = max(self.current_index + self.chunk_size, self.maxPanningValue_1)
                    self.minY_1 = min(min(self.browsedData_y), self.minY_1)
                    self.maxY_1 = max(max(self.browsedData_y), self.maxY_1)
                    self.plotWidget_1.plotItem.setXRange(self.current_index, self.current_index + self.chunk_size , padding=0)  # Set initial x-axis range
                    self.plotWidget_1.plotItem.setYRange(self.minY_1 - 2, self.maxY_1 + 2, padding = 0)
                    self.plotWidget_1.plotItem.getViewBox().setLimits(xMin=0, xMax=self.maxPanningValue_1 + 50, yMin=self.minY_1 - 2, yMax=self.maxY_1 + 2)
                if self.df_2 is not None and not self.df_2.empty:  # if dataframe of first graph contains data:
                    if not len(self.browsedData_y_2) and not self.isPaused_2:
                        self.browsedData_y_2 = self.df_2.to_numpy().flatten()
                        self.pastSignalsY_2.append(self.browsedData_y_2)
                        data_x_2 = np.arange(len(self.browsedData_y_2))
                        self.data_x_2 = data_x_2
                        self.pastSignalsX_2.append(self.data_x_2)           
                        self.maxPanningValue_2 = max(self.current_index_2 + self.chunk_size, self.maxPanningValue_2)
                        self.minY_2 = min(min(self.browsedData_y_2), self.minY_2)
                        self.maxY_2 = max(max(self.browsedData_y_2), self.maxY_2)
                        self.plotWidget_2.plotItem.setXRange(self.current_index_2, self.current_index_2 + self.chunk_size , padding=0)  # Set initial x-axis range
                        self.plotWidget_2.plotItem.setYRange(self.minY_2 - 2, self.maxY_2 + 2, padding = 0)   
                        self.plotWidget_2.plotItem.getViewBox().setLimits(xMin=0, xMax=self.maxPanningValue_2 + 50, yMin=self.minY_2 - 2, yMax=self.maxY_2 + 2)
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
            #self.plotWidget_1.clear() # Clear the graph first so that the widget only contains the latest plots (needed for show and hide functionality)

            for signalIdx in range (len(self.pastSignalsY_1)):  # Plotting all stored signals on the graph
                if not self.hidden_1[signalIdx]:
                    segment_x = self.pastSignalsX_1[signalIdx][self.current_index:end_index]
                    segment_y = self.pastSignalsY_1[signalIdx][self.current_index:end_index]
                    self.plotCurves_1[signalIdx].append(self.plotWidget_1.plot(
                        segment_x, segment_y, pen=self.plotColors_1[signalIdx], clear=False, name=self.signalNames_1[signalIdx]
                        ))
            
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
             
        self.plotWidget_1.plotItem.getViewBox().setLimits(xMin=0, xMax=self.maxPanningValue_1 + 50, yMin=self.minY_1 - 2, yMax=self.maxY_1 + 2)
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
            #self.plotWidget_2.clear()
            
            for signalIdx in range (len(self.pastSignalsY_2)):  # plotting all stored signals on the graph
                if not self.hidden_2[signalIdx]:
                    segment_x = self.pastSignalsX_2[signalIdx][self.current_index_2:end_index_2]
                    segment_y = self.pastSignalsY_2[signalIdx][self.current_index_2:end_index_2]
                    self.plotCurves_2[signalIdx].append(self.plotWidget_2.plot(
                        segment_x, segment_y, pen=self.plotColors_2[signalIdx], clear=False, name=self.signalNames_2[signalIdx]
                        ))
            
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
        
        self.plotWidget_2.plotItem.getViewBox().setLimits(xMin=0, xMax=self.maxPanningValue_2 + 50, yMin=self.minY_2 - 2, yMax=self.maxY_2 + 2)
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
    
    def openLiveSignal(self):
        self.liveTimer = QtCore.QTimer()
        self.liveTimer.timeout.connect(self.fetchLiveData)
        self.liveTimer.start(3000) # Every 3 Seconds we fetch from the API
        self.fetchLiveData() # Initial Fetch
        self.liveSignal.show()
    
    def fetchLiveData(self):
        if not self.liveSignal.isPaused:
            try:
                response = requests.get(self.URL)
                data = response.json()
                temperature = data['main']['temp']
                self.liveSignal.updatePlot(temperature)
            except Exception as e:
                print(f"Error fetching data: {e}")
    
    def glueSignals(self):
        firstSignalIdx = self.colorMoveBox_1.currentIndex() - 1
        secondSignalIdx = self.colorMoveBox_2.currentIndex() - 1
        
        if(firstSignalIdx > -1 and secondSignalIdx > -1):
            self.glueSignal = GlueSignalsPopup([self.signalNames_1[firstSignalIdx], self.signalNames_2[secondSignalIdx]], 
                                               [self.plotCurves_1[firstSignalIdx], self.plotCurves_2[secondSignalIdx]],
                                               [self.plotColors_1[firstSignalIdx], self.plotColors_2[secondSignalIdx]],
                                               self
                                               )
            self.glueSignal.show()
            
    def linkGraphs(self):
        if self.isLinked == True:
            self.isLinked = False
            self.linkButton.setText("Link")
        else:
            self.isLinked = True
            self.linkButton.setText("Unlink")
            self.zoom_level = 0  # Default zoom level
            self.zoom_level_2 = 0
            self.speedSlider_1.setValue(0)
            self.speedSlider_2.setValue(0)
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
            for plot in self.plotCurves_1[index]:
                plot.setVisible(True)

    def hideTheSignal_1(self, index):
        if(self.df_1 is not None):
            self.hidden_1[index] = True
            for plot in self.plotCurves_1[index]:
                plot.setVisible(False)
    
    def showTheSignal_2(self, index):
        if(self.df_2 is not None):
            self.hidden_2[index] = False
            for plot in self.plotCurves_2[index]:
                plot.setVisible(True)

    def hideTheSignal_2(self, index):
        if(self.df_2 is not None):
            self.hidden_2[index] = True
            for plot in self.plotCurves_2[index]:
                plot.setVisible(False)

    def colorTheSignal_1(self):
        if(self.df_1 is not None):
            color = QColorDialog.getColor()
            if color.isValid():
                currIdx = self.colorMoveBox_1.currentIndex() - 1
                currColor = pg.mkPen(color.name())
                if currIdx == -1:
                    for i in range(len(self.plotColors_1)):
                        self.plotColors_1[i] = currColor
                        for plot in self.plotCurves_1[i]:
                            plot.setPen(currColor)
                        self.labelItems_1[i].setCheckboxColor((color.red(), color.green(), color.blue()))
                else:
                    self.plotColors_1[currIdx] = currColor
                    for plot in self.plotCurves_1[currIdx]:
                        plot.setPen(currColor)
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
                        for plot in self.plotCurves_2[i]:
                            plot.setPen(currColor)
                        self.labelItems_2[i].setCheckboxColor((color.red(), color.green(), color.blue()))
                else:
                    self.plotColors_2[currIdx] = currColor
                    for plot in self.plotCurves_2[currIdx]:
                        plot.setPen(currColor)
                    self.labelItems_2[currIdx].setCheckboxColor((color.red(), color.green(), color.blue()))

    def moveTheSignal_1(self):
        if(self.df_1 is not None):
            self.graphSelectBox.setCurrentIndex(1) # Needed so that when we call start the signal later in the function it starts the second graph
            currIdx = self.colorMoveBox_1.currentIndex() - 1
            if(currIdx == -1):
                for signalIdx in range(len(self.pastSignalsY_1)):
                    self.signalNames_2.append(self.signalNames_1[signalIdx])
                    self.plotCurves_2.append([self.plotWidget_2.plotItem.plot()])
                    self.plotColors_2.append(self.plotColors_1[signalIdx])
                    self.hidden_2.append(self.hidden_1[signalIdx])
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
                self.colorMoveBox_1.clear()
                self.colorMoveBox_1.addItem("All Channels")

            else:
                self.signalNames_2.append(self.signalNames_1[currIdx])
                self.plotCurves_2.append([self.plotWidget_2.plotItem.plot()])
                self.plotColors_2.append(self.plotColors_1[currIdx])
                self.hidden_2.append(self.hidden_1[currIdx])
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

                for plot in self.plotCurves_1[currIdx]:
                    self.plotWidget_1.plotItem.removeItem(plot)
                self.listChannelsWidget_1.takeItem(currIdx)
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
                    self.plotCurves_1.append([self.plotWidget_1.plotItem.plot()])
                    self.plotColors_1.append(self.plotColors_2[signalIdx])
                    self.hidden_1.append(self.hidden_2[signalIdx])
                    self.colorMoveBox_1.addItem(self.signalNames_2[signalIdx])

                    self.filePaths_1.append(self.filePaths_2[signalIdx])
                    self.df_1 = pd.read_csv(self.filePaths_2[signalIdx], header=None)
                    self.browsedData_y = [] 
                    self.isPaused = False
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
                self.colorMoveBox_2.clear()
                self.colorMoveBox_2.addItem("All Channels")

            else:
                self.signalNames_1.append(self.signalNames_2[currIdx])
                self.plotCurves_1.append([self.plotWidget_1.plotItem.plot()])
                self.plotColors_1.append(self.plotColors_2[currIdx])
                self.hidden_1.append(self.hidden_2[currIdx])
                self.colorMoveBox_1.addItem(self.signalNames_2[currIdx])

                self.filePaths_1.append(self.filePaths_2[currIdx])
                self.df_1 = pd.read_csv(self.filePaths_2[currIdx], header=None)
                self.browsedData_y = [] 
                self.isPaused = False
                self.current_index = 0

                # Adding Signal Name To Our Labels List
                labelItem = CheckableLabelItem(len(self.labelItems_1), self.signalNames_1[-1], self.plotColors_1[-1], self, 1)
                self.labelItems_1.append(labelItem)
                listWidgetItem = QtWidgets.QListWidgetItem()
                listWidgetItem.setSizeHint(labelItem.sizeHint())  # Set the size hint
                self.listChannelsWidget_1.addItem(listWidgetItem)
                self.listChannelsWidget_1.setItemWidget(listWidgetItem, labelItem)  # Set the widget
                self.widgetItems_1.append(listWidgetItem)

                for plot in self.plotCurves_2[currIdx]:
                    self.plotWidget_2.plotItem.removeItem(plot)
                self.listChannelsWidget_2.takeItem(currIdx)
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
    
    def updateSpeed_1(self):
        """ Adjust the speed of the signal based on the slider value and update the label. """
        speed = self.speedSlider_1.value()
        if(self.isLinked):
            self.speedSlider_2.setValue(speed)
            self.timer_2.start(101 - speed)
        # Adjust the timer interval based on the slider value
        self.timer.start(101 - speed)  # Reverse the speed so a higher slider value means faster etes
    #################################################################################################
    
    def updateSpeed_2(self):
        """ Adjust the speed of the signal based on the slider value and update the label. """
        speed = self.speedSlider_2.value()
        if(self.isLinked):
            self.speedSlider_1.setValue(speed)
            self.timer.start(101 - speed)
     
        # Adjust the timer interval based on the slider value
        self.timer_2.start(101 - speed)  # Reverse the speed so a higher slider value means faster updates
    #################################################################################################
    
    def zoom_1(self):
        """ Zoom in on the plot by 10%."""
        if self.zoom_level < self.max_zoom_level:
            self.zoom_level += 10  # Increase zoom level by 10%
            if(self.isLinked):
                self.zoom_level_2 = self.zoom_level
                self.plotWidget_2.getViewBox().scaleBy((0.9, 0.9))
            self.plotWidget_1.getViewBox().scaleBy((0.9, 0.9))
    #################################################################################################
    
    def zoom_2(self):
        """ Zoom in on the plot by 10%."""
        if self.zoom_level_2 < self.max_zoom_level:
            self.zoom_level_2 += 10  # Increase zoom level by 10%
            if(self.isLinked):
                self.zoom_level = self.zoom_level_2
                self.plotWidget_1.getViewBox().scaleBy((0.9, 0.9))
            self.plotWidget_2.getViewBox().scaleBy((0.9, 0.9))
    #################################################################################################
    def zoom_out_1(self):
        """ Zoom out of the plot by 10%. """
        if self.zoom_level > self.min_zoom_level:
            self.zoom_level -= 10  # Decrease zoom level by 10%
            if(self.isLinked):
                self.zoom_level_2 = self.zoom_level
                self.plotWidget_2.getViewBox().scaleBy((1.1, 1.1))
            self.plotWidget_1.getViewBox().scaleBy((1.1, 1.1))  # Scale the plot by 110%
    #################################################################################################
    def zoom_out_2(self):
        """ Zoom out of the plot by 10%. """
        if self.zoom_level_2 > self.min_zoom_level:
            self.zoom_level_2 -= 10  # Decrease zoom level by 10%
            if(self.isLinked):
                self.zoom_level = self.zoom_level_2
                self.plotWidget_1.getViewBox().scaleBy((1.1, 1.1))
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
    
    def syncViewBoxes_1(self):
        if(self.isLinked):
            self.plotWidget_2.plotItem.getViewBox().setXRange(*self.plotWidget_1.plotItem.getViewBox().viewRange()[0], padding=0) # * allows us to convert tuple
            self.plotWidget_2.plotItem.getViewBox().setYRange(*self.plotWidget_1.plotItem.getViewBox().viewRange()[1], padding=0)
    
    def syncViewBoxes_2(self):
        if(self.isLinked):
            self.plotWidget_1.plotItem.getViewBox().setXRange(*self.plotWidget_2.plotItem.getViewBox().viewRange()[0], padding=0)
            self.plotWidget_1.plotItem.getViewBox().setYRange(*self.plotWidget_2.plotItem.getViewBox().viewRange()[1], padding=0)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
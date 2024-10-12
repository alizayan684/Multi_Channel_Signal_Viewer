import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg

class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        
        # Create the central widget and set it as the central widget of MainWindow
        self.centralWidget = QtWidgets.QWidget(parent = MainWindow)
        MainWindow.setCentralWidget(self.centralWidget)
        
        # Create a vertical layout for the central widget
        self.layout1 = QtWidgets.QVBoxLayout(self.centralWidget)
        
        # Create the PlotWidget and add it to the layout
        self.graphWidget = pg.PlotWidget(parent=self.centralWidget)
        self.graphWidget.setObjectName("graphWidget")
        self.layout1.addWidget(self.graphWidget)
        
        # Create a horizontal layout for the buttons
        self.buttonLayout = QtWidgets.QHBoxLayout()
        
        # Create buttons and add them to the button layout
        self.browseBtn = QtWidgets.QPushButton("browse", parent=self.centralWidget)
        self.browseBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.startBtn = QtWidgets.QPushButton("start", parent=self.centralWidget)
        self.startBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pauseBtn = QtWidgets.QPushButton("pause", parent=self.centralWidget)
        self.pauseBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.rewindBtn = QtWidgets.QPushButton("rewind", parent=self.centralWidget)
        self.rewindBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        
        self.linkBtn = QtWidgets.QPushButton("link", parent = self.centralWidget)
        self.linkBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        
        # Add the buttons to the button layout
        self.buttonLayout.addWidget(self.startBtn)
        self.buttonLayout.addWidget(self.pauseBtn)
        self.buttonLayout.addWidget(self.rewindBtn)
        self.buttonLayout.addWidget(self.browseBtn)
        
        self.buttonLayout.addWidget(self.linkBtn)
        
        # Add the button layout to the main layout
        self.layout1.addLayout(self.buttonLayout)
        
        # the other graph
        self.graphWidget_2 = pg.PlotWidget(parent= self.centralWidget)
        self.graphWidget_2.setObjectName("graphWidget2")
        self.layout1.addWidget(self.graphWidget_2)
        
        self.buttonLayout2 = QtWidgets.QHBoxLayout()
        
        # Create buttons and add them to the button layout
        self.browseBtn2 = QtWidgets.QPushButton("browse", parent=self.centralWidget)
        self.browseBtn2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.startBtn2 = QtWidgets.QPushButton("start", parent=self.centralWidget)
        self.startBtn2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pauseBtn2 = QtWidgets.QPushButton("pause", parent=self.centralWidget)
        self.pauseBtn2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.rewindBtn2 = QtWidgets.QPushButton("rewind", parent=self.centralWidget)
        self.rewindBtn2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        
        # Add the buttons to the button layout
        self.buttonLayout2.addWidget(self.startBtn2)
        self.buttonLayout2.addWidget(self.pauseBtn2)
        self.buttonLayout2.addWidget(self.rewindBtn2)
        self.buttonLayout2.addWidget(self.browseBtn2)
        
        # Add the button layout to the main layout
        self.layout1.addLayout(self.buttonLayout2)
        
        
        
        # Set up menu bar and status bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        # Finalize UI setup
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    
    
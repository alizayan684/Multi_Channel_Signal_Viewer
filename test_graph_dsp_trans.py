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
        self.graphwidget = pg.PlotWidget(parent=self.centralWidget)
        self.graphwidget.setObjectName("graphwidget")
        self.layout1.addWidget(self.graphwidget)
        
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
        
        # Add the buttons to the button layout
        self.buttonLayout.addWidget(self.startBtn)
        self.buttonLayout.addWidget(self.pauseBtn)
        self.buttonLayout.addWidget(self.rewindBtn)
        self.buttonLayout.addWidget(self.browseBtn)
        
        # Add the button layout to the main layout
        self.layout1.addLayout(self.buttonLayout)
        
        
        
        
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

    
    
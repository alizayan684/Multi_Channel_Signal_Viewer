# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UI_initial_phase.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QListWidget,
    QListWidgetItem, QMainWindow, QPushButton, QScrollBar,
    QSizePolicy, QSlider, QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget

class Ui_SignalViewer(object):
    def setupUi(self, SignalViewer):
        if not SignalViewer.objectName():
            SignalViewer.setObjectName(u"SignalViewer")
        SignalViewer.resize(1057, 754)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SignalViewer.sizePolicy().hasHeightForWidth())
        SignalViewer.setSizePolicy(sizePolicy)
        SignalViewer.setStyleSheet(u"/*\n"
"Material Dark Style Sheet for QT Applications\n"
"Author: Jaime A. Quiroga P.\n"
"Inspired on https://github.com/jxfwinter/qt-material-stylesheet\n"
"Company: GTRONICK\n"
"Last updated: 04/12/2018, 15:00.\n"
"Available at: https://github.com/GTRONICK/QSS/blob/master/MaterialDark.qss\n"
"*/\n"
"QMainWindow {\n"
"	background-color:#1e1d23;\n"
"}\n"
"QMenuBar {\n"
"    background-color: #2E3440; /* Dark background */\n"
"    color: #D8DEE9; /* Light text color */\n"
"    font-size: 16px; /* Font size */\n"
"    padding: 5px; /* Padding around the text */\n"
"    border: 1px solid #4C566A; /* Border color */\n"
"    font-family: \"Segoe UI\", \"Helvetica Neue\", \"Arial\", sans-serif; /* Font family */\n"
"}\n"
"\n"
"QMenuBar::item {\n"
"    background-color: transparent; /* Transparent background */\n"
"    padding: 5px 10px; /* Padding around each item */\n"
"}\n"
"\n"
"QMenuBar::item:selected {\n"
"    background-color: #4C566A; /* Background color when selected */\n"
"    color: #ECEFF4; /* Text color w"
                        "hen selected */\n"
"}\n"
"\n"
"QMenuBar::item:pressed {\n"
"    background-color: #3B4252; /* Background color when pressed */\n"
"    color: #ECEFF4; /* Text color when pressed */\n"
"}\n"
"\n"
"QDialog {\n"
"	background-color:#1e1d23;\n"
"}\n"
"QColorDialog {\n"
"	background-color:#1e1d23;\n"
"}\n"
"QTextEdit {\n"
"	background-color:#1e1d23;\n"
"	color: #a9b7c6;\n"
"}\n"
"QPlainTextEdit {\n"
"	selection-background-color:#007b50;\n"
"	background-color:#1e1d23;\n"
"	border-style: solid;\n"
"	border-top-color: transparent;\n"
"	border-right-color: transparent;\n"
"	border-left-color: transparent;\n"
"	border-bottom-color: transparent;\n"
"	border-width: 1px;\n"
"	color: #a9b7c6;\n"
"}\n"
"QPushButton{\n"
"	border-style: solid;\n"
"	border-top-color: transparent;\n"
"	border-right-color: transparent;\n"
"	border-left-color: transparent;\n"
"	border-bottom-color: transparent;\n"
"	border-width: 1px;\n"
"	border-style: solid;\n"
"	color: #a9b7c6;\n"
"	padding: 2px;\n"
"	background-color: #1e1d23;\n"
"}\n"
"QPushBu"
                        "tton::default{\n"
"	border-style: inset;\n"
"	border-top-color: transparent;\n"
"	border-right-color: transparent;\n"
"	border-left-color: transparent;\n"
"	border-bottom-color: #04b97f;\n"
"	border-width: 1px;\n"
"	color: #a9b7c6;\n"
"	padding: 2px;\n"
"	background-color: #1e1d23;\n"
"}\n"
"QToolButton {\n"
"	border-style: solid;\n"
"	border-top-color: transparent;\n"
"	border-right-color: transparent;\n"
"	border-left-color: transparent;\n"
"	border-bottom-color: #04b97f;\n"
"	border-bottom-width: 1px;\n"
"	border-style: solid;\n"
"	color: #a9b7c6;\n"
"	padding: 2px;\n"
"	background-color: #1e1d23;\n"
"}\n"
"QToolButton:hover{\n"
"	border-style: solid;\n"
"	border-top-color: transparent;\n"
"	border-right-color: transparent;\n"
"	border-left-color: transparent;\n"
"	border-bottom-color: #37efba;\n"
"	border-bottom-width: 2px;\n"
"	border-style: solid;\n"
"	color: #FFFFFF;\n"
"	padding-bottom: 1px;\n"
"	background-color: #1e1d23;\n"
"}\n"
"QPushButton:hover{\n"
"	border-style: solid;\n"
"	border-top-color: tr"
                        "ansparent;\n"
"	border-right-color: transparent;\n"
"	border-left-color: transparent;\n"
"	/*border-bottom-color: #37efba;*/\n"
"\n"
"	border-bottom-width: 1px;\n"
"	border-style: solid;\n"
"	color: #FFFFFF;\n"
"	color: rgb(49, 149, 255);\n"
"	color: rgb(0, 187, 255);\n"
"	padding-bottom: 2px;\n"
"	background-color: #1e1d23;\n"
"}\n"
"QPushButton:pressed{\n"
"	border-style: solid;\n"
"	border-top-color: transparent;\n"
"	border-right-color: transparent;\n"
"	border-left-color: transparent;\n"
"	border-bottom-color: #37efba;\n"
"	border-bottom-width: 2px;\n"
"	border-style: solid;\n"
"	color: #37efba;\n"
"	padding-bottom: 1px;\n"
"	background-color: #1e1d23;\n"
"}\n"
"QPushButton:disabled{\n"
"	border-style: solid;\n"
"	border-top-color: transparent;\n"
"	border-right-color: transparent;\n"
"	border-left-color: transparent;\n"
"	border-bottom-color: #808086;\n"
"	border-bottom-width: 2px;\n"
"	border-style: solid;\n"
"	color: #808086;\n"
"	padding-bottom: 1px;\n"
"	background-color: #1e1d23;\n"
"}\n"
"QLineEdit"
                        " {\n"
"	border-width: 1px; border-radius: 4px;\n"
"	border-color: rgb(58, 58, 58);\n"
"	border-style: inset;\n"
"	padding: 0 8px;\n"
"	color: #a9b7c6;\n"
"	background:#1e1d23;\n"
"	selection-background-color:#007b50;\n"
"	selection-color: #FFFFFF;\n"
"}\n"
"QLabel {\n"
"	color: #a9b7c6;\n"
"}\n"
"QLCDNumber {\n"
"	color: #37e6b4;\n"
"}\n"
"QProgressBar {\n"
"	text-align: center;\n"
"	color: rgb(240, 240, 240);\n"
"	border-width: 1px; \n"
"	border-radius: 10px;\n"
"	border-color: rgb(58, 58, 58);\n"
"	border-style: inset;\n"
"	background-color:#1e1d23;\n"
"}\n"
"QProgressBar::chunk {\n"
"	background-color: #04b97f;\n"
"	border-radius: 5px;\n"
"}\n"
"QMenuBar {\n"
"	background-color: #1e1d23;\n"
"}\n"
"QMenuBar::item {\n"
"	color: #a9b7c6;\n"
"  	spacing: 3px;\n"
"  	padding: 1px 4px;\n"
"  	background: #1e1d23;\n"
"}\n"
"\n"
"QMenuBar::item:selected {\n"
"  	background:#1e1d23;\n"
"	color: #FFFFFF;\n"
"}\n"
"QMenu::item:selected {\n"
"	border-style: solid;\n"
"	border-top-color: transparent;\n"
"	border-right-c"
                        "olor: transparent;\n"
"	border-left-color: #04b97f;\n"
"	border-bottom-color: transparent;\n"
"	border-left-width: 2px;\n"
"	color: #FFFFFF;\n"
"	padding-left:15px;\n"
"	padding-top:4px;\n"
"	padding-bottom:4px;\n"
"	padding-right:7px;\n"
"	background-color: #1e1d23;\n"
"}\n"
"QMenu::item {\n"
"	border-style: solid;\n"
"	border-top-color: transparent;\n"
"	border-right-color: transparent;\n"
"	border-left-color: transparent;\n"
"	border-bottom-color: transparent;\n"
"	border-bottom-width: 1px;\n"
"	border-style: solid;\n"
"	color: #a9b7c6;\n"
"	padding-left:17px;\n"
"	padding-top:4px;\n"
"	padding-bottom:4px;\n"
"	padding-right:7px;\n"
"	background-color: #1e1d23;\n"
"}\n"
"QMenu{\n"
"	background-color:#1e1d23;\n"
"}\n"
"QTabWidget {\n"
"	color:rgb(0,0,0);\n"
"	background-color:#1e1d23;\n"
"}\n"
"QTabWidget::pane {\n"
"		border-color: rgb(77,77,77);\n"
"		background-color:#1e1d23;\n"
"		border-style: solid;\n"
"		border-width: 1px;\n"
"    	border-radius: 6px;\n"
"}\n"
"QTabBar::tab {\n"
"	border-style: solid;"
                        "\n"
"	border-top-color: transparent;\n"
"	border-right-color: transparent;\n"
"	border-left-color: transparent;\n"
"	border-bottom-color: transparent;\n"
"	border-bottom-width: 1px;\n"
"	border-style: solid;\n"
"	color: #808086;\n"
"	padding: 3px;\n"
"	margin-left:3px;\n"
"	background-color: #1e1d23;\n"
"}\n"
"QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {\n"
"  	border-style: solid;\n"
"	border-top-color: transparent;\n"
"	border-right-color: transparent;\n"
"	border-left-color: transparent;\n"
"	border-bottom-color: #04b97f;\n"
"	border-bottom-width: 2px;\n"
"	border-style: solid;\n"
"	color: #FFFFFF;\n"
"	padding-left: 3px;\n"
"	padding-bottom: 2px;\n"
"	margin-left:3px;\n"
"	background-color: #1e1d23;\n"
"}\n"
"\n"
"QCheckBox {\n"
"	color: #a9b7c6;\n"
"	padding: 2px;\n"
"}\n"
"QCheckBox:disabled {\n"
"	color: #808086;\n"
"	padding: 2px;\n"
"}\n"
"\n"
"QCheckBox:hover {\n"
"	border-radius:4px;\n"
"	border-style:solid;\n"
"	padding-left: 1px;\n"
"	padding-right: 1px;\n"
"	padding-bot"
                        "tom: 1px;\n"
"	padding-top: 1px;\n"
"	border-width:1px;\n"
"	border-color: rgb(87, 97, 106);\n"
"	background-color:#1e1d23;\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"\n"
"	height: 10px;\n"
"	width: 10px;\n"
"	border-style:solid;\n"
"	border-width: 1px;\n"
"	border-color: #04b97f;\n"
"	color: #a9b7c6;\n"
"	background-color: #04b97f;\n"
"}\n"
"QCheckBox::indicator:unchecked {\n"
"\n"
"	height: 10px;\n"
"	width: 10px;\n"
"	border-style:solid;\n"
"	border-width: 1px;\n"
"	border-color: #04b97f;\n"
"	color: #a9b7c6;\n"
"	background-color: transparent;\n"
"}\n"
"QRadioButton {\n"
"	color: #a9b7c6;\n"
"	background-color: #1e1d23;\n"
"	padding: 1px;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"	height: 10px;\n"
"	width: 10px;\n"
"	border-style:solid;\n"
"	border-radius:5px;\n"
"	border-width: 1px;\n"
"	border-color: #04b97f;\n"
"	color: #a9b7c6;\n"
"	background-color: #04b97f;\n"
"}\n"
"QRadioButton::indicator:!checked {\n"
"	height: 10px;\n"
"	width: 10px;\n"
"	border-style:solid;\n"
"	border-radius:5px;\n"
"	b"
                        "order-width: 1px;\n"
"	border-color: #04b97f;\n"
"	color: #a9b7c6;\n"
"	background-color: transparent;\n"
"}\n"
"QStatusBar {\n"
"	color:#027f7f;\n"
"}\n"
"QSpinBox {\n"
"	color: #a9b7c6;	\n"
"	background-color: #1e1d23;\n"
"}\n"
"QDoubleSpinBox {\n"
"	color: #a9b7c6;	\n"
"	background-color: #1e1d23;\n"
"}\n"
"QTimeEdit {\n"
"	color: #a9b7c6;	\n"
"	background-color: #1e1d23;\n"
"}\n"
"QDateTimeEdit {\n"
"	color: #a9b7c6;	\n"
"	background-color: #1e1d23;\n"
"}\n"
"QDateEdit {\n"
"	color: #a9b7c6;	\n"
"	background-color: #1e1d23;\n"
"}\n"
"QComboBox {\n"
"	color: #a9b7c6;	\n"
"	background: #1e1d23;\n"
"}\n"
"QComboBox:editable {\n"
"	background: #1e1d23;\n"
"	color: #a9b7c6;\n"
"	selection-background-color: #1e1d23;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"	color: #a9b7c6;	\n"
"	background: #1e1d23;\n"
"	selection-color: #FFFFFF;\n"
"	selection-background-color: #1e1d23;\n"
"}\n"
"QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
"	color: #a9b7c6;	\n"
"	background: #1e1d23;\n"
"}\n"
"QFontComboBox"
                        " {\n"
"	color: #a9b7c6;	\n"
"	background-color: #1e1d23;\n"
"}\n"
"QToolBox {\n"
"	color: #a9b7c6;\n"
"	background-color: #1e1d23;\n"
"}\n"
"QToolBox::tab {\n"
"	color: #a9b7c6;\n"
"	background-color: #1e1d23;\n"
"}\n"
"QToolBox::tab:selected {\n"
"	color: #FFFFFF;\n"
"	background-color: #1e1d23;\n"
"}\n"
"QScrollArea {\n"
"	color: #FFFFFF;\n"
"	background-color: #1e1d23;\n"
"}\n"
"QSlider::groove:horizontal {\n"
"	height: 5px;\n"
"	background: #04b97f;\n"
"}\n"
"QSlider::groove:vertical {\n"
"	width: 5px;\n"
"	background: #04b97f;\n"
"}\n"
"QSlider::handle:horizontal {\n"
"	background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);\n"
"	border: 1px solid #5c5c5c;\n"
"	width: 14px;\n"
"	margin: -5px 0;\n"
"	border-radius: 7px;\n"
"}\n"
"QSlider::handle:vertical {\n"
"	background: qlineargradient(x1:1, y1:1, x2:0, y2:0, stop:0 #b4b4b4, stop:1 #8f8f8f);\n"
"	border: 1px solid #5c5c5c;\n"
"	height: 14px;\n"
"	margin: 0 -5px;\n"
"	border-radius: 7px;\n"
"}\n"
"QSlider::add-page:horizontal"
                        " {\n"
"    background: white;\n"
"}\n"
"QSlider::add-page:vertical {\n"
"    background: white;\n"
"}\n"
"QSlider::sub-page:horizontal {\n"
"    background: #04b97f;\n"
"}\n"
"QSlider::sub-page:vertical {\n"
"    background: #04b97f;\n"
"}\n"
"QPushButton {\n"
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
"    font-family: \"Segoe"
                        " UI\", \"Helvetica Neue\", \"Arial\", sans-serif; /* Font family */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #3B4252; /* Background color when pressed */\n"
"    border: 2px solid #4C566A; /* Border color when pressed */\n"
"}\n"
"")
        self.actionOpen_File = QAction(SignalViewer)
        self.actionOpen_File.setObjectName(u"actionOpen_File")
        self.actionDelete = QAction(SignalViewer)
        self.actionDelete.setObjectName(u"actionDelete")
        self.centralwidget = QWidget(SignalViewer)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetNoConstraint)
        self.plotWidget_1 = PlotWidget(self.centralwidget)
        self.plotWidget_1.setObjectName(u"plotWidget_1")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.plotWidget_1.sizePolicy().hasHeightForWidth())
        self.plotWidget_1.setSizePolicy(sizePolicy1)
        self.plotWidget_1.setStyleSheet(u"    background-color: #000000; /* Dark background */\n"
"    color: #D8DEE9; /* Light text color */\n"
"    font-size: 16px; /* Font size */\n"
"    padding: 5px; /* Padding around the text */\n"
"    border: 2px solid #4C566A; /* Border color */\n"
"    border-radius: 5px; /* Rounded corners */\n"
"    font-family: \"Segoe UI\", \"Helvetica Neue\", \"Arial\", sans-serif; /* Font family */\n"
"")

        self.verticalLayout.addWidget(self.plotWidget_1)

        self.horizontalScrollBar_1 = QScrollBar(self.centralwidget)
        self.horizontalScrollBar_1.setObjectName(u"horizontalScrollBar_1")
        self.horizontalScrollBar_1.setStyleSheet(u"/* Scrollbar background */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background-color: #2E3440; /* Dark background */\n"
"    height: 12px;\n"
"    margin: 0px 0px 0px 0px;\n"
"}\n"
"\n"
"/* Handle */\n"
"QScrollBar::handle:horizontal {\n"
"    background: #888;\n"
"    min-width: 20px;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"/* Handle on hover */\n"
"QScrollBar::handle:horizontal:hover {\n"
"    background: #555;\n"
"}\n"
"\n"
"/* Add-line (right arrow) */\n"
"QScrollBar::add-line:horizontal {\n"
"    background: none;\n"
"    width: 0px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"/* Sub-line (left arrow) */\n"
"QScrollBar::sub-line:horizontal {\n"
"    background: none;\n"
"    width: 0px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"/* Add-page and sub-page (scrollbar background to the left and right of the handle) */\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
"    background:"
                        " none;\n"
"}\n"
"")
        self.horizontalScrollBar_1.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.horizontalScrollBar_1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.speedLabel_1 = QLabel(self.centralwidget)
        self.speedLabel_1.setObjectName(u"speedLabel_1")
        self.speedLabel_1.setStyleSheet(u"QLabel {\n"
"    background-color: #2E3440; /* Dark background */\n"
"    color: #D8DEE9; /* Light text color */\n"
"    font-size: 16px; /* Font size */\n"
"    padding: 2px; /* Padding around the text */\n"
"    border: 2px solid #4C566A; /* Border color */\n"
"    border-radius: 5px; /* Rounded corners */\n"
"    font-family: \"Segoe UI\"\n"
"}")

        self.horizontalLayout_10.addWidget(self.speedLabel_1)

        self.speedSlider_1 = QSlider(self.centralwidget)
        self.speedSlider_1.setObjectName(u"speedSlider_1")
        self.speedSlider_1.setOrientation(Qt.Horizontal)

        self.horizontalLayout_10.addWidget(self.speedSlider_1)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.plotWidget_2 = PlotWidget(self.centralwidget)
        self.plotWidget_2.setObjectName(u"plotWidget_2")
        sizePolicy1.setHeightForWidth(self.plotWidget_2.sizePolicy().hasHeightForWidth())
        self.plotWidget_2.setSizePolicy(sizePolicy1)
        self.plotWidget_2.setStyleSheet(u"    background-color: #000000; /* Dark background */\n"
"    color: #D8DEE9; /* Light text color */\n"
"    font-size: 16px; /* Font size */\n"
"    padding: 5px; /* Padding around the text */\n"
"    border: 2px solid #4C566A; /* Border color */\n"
"    border-radius: 5px; /* Rounded corners */\n"
"    font-family: \"Segoe UI\", \"Helvetica Neue\", \"Arial\", sans-serif; /* Font family */\n"
"")

        self.verticalLayout.addWidget(self.plotWidget_2)

        self.horizontalScrollBar_2 = QScrollBar(self.centralwidget)
        self.horizontalScrollBar_2.setObjectName(u"horizontalScrollBar_2")
        self.horizontalScrollBar_2.setStyleSheet(u"/* Scrollbar background */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background-color: #2E3440; /* Dark background */\n"
"    height: 12px;\n"
"    margin: 0px 0px 0px 0px;\n"
"}\n"
"\n"
"/* Handle */\n"
"QScrollBar::handle:horizontal {\n"
"    background: #888;\n"
"    min-width: 20px;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"/* Handle on hover */\n"
"QScrollBar::handle:horizontal:hover {\n"
"    background: #555;\n"
"}\n"
"\n"
"/* Add-line (right arrow) */\n"
"QScrollBar::add-line:horizontal {\n"
"    background: none;\n"
"    width: 0px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"/* Sub-line (left arrow) */\n"
"QScrollBar::sub-line:horizontal {\n"
"    background: none;\n"
"    width: 0px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"/* Add-page and sub-page (scrollbar background to the left and right of the handle) */\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
"    background:"
                        " none;\n"
"}\n"
"")
        self.horizontalScrollBar_2.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.horizontalScrollBar_2)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.speedLabel_2 = QLabel(self.centralwidget)
        self.speedLabel_2.setObjectName(u"speedLabel_2")
        self.speedLabel_2.setStyleSheet(u"QLabel {\n"
"    background-color: #2E3440; /* Dark background */\n"
"    color: #D8DEE9; /* Light text color */\n"
"    font-size: 16px; /* Font size */\n"
"    padding: 2px; /* Padding around the text */\n"
"    border: 2px solid #4C566A; /* Border color */\n"
"    border-radius: 5px; /* Rounded corners */\n"
"    font-family: \"Segoe UI\"\n"
"}")

        self.horizontalLayout_8.addWidget(self.speedLabel_2)

        self.speedSlider_2 = QSlider(self.centralwidget)
        self.speedSlider_2.setObjectName(u"speedSlider_2")
        self.speedSlider_2.setOrientation(Qt.Horizontal)

        self.horizontalLayout_8.addWidget(self.speedSlider_2)


        self.verticalLayout.addLayout(self.horizontalLayout_8)


        self.gridLayout.addLayout(self.verticalLayout, 3, 1, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalScrollBar_1 = QScrollBar(self.centralwidget)
        self.verticalScrollBar_1.setObjectName(u"verticalScrollBar_1")
        self.verticalScrollBar_1.setStyleSheet(u"/* Scrollbar background */\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background-color: #2E3440; /* Dark background */\n"
"    width: 12px;\n"
"    margin: 0px 0px 0px 0px;\n"
"}\n"
"\n"
"/* Handle */\n"
"QScrollBar::handle:vertical {\n"
"    background: #888;\n"
"    min-height: 20px;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"/* Handle on hover */\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #555;\n"
"}\n"
"\n"
"/* Add-line (down arrow) */\n"
"QScrollBar::add-line:vertical {\n"
"    background: none;\n"
"    height: 0px;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"/* Sub-line (up arrow) */\n"
"QScrollBar::sub-line:vertical {\n"
"    background: none;\n"
"    height: 0px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"/* Add-page and sub-page (scrollbar background above and below the handle) */\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}\n"
"")
        self.verticalScrollBar_1.setOrientation(Qt.Vertical)

        self.verticalLayout_2.addWidget(self.verticalScrollBar_1)

        self.verticalScrollBar_2 = QScrollBar(self.centralwidget)
        self.verticalScrollBar_2.setObjectName(u"verticalScrollBar_2")
        self.verticalScrollBar_2.setStyleSheet(u"/* Scrollbar background */\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background-color: #2E3440; /* Dark background */\n"
"    width: 12px;\n"
"    margin: 0px 0px 0px 0px;\n"
"\n"
"\n"
"}\n"
"\n"
"/* Handle */\n"
"QScrollBar::handle:vertical {\n"
"    background: #888;\n"
"    min-height: 20px;\n"
"    border-radius: 6px;\n"
"\n"
"}\n"
"\n"
"/* Handle on hover */\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #555;\n"
"\n"
"\n"
"}\n"
"\n"
"/* Add-line (down arrow) */\n"
"QScrollBar::add-line:vertical {\n"
"    background: none;\n"
"    height: 0px;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"\n"
"}\n"
"\n"
"/* Sub-line (up arrow) */\n"
"QScrollBar::sub-line:vertical {\n"
"    background: none;\n"
"    height: 0px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"/* Add-page and sub-page (scrollbar background above and below the handle) */\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    backg"
                        "round: none;\n"
"}\n"
"")
        self.verticalScrollBar_2.setOrientation(Qt.Vertical)

        self.verticalLayout_2.addWidget(self.verticalScrollBar_2)


        self.gridLayout.addLayout(self.verticalLayout_2, 3, 6, 1, 1)

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setSizeConstraint(QLayout.SetMinimumSize)
        self.graphLabel_1 = QLabel(self.centralwidget)
        self.graphLabel_1.setObjectName(u"graphLabel_1")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.graphLabel_1.sizePolicy().hasHeightForWidth())
        self.graphLabel_1.setSizePolicy(sizePolicy2)
        self.graphLabel_1.setMaximumSize(QSize(16777215, 30))
        self.graphLabel_1.setStyleSheet(u"QLabel {\n"
"    background-color: #2E3440; /* Dark background */\n"
"    color: #D8DEE9; /* Light text color */\n"
"    font-size: 16px; /* Font size */\n"
"    padding: 2px; /* Padding around the text */\n"
"    border: 2px solid #4C566A; /* Border color */\n"
"    border-radius: 5px; /* Rounded corners */\n"
"    font-family: \"Segoe UI\"\n"
"}")

        self.verticalLayout_13.addWidget(self.graphLabel_1)

        self.selectChannelBox_1 = QComboBox(self.centralwidget)
        self.selectChannelBox_1.addItem("")
        self.selectChannelBox_1.setObjectName(u"selectChannelBox_1")
        self.selectChannelBox_1.setMinimumSize(QSize(0, 40))
        self.selectChannelBox_1.setMaximumSize(QSize(200, 40))
        self.selectChannelBox_1.setStyleSheet(u"QComboBox{\n"
" font-size: 16px; /* Font size */\n"
"   padding: 2px; /* Padding around the text */\n"
"    border: 2px solid; /* Border color */\n"
"    border-radius: 5px; /* Rounded corners */\n"
"    font-family: \"Segoe UI\"\n"
"}")

        self.verticalLayout_13.addWidget(self.selectChannelBox_1)

        self.listChannelsWidget_1 = QListWidget(self.centralwidget)
        self.listChannelsWidget_1.setObjectName(u"listChannelsWidget_1")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.listChannelsWidget_1.sizePolicy().hasHeightForWidth())
        self.listChannelsWidget_1.setSizePolicy(sizePolicy3)
        self.listChannelsWidget_1.setMaximumSize(QSize(200, 300))
        self.listChannelsWidget_1.setStyleSheet(u"QListWidget {\n"
"    background-color: #2E3440; /* Dark background */\n"
"    color: #D8DEE9; /* Light text color */\n"
"    font-size: 16px; /* Font size */\n"
"    padding: 5px; /* Padding around the text */\n"
"    border: 2px solid #4C566A; /* Border color */\n"
"    border-radius: 5px; /* Rounded corners */\n"
"    font-family: \"Segoe UI\", \"Helvetica Neue\", \"Arial\", sans-serif; /* Font family */\n"
"}\n"
"\n"
"QListWidget::item {\n"
"    padding: 5px; /* Padding around each item */\n"
"    border-bottom: 1px solid #4C566A; /* Border between items */\n"
"}\n"
"\n"
"QListWidget::item:selected {\n"
"    background-color: #4C566A; /* Background color for selected item */\n"
"    color: #ECEFF4; /* Text color for selected item */\n"
"}\n"
"")

        self.verticalLayout_13.addWidget(self.listChannelsWidget_1)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setStyleSheet(u"background-color: rgb(4, 3, 3);")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_13.addWidget(self.line_2)

        self.graphLabel_2 = QLabel(self.centralwidget)
        self.graphLabel_2.setObjectName(u"graphLabel_2")
        self.graphLabel_2.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.graphLabel_2.sizePolicy().hasHeightForWidth())
        self.graphLabel_2.setSizePolicy(sizePolicy2)
        self.graphLabel_2.setMaximumSize(QSize(16777215, 30))
        self.graphLabel_2.setStyleSheet(u"QLabel {\n"
"    background-color: #2E3440; /* Dark background */\n"
"    color: #D8DEE9; /* Light text color */\n"
"    font-size: 16px; /* Font size */\n"
"    padding: 2px; /* Padding around the text */\n"
"    border: 2px solid #4C566A; /* Border color */\n"
"    border-radius: 5px; /* Rounded corners */\n"
"    font-family: \"Segoe UI\"\n"
"}")

        self.verticalLayout_13.addWidget(self.graphLabel_2)

        self.selectChannelBox_2 = QComboBox(self.centralwidget)
        self.selectChannelBox_2.addItem("")
        self.selectChannelBox_2.setObjectName(u"selectChannelBox_2")
        self.selectChannelBox_2.setMinimumSize(QSize(0, 40))
        self.selectChannelBox_2.setMaximumSize(QSize(200, 40))
        self.selectChannelBox_2.setStyleSheet(u" font-size: 16px; /* Font size */\n"
"    padding: 2px; /* Padding around the text */\n"
"    border: 2px solid; /* Border color */\n"
"    border-radius: 5px; /* Rounded corners */\n"
"    font-family: \"Segoe UI\"")

        self.verticalLayout_13.addWidget(self.selectChannelBox_2)

        self.listChannelsWidget_2 = QListWidget(self.centralwidget)
        self.listChannelsWidget_2.setObjectName(u"listChannelsWidget_2")
        sizePolicy3.setHeightForWidth(self.listChannelsWidget_2.sizePolicy().hasHeightForWidth())
        self.listChannelsWidget_2.setSizePolicy(sizePolicy3)
        self.listChannelsWidget_2.setMaximumSize(QSize(200, 300))
        self.listChannelsWidget_2.setStyleSheet(u"QListWidget {\n"
"    background-color: #2E3440; /* Dark background */\n"
"    color: #D8DEE9; /* Light text color */\n"
"    font-size: 16px; /* Font size */\n"
"    padding: 5px; /* Padding around the text */\n"
"    border: 2px solid #4C566A; /* Border color */\n"
"    border-radius: 5px; /* Rounded corners */\n"
"    font-family: \"Segoe UI\", \"Helvetica Neue\", \"Arial\", sans-serif; /* Font family */\n"
"}\n"
"\n"
"QListWidget::item {\n"
"    padding: 5px; /* Padding around each item */\n"
"    border-bottom: 1px solid #4C566A; /* Border between items */\n"
"}\n"
"\n"
"QListWidget::item:selected {\n"
"    background-color: #4C566A; /* Background color for selected item */\n"
"    color: #ECEFF4; /* Text color for selected item */\n"
"}\n"
"")

        self.verticalLayout_13.addWidget(self.listChannelsWidget_2)


        self.gridLayout.addLayout(self.verticalLayout_13, 3, 8, 1, 1)

        self.glueButton = QPushButton(self.centralwidget)
        self.glueButton.setObjectName(u"glueButton")
        self.glueButton.setMaximumSize(QSize(200, 40))

        self.gridLayout.addWidget(self.glueButton, 2, 8, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.addFileButton = QPushButton(self.centralwidget)
        self.addFileButton.setObjectName(u"addFileButton")
        self.addFileButton.setMaximumSize(QSize(200, 40))

        self.horizontalLayout_6.addWidget(self.addFileButton)

        self.connectOnlineButton = QPushButton(self.centralwidget)
        self.connectOnlineButton.setObjectName(u"connectOnlineButton")
        self.connectOnlineButton.setMaximumSize(QSize(200, 40))

        self.horizontalLayout_6.addWidget(self.connectOnlineButton)

        self.linkButton = QPushButton(self.centralwidget)
        self.linkButton.setObjectName(u"linkButton")
        sizePolicy3.setHeightForWidth(self.linkButton.sizePolicy().hasHeightForWidth())
        self.linkButton.setSizePolicy(sizePolicy3)
        self.linkButton.setMaximumSize(QSize(200, 40))

        self.horizontalLayout_6.addWidget(self.linkButton)

        self.graphSelectBox = QComboBox(self.centralwidget)
        self.graphSelectBox.addItem("")
        self.graphSelectBox.addItem("")
        self.graphSelectBox.setObjectName(u"graphSelectBox")
        self.graphSelectBox.setMaximumSize(QSize(200, 40))
        self.graphSelectBox.setStyleSheet(u" font-size: 16px; /* Font size */\n"
"    padding: 2px; /* Padding around the text */\n"
"    border: 2px solid ; /* Border color */\n"
"    border-radius: 5px; /* Rounded corners */\n"
"    font-family: \"Segoe UI\"")

        self.horizontalLayout_6.addWidget(self.graphSelectBox)


        self.gridLayout.addLayout(self.horizontalLayout_6, 2, 1, 1, 1)

        self.nonRectGraphButton = QPushButton(self.centralwidget)
        self.nonRectGraphButton.setObjectName(u"nonRectGraphButton")
        self.nonRectGraphButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #ffffff; /* Background color on hover */\n"
"\n"
"    color: #000000; /* Light text color */\n"
"    font-size: 16px; /* Font size */\n"
"    padding: 10px 20px; /* Padding around the text */\n"
"    border: 2px solid #2E3440; /* Border color */\n"
"    border-radius: 5px; /* Rounded corners */\n"
"    font-family: \"Segoe UI\", \"Helvetica Neue\", \"Arial\", sans-serif; /* Font family */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: #ffffff;\n"
"	color: rgb(0, 0, 0);\n"
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

        self.gridLayout.addWidget(self.nonRectGraphButton, 4, 8, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(7)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.colorButton = QPushButton(self.centralwidget)
        self.colorButton.setObjectName(u"colorButton")
        sizePolicy3.setHeightForWidth(self.colorButton.sizePolicy().hasHeightForWidth())
        self.colorButton.setSizePolicy(sizePolicy3)
        self.colorButton.setMaximumSize(QSize(200, 40))
        self.colorButton.setStyleSheet(u"")

        self.horizontalLayout_11.addWidget(self.colorButton)

        self.moveButton = QPushButton(self.centralwidget)
        self.moveButton.setObjectName(u"moveButton")
        sizePolicy3.setHeightForWidth(self.moveButton.sizePolicy().hasHeightForWidth())
        self.moveButton.setSizePolicy(sizePolicy3)
        self.moveButton.setMaximumSize(QSize(200, 40))

        self.horizontalLayout_11.addWidget(self.moveButton)

        self.colorMoveBox = QComboBox(self.centralwidget)
        self.colorMoveBox.addItem("")
        self.colorMoveBox.setObjectName(u"colorMoveBox")
        self.colorMoveBox.setMaximumSize(QSize(200, 40))
        self.colorMoveBox.setStyleSheet(u" font-size: 16px; /* Font size */\n"
"    padding: 2px; /* Padding around the text */\n"
"    border: 2px solid ; /* Border color */\n"
"    border-radius: 5px; /* Rounded corners */\n"
"    font-family: \"Segoe UI\"")

        self.horizontalLayout_11.addWidget(self.colorMoveBox)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_11)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setStyleSheet(u"background-color: rgb(0, 170, 0);")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_7.addWidget(self.line)

        self.rewindButton = QPushButton(self.centralwidget)
        self.rewindButton.setObjectName(u"rewindButton")
        self.rewindButton.setMaximumSize(QSize(200, 40))

        self.horizontalLayout_7.addWidget(self.rewindButton)

        self.zoomOutButton = QPushButton(self.centralwidget)
        self.zoomOutButton.setObjectName(u"zoomOutButton")
        self.zoomOutButton.setMaximumSize(QSize(200, 40))

        self.horizontalLayout_7.addWidget(self.zoomOutButton)

        self.zoomInButton = QPushButton(self.centralwidget)
        self.zoomInButton.setObjectName(u"zoomInButton")
        self.zoomInButton.setMaximumSize(QSize(200, 40))

        self.horizontalLayout_7.addWidget(self.zoomInButton)

        self.stopButton = QPushButton(self.centralwidget)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setMaximumSize(QSize(200, 40))

        self.horizontalLayout_7.addWidget(self.stopButton)

        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")
        sizePolicy3.setHeightForWidth(self.startButton.sizePolicy().hasHeightForWidth())
        self.startButton.setSizePolicy(sizePolicy3)
        self.startButton.setMaximumSize(QSize(200, 40))

        self.horizontalLayout_7.addWidget(self.startButton)


        self.gridLayout.addLayout(self.horizontalLayout_7, 4, 1, 1, 1)

        SignalViewer.setCentralWidget(self.centralwidget)

        self.retranslateUi(SignalViewer)

        QMetaObject.connectSlotsByName(SignalViewer)
    # setupUi

    def retranslateUi(self, SignalViewer):
        SignalViewer.setWindowTitle(QCoreApplication.translate("SignalViewer", u"MainWindow", None))
        self.actionOpen_File.setText(QCoreApplication.translate("SignalViewer", u"Open", None))
        self.actionDelete.setText(QCoreApplication.translate("SignalViewer", u"Delete", None))
        self.speedLabel_1.setText(QCoreApplication.translate("SignalViewer", u"Speed", None))
        self.speedLabel_2.setText(QCoreApplication.translate("SignalViewer", u"Speed", None))
        self.graphLabel_1.setText(QCoreApplication.translate("SignalViewer", u"Graph 1", None))
        self.selectChannelBox_1.setItemText(0, QCoreApplication.translate("SignalViewer", u"All Channels", None))

        self.graphLabel_2.setText(QCoreApplication.translate("SignalViewer", u"Graph 2", None))
        self.selectChannelBox_2.setItemText(0, QCoreApplication.translate("SignalViewer", u"All Channels", None))

        self.glueButton.setText(QCoreApplication.translate("SignalViewer", u"Glue", None))
        self.addFileButton.setText(QCoreApplication.translate("SignalViewer", u"Add File", None))
        self.connectOnlineButton.setText(QCoreApplication.translate("SignalViewer", u"Connnect Online", None))
        self.linkButton.setText(QCoreApplication.translate("SignalViewer", u"Link", None))
        self.graphSelectBox.setItemText(0, QCoreApplication.translate("SignalViewer", u"Graph 1", None))
        self.graphSelectBox.setItemText(1, QCoreApplication.translate("SignalViewer", u"Graph 2", None))

        self.nonRectGraphButton.setText(QCoreApplication.translate("SignalViewer", u"Non Rect Graph", None))
        self.colorButton.setText(QCoreApplication.translate("SignalViewer", u"Color", None))
        self.moveButton.setText(QCoreApplication.translate("SignalViewer", u"Move", None))
        self.colorMoveBox.setItemText(0, QCoreApplication.translate("SignalViewer", u"All Channels", None))

        self.rewindButton.setText(QCoreApplication.translate("SignalViewer", u"Rewind", None))
        self.zoomOutButton.setText(QCoreApplication.translate("SignalViewer", u"Zoom Out", None))
        self.zoomInButton.setText(QCoreApplication.translate("SignalViewer", u"Zoom In", None))
        self.stopButton.setText(QCoreApplication.translate("SignalViewer", u"Stop", None))
        self.startButton.setText(QCoreApplication.translate("SignalViewer", u"Start", None))
    # retranslateUi


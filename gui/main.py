import sys
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import pyqtgraph as pg
import numpy as np
import math
import video_eye_tracking_1
import eeg_widget
#import timeline

try:
    _fromUtf8 = str
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def __init__(self):
        self.time = 0
        self.eeg = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setGeometry(0, 0, 1920, 2000)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.video_widget = video_eye_tracking_1.eyeTrackingWidget(self.centralWidget)
        self.video_widget.setObjectName(_fromUtf8("eyeTrackingWidget"))
        #self.tl = timeline.timeline(self.centralWidget)


        self.eegWidget = eeg_widget.eegWidget(self.centralWidget)
        self.eegWidget.setGeometry(QtCore.QRect(0, 750, self.video_widget.view_width + 2, 350))
        self.eegWidget.setObjectName(_fromUtf8("graphicsView"))

        self.video_widget.openbutton4.clicked.connect(self.eegWidget.open_file)

        self.video_widget.positionSlider.rangeChanged.connect(self.syncEggRange)
        self.video_widget.positionSlider.valueChanged.connect(self.SyncScroll)
        self.eegWidget.positionSlider.sliderMoved.connect(self.updateScroll)

        MainWindow.setCentralWidget(self.centralWidget)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def syncEggRange(self):
        self.eegWidget.positionSlider.setRange(0, self.video_widget.positionSlider.maximum())

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))

    def SyncScroll(self,position):
        self.eegWidget.positionSlider.setValue(position)

    def updateScroll(self,position):
        self.video_widget.player.pause()
        self.video_widget.positionSlider.setValue(position)
        self.video_widget.player.setPosition(position)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.resize(1920, 2000)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    #ui.drawCurve(eeg)
    # ui.cal_content()
    # t = QtCore.QTimer()
    
    sys.exit(app.exec_())

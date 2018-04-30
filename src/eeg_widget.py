import sys
import os
from pathlib import Path
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import utility
import numpy as np
import math
#import pandas
import pyqtgraph
import sip

class eegWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.eeg_data = None
        self.graph_width = 1280
        self.graph_height = 350
        self.time = 0
        self.eeg = None
        self.views = []
        self.view_plots = []
        self.view2ObjectIndex = []
        self.layout = QtWidgets.QVBoxLayout(self)
        pyqtgraph.setConfigOption('leftButtonPan', False)
        self.createUI()



    def createUI(self):

        # video position slider
        self.graph_widget = QtWidgets.QWidget()
        # Layout of Container Widget
        self.graph_layout = QtWidgets.QVBoxLayout()
        self.graph_widget.setLayout(self.graph_layout)

        self.scrollarea = QtWidgets.QScrollArea()
        self.scrollarea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollarea.setWidgetResizable(True)
        # self.scrollarea.setGeometry(10, 0, self.graph_width, self.graph_height * 3)
        self.scrollarea.setWidget(self.graph_widget)

        self.positionSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.positionSlider.setStyleSheet("QSlider::groove:horizontal {background-color:grey;}"
                                "QSlider::handle:horizontal {background-color:black; height:8px; width: 8px;}")
        self.positionSlider.valueChanged.connect(self.update_eeg_graph)

        self.hbuttonbox = QtWidgets.QHBoxLayout()
        self.openbutton = QtWidgets.QPushButton("Open EEG")
        self.comboLabel = QtWidgets.QLabel("Select Channels:")
        self.combobox = QtWidgets.QComboBox(self)
        self.comboboxDelegate = utility.SubclassOfQStyledItemDelegate()
        self.combobox.setItemDelegate(self.comboboxDelegate)
        self.combobox.setSizeAdjustPolicy(0)
        self.hbuttonbox.addWidget(self.openbutton)
        self.hbuttonbox.addWidget(self.comboLabel)
        self.hbuttonbox.addWidget(self.combobox)
        self.openbutton.clicked.connect(self.open_file)

        self.hbuttonbox.addStretch(1)
        self.layout.addWidget(self.scrollarea)
        self.layout.addWidget(self.positionSlider)
        self.layout.addLayout(self.hbuttonbox)
        self.setLayout(self.layout)

    def update_eeg_graph(self):
        if(self.eeg_data is not None and self.eeg_data.shape[0] != 0):
            self.updateData(self.positionSlider.value())

    def lowestGreaterThan(self, arr, threshold):
        # print(arr.shape)
        low = 0
        high = len(arr)
        while low < high:
            mid = int(math.floor((low + high) / 2))
            # print("low = ", low, " mid = ", mid, " high = ", high)
            if arr[mid] == threshold:
                return mid
            elif arr[mid] < threshold and mid != low:
                low = mid
            elif arr[mid] > threshold and mid != high:
                high = mid
            else:
                # terminate with index pointing to the first element greater than low
                high = low = low + 1
        return low

    def GreatestLowerThan(self, arr, threshold):
        # print(arr.shape)
        low = 0
        high = len(arr)
        while low < high:
            mid = int(math.floor((low + high) / 2))
            # print("low = ", low, " mid = ", mid, " high = ", high)
            if arr[mid] == threshold:
                return mid
            elif arr[mid] < threshold and mid != low:
                low = mid
            elif arr[mid] > threshold and mid != high:
                high = mid
            else:
                # terminate with index pointing to the first element greater than low
                high = low
        return high

    def drawCurve(self, i):
        self.time = self.positionSlider.value()
        start_time = self.time - 2000
        end_time = self.time + 2000
        max = np.max(self.eeg_data[i + 1, :])
        min = np.min(self.eeg_data[i + 1, :])
        y, x = self.cal_content(start_time=start_time, end_time=end_time, row=i+1)
        self.views[-1].setYRange(min, max)
        self.views[-1].setLabel('left', 'EEG Value for ', units='V')
        self.views[-1].setLabel('bottom', 'EEG Channel{}, Time'.format(i + 1), units='ms')
        self.view_plots.append(self.views[-1].plot(x, y, pen=(0,1)))

    def cal_content(self, start_time=-2000, end_time=2000, row=1):
        low = self.lowestGreaterThan(self.eeg_data[0, :], start_time)
        high = self.GreatestLowerThan(self.eeg_data[0, :], end_time)
        # limit the index in case out of array bound
        low = min(self.eeg_data.shape[1] - 1,max(0,low))
        high = max(0,min(self.eeg_data.shape[1] - 1, high))
        # print(start_time, end_time, self.eeg_data[0, low], self.eeg_data[0, high], low, high)
        return self.eeg_data[row,low:high + 1], self.eeg_data[0,low:high + 1]

    def updateData(self, time):
        self.time = time
        start_time = self.time - 2000
        end_time = self.time + 2000
        for i in range(len(self.views)):
            yd, xd = self.cal_content(start_time=start_time,end_time=end_time, row=i+1)
            self.views[i].setXRange(start_time, end_time)
            self.view_plots[i].setData(y=yd, x=xd)

    def update_channels(self, item):
        if item.checkState() == 0:
            self.removeObjFromView(item.index().row()-1)
        else:
            self.addView(0, len(self.views) * (self.graph_height + 5), item.index().row()-1)


    def removeObjFromView(self, objIndex):
        for i in range(len(self.view2ObjectIndex)-1,-1,-1):
            if self.view2ObjectIndex[i] == objIndex:
                self.graph_layout.removeWidget(self.views[i])
                sip.delete(self.views[i])
                self.views[i] = None
                self.view2ObjectIndex.pop(i)
                self.views.pop(i)
                self.view_plots.pop(i)
                break

    def addView(self, margin_x, margin_y, i):
        view = pyqtgraph.PlotWidget(self)
        self.graph_layout.addWidget(view)
        view.setGeometry(QtCore.QRect(margin_x, margin_y, self.graph_width, self.graph_height))
        self.views.append(view)
        self.view2ObjectIndex.append(i)
        if len(self.eeg_data) > 0:
            self.drawCurve(i)

    def addSelectArea(self, objects_num):
        self.model = QtGui.QStandardItemModel(objects_num + 1, 1)  # 5 rows, 2 col

        firstItem = QtGui.QStandardItem("---- Select area(s) ----")
        firstItem.setBackground(QtGui.QBrush(QtGui.QColor(200, 200, 200)))
        firstItem.setSelectable(False)
        self.model.setItem(0, 0, firstItem)

        for i in range(objects_num):
            item = QtGui.QStandardItem("Channel {}".format(i + 1))
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            if i < 3:
                item.setData(QtCore.Qt.Checked, QtCore.Qt.CheckStateRole)
            else:
                item.setData(QtCore.Qt.Unchecked,QtCore.Qt.CheckStateRole)
            self.model.setItem(i + 1, 0, item)
        self.model.itemChanged.connect(self.update_channels)
        self.addView(0, len(self.views) * (self.graph_height + 5), 0);
        self.addView(0, len(self.views) * (self.graph_height + 5), 1);
        self.addView(0, len(self.views) * (self.graph_height + 5), 2);
        self.combobox.setModel(self.model)

    def open_file(self, filename=None):
        home = str(Path.home())
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open EYE", home)
        if not filename:
            return
        self.eeg_data = np.loadtxt(str(filename), delimiter=",")[0:65, :]
        objects_num = self.eeg_data.shape[0] - 1
        # self.changeView(np.ones(3).tolist())
        self.addSelectArea(objects_num)
        self.positionSlider.setRange(0, self.eeg_data[0,-1])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = eegWidget()
    w.show()
    sys.exit(app.exec_())

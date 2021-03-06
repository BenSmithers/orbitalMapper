from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class Window(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.figure = plt.figure()
        self.ax = plt.axes()

        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, MainWindow)
        self.figurelayout = QtWidgets.QVBoxLayout()
        self.figurelayout.addWidget(self.toolbar)
        self.figurelayout.addWidget(self.canvas)
        self.horizontalLayout.addLayout(self.figurelayout)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.focusSelect = QtWidgets.QComboBox(self.centralwidget)
        self.focusSelect.setObjectName("focusSelect")
        self.verticalLayout.addWidget(self.focusSelect)
        self.zoomIn = QtWidgets.QPushButton(self.centralwidget)
        self.zoomIn.setObjectName("zoomIn")
        self.verticalLayout.addWidget(self.zoomIn)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.left = QtWidgets.QPushButton(self.centralwidget)
        self.left.setMaximumSize(QtCore.QSize(30, 30))
        self.left.setIconSize(QtCore.QSize(16, 16))
        self.left.setObjectName("left")
        self.horizontalLayout_2.addWidget(self.left)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.up = QtWidgets.QPushButton(self.centralwidget)
        self.up.setMaximumSize(QtCore.QSize(30, 30))
        self.up.setObjectName("up")
        self.verticalLayout_2.addWidget(self.up)
        self.down = QtWidgets.QPushButton(self.centralwidget)
        self.down.setMaximumSize(QtCore.QSize(30, 30))
        self.down.setObjectName("down")
        self.verticalLayout_2.addWidget(self.down)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.right = QtWidgets.QPushButton(self.centralwidget)
        self.right.setMaximumSize(QtCore.QSize(30, 30))
        self.right.setObjectName("right")
        self.horizontalLayout_2.addWidget(self.right)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.zoomOut = QtWidgets.QPushButton(self.centralwidget)
        self.zoomOut.setObjectName("zoomOut")
        self.verticalLayout.addWidget(self.zoomOut)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.zoomIn.setText(_translate("MainWindow", "+"))
        self.left.setText(_translate("MainWindow", "<"))
        self.up.setText(_translate("MainWindow", "^"))
        self.down.setText(_translate("MainWindow", "V"))
        self.right.setText(_translate("MainWindow", ">"))
        self.zoomOut.setText(_translate("MainWindow", "-"))



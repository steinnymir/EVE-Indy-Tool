# -*- coding: utf-8 -*-
"""
Created on Sun May 21 01:42:48 2017

@author: Steinn Ymir
"""

from . import indy, gfs
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
import qdarkstyle
import sys



class MainWindow(qw.QMainWindow):
    """ """
    def __init__(self):
        super().__init__()
        self.title = 'EVE Indy Tool'
        self.left = 300
        self.top = 100
        self.width = 300
        self.height = 400
        self.initUI()
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    def initUI(self):
        """ Generate GUI layout """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = qg.QGridLayout()

        self.central = BPcalc_GUI()
        layout.addWidget(self.central,0,0)
        self.setCentralWidget(self.central)
        self.show()



class BPcalc_GUI(qw.QWidget):
    """ """

    def __init__(self):
        super().__init__()
        self.makeLayout()
        self.sde = indy.SDE()


    def makeLayout(self):
        """ Generate the GUI layout """

        layout = qg.QGridLayout() # create a grid for subWidgets
        layout.setSpacing(10)
        self.setLayout(layout)

        font = qg.QFont()
        font.setBold(True)
        font.setPixelSize(15)
        font2 = qg.QFont()
        font.setPixelSize(12)

        self.initialize_sde_button = qw.QPushButton('Initialize SDE',self)
        self.initialize_sde_button.clicked.connect(self.initialize_SDE)
        self.blueprintID_textbox_label = qw.QLabel('Blueprint ID:', self)
        self.blueprintID_textbox_label.setFont(font)
        self.blueprintID_textbox = qw.QLineEdit(self)
        self.blueprintID_textbox.setPlaceholderText('000')
        #self.nameTxtbox.editingFinished.connect(self.calcBP)
        self.calculate_button = qw.QPushButton('Calculate!',self)
        self.calculate_button.clicked.connect(self.calculateBP)

        results_box_layout = qw.QVBoxLayout()
        self.results_box = qw.QGroupBox(self)
        self.results_box_label = qw.QLabel('Materials Required:', self)
        self.results_box_label.setFont(font2)


        layout.addWidget(self.blueprintID_textbox_label, 1,1)
        layout.addWidget(self.blueprintID_textbox, 2,1)
        layout.addWidget(self.initialize_sde_button, 1,1)
        layout.addWidget(self.calculate_button, 1,2)
        layout.addWidget(self.results_box_label, 1,1)
        layout.addWidget(self.results_box, 3,1,)

    def initialize_SDE(self):

        self.sde.importData('blueprints')

    def calculateBP(self):

        blueprintID = self.blueprintID_textbox.text()
        self.testbp = indy.Blueprint(blueprintID)
        self.testbp.fetchBpData()
        self.testbp.getMaterials()



    def showMaterialsList(self):
        pass


if __name__ == '__main__':

    app = qc.QCoreApplication.instance()
    if app is None:
        app = qg.QApplication(sys.argv)
    # Create handle prg for the Graphic Interface
    prg = MainWindow()
    prg.show()
    app.exec_()

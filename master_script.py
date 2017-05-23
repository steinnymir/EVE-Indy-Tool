# -*- coding: utf-8 -*-
"""
Created on Sat May 20 17:10:26 2017

@author: Steinn Ymir
"""
from library import indy, gfs, gui
from PyQt5 import QtGui as qg  # (the example applies equally well to PySide)
from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
import sys


def main():



#    timer = gfs.Timer()
#    timer.tic()
#
##    sde = SDE()
##    sde.import_indy_DB()
##    timer.tic()
#
#    testbp = indy.Blueprint(28675)
#    testbp.fetchBpData()
#
#    print(testbp.getMaterials(20))
#
#
#    timer.toc()

    launchGUI()

def launchGUI():
    ''' launch the gui '''
    app = qc.QCoreApplication.instance()
    if app is None:
        app = qw.QApplication(sys.argv)
    # Create handle prg for the Graphic Interface
    prg = gui.MainWindow()
    prg.show()
    app.exec_()


if __name__ == '__main__':
    main()
    #launch()
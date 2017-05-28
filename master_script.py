# -*- coding: utf-8 -*-
"""
Created on Sat May 20 17:10:26 2017

@author: Steinn Ymir
"""
from library import indy, gfs, gui, data
from PyQt5 import QtGui as qg  # (the example applies equally well to PySide)
from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
import sys
import os


def main():
    # timer = gfs.Timer()
    # timer.tic()
    #
    db = data.SDE()

    #
    # sde.import_quick()
    #
    # # sde.import_pickle('blueprints')
    # print(sde.blueprints[28675])
    # print(sde.invTypes[28675])
    # timer.toc_end()
    #
    # test_bp = indy.Blueprint(681, sde)
    # test_bp.printName()
    # test_bp.fetch_bp_data()
    # # print(test_bp.activities)
    # materials = test_bp.get_manufacturing_materials(out='name')
    # print(materials)

    project_path = os.path.dirname(os.path.realpath(__file__))
    newpath = os.path.dirname(project_path)
    newerpath = os.path.dirname(newpath)
    print(newerpath)


def launchGUI():
    """ launch the gui """
    app = qc.QCoreApplication.instance()
    if app is None:
        app = qw.QApplication(sys.argv)
    # Create handle prg for the Graphic Interface
    prg = gui.MainWindow()
    prg.show()
    app.exec_()


if __name__ == '__main__':


    main()
    # launchGUI()

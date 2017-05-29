# -*- coding: utf-8 -*-
"""
Created on Sat May 20 17:10:26 2017

@author: Steinn Ymir
"""
from library import gfs, gui, data
from library.indy import EVEItem, Blueprint
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
import sys
import os


def main():

    timer = gfs.Timer()
    timer.tic()

    db = data.SDE()
    db.import_quick()
    print('\n\n\n')

    name = 'enyo'

    ID = db.get_ID_from_name(name)

    item = EVEItem(ID, db)

    itemBPID = item.get_blueprintID()
    itemBP = Blueprint(itemBPID, db)
    item.printName()
    material_list = itemBP.manufacturing_materials
    print('Production Materials:')
    market = data.Market()
    totalcost = 0
    for ID in material_list:  # todo: implement as function, add category separation
        mat = EVEItem(int(ID), db)
        quantity = material_list[ID]
        cost = market.get_min_sellprice(mat.itemID) * quantity
        print('- {0} \t {1} \t {2}'.format(mat.name, quantity, cost))
        totalcost += cost

    print('total cost: ' + str(totalcost))
    print('parent bp: ' + str(itemBP.name))
    print(item.basePrice)
    market = data.Market()
    #market.update_marketData()
    cost = market.get_min_sellprice(item.itemID)
    print('{0} minimum cost is {1} ISK'.format(item.name,cost))


    timer.toc()
    #
    # project_path = os.path.dirname(os.path.realpath(__file__))
    # newpath = os.path.dirname(project_path)
    # newerpath = os.path.dirname(newpath)
    # print(newerpath)


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
    launchGUI()

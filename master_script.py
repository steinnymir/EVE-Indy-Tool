# -*- coding: utf-8 -*-
"""
Created on Sat May 20 17:10:26 2017

@author: Steinn Ymir
"""
from library import gfs, gui, data
from library.indy import Item, Blueprint, BPO
from library.gfs import roundup, Timer, isk
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
import sys
import os


def main():
    timer = Timer()
    timer.tic()

    item = 'capital construction parts'

    base_materials, production_list = manufacture(item)
    totprice = 0
    market_value = Item(item).price
    print('Shopping List:')
    for material, quantity in base_materials.items():
        mat = Item(material)
        price = mat.price * quantity
        print(str(mat.name).rjust(23), str(quantity).rjust(7), isk(mat.price), isk(price))
        totprice += price

    print('Production List:')
    for material, quantity in production_list.items():
        mat = Item(material)
        print(str(mat.name).rjust(20), isk(quantity))

    print('Market Value: ' + isk(market_value) + '  Production cost: ' + isk(totprice))
    print('gain: ' + isk(market_value - totprice))
    print('gain %: ' + str(round(((market_value - totprice)/market_value)*100,2)))

    print
    timer.toc()


def manufacture(product_IDorname):
    product = Item(product_IDorname)

    # if product.parent_blueprintID is None:
    #     # print(product.name,' has no bp')
    #     return None
    # else:
    product_blueprintID = product.parent_blueprintID
    product_bp = Blueprint(product_blueprintID)

    ME = 10
    stationBonus = 1
    rigBonus = 2 * 0
    effectiveME = (100 - ME - stationBonus - rigBonus) / 100
    raw_materials = product_bp.manufacturing_materials
    # product_bp.print_manufacturing_materials()
    base_materials = {}
    materials = {}
    for item in raw_materials:
        if Item(item).parent_blueprintID is None:
            base_materials[item] = roundup(raw_materials[item] * effectiveME)
        else:
            materials[item] = roundup(raw_materials[item] * effectiveME)

    for item, quantity in materials.items():
        base2, mat2 = manufacture(item)
        for baseitem, basequantity in base2.items():
            try:
                base_materials[baseitem] += basequantity*quantity
            except KeyError:
                base_materials[baseitem] = basequantity*quantity
        for matitem, matquantity in mat2.items():
            try:
                materials[matitem] += matquantity*quantity
            except KeyError:
                materials[matitem] = matquantity*quantity
    return base_materials, materials




    #
    # pop_list = []
    # children_materials = {}
    # for item in materials:
    #     matlist = manufacture(item)
    #     if type(matlist) == dict:
    #         for key in matlist:
    #             try:
    #                 children_materials[key] += matlist[key]
    #             except KeyError:
    #                 children_materials[key] = matlist[key]
    #         pop_list.append(item)
    #     else:
    #         pass
    # for item in children_materials:
    #     try:
    #         materials[item] += children_materials[item]
    #     except KeyError:
    #         materials[item] = children_materials[item]
    #
    # # for item in materials:
    # #     if item in pop_list:
    # #         pass
    # #     else:
    # #         final_materials[item] = materials[item]
    # return materials, pop_list


def basic_manufacturing():
    timer = gfs.Timer()
    timer.tic()

    db = data.SDE()
    db.import_quick()
    print('\n\n\n')

    name = 'Standup L-Set Advanced Component Manufacturing Efficiency I'
    name = 'widow'

    ID = db.get_ID_from_name(name)

    item = Item(ID, db)

    itemBPID = item.get_blueprintID()
    itemBP = Blueprint(itemBPID, db)
    item.printName()
    material_list = itemBP.manufacturing_materials
    print('Production Materials:')
    market = data.Market()
    totalcost = 0
    for ID in material_list:  # todo: implement as function, add category separation
        mat = Item(int(ID))
        quantity = material_list[ID]
        cost = market.get_min_sellprice(mat.itemID) * quantity
        print('- {0} \t {1} \t {2}'.format(mat.name, quantity, cost))
        totalcost += cost

    print('total cost: ' + str(totalcost))
    print('parent bp: ' + str(itemBP.name))
    print(item.basePrice)
    market = data.Market()
    # market.update_marketData()
    cost = market.get_min_sellprice(item.itemID)
    print('{0} minimum cost is {1} ISK'.format(item.name, cost))

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
    # launchGUI()

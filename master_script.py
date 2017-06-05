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

    item = 'crow'
    invent(item)

    timer.toc()
    timer.reset()


def invent(product_IDorname):  # todo: implement item or bp recognition

    product = Item(product_IDorname)
    product_blueprintID = product.parent_blueprintID
    product_bp = Blueprint(product_blueprintID)
    parent_invention_bpID = product_bp.inventionBP

    inventionBP = Blueprint(parent_invention_bpID)
    inv_probability = inventionBP.invention_probability
    inv_materials_raw = inventionBP.invention_materials
    inv_materials = {}
    tot_price = 0
    for key, value in inv_materials_raw.items():
        inv_materials[key] = value / inv_probability

    for items, quantity in inv_materials.items():
        item = Item(items)
        price = item.price * quantity
        print(item.name, quantity, isk(price))
        tot_price += price
        print(isk(tot_price))
    return inv_materials, tot_price


def TEMP_manufacture_item(item):
    """ get an item name as string and print material and production requirements, prices and gains
    :param item:
    :return:
    """
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
    print('gain %: ' + str(round(((market_value - totprice) / market_value) * 100, 2)))


def manufacture(product_IDorname, material_efficiency=0,  ):  # todo: implement item or bp recognition

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
        for base_item, base_quantity in base2.items():
            try:
                base_materials[base_item] += base_quantity * quantity
            except KeyError:
                base_materials[base_item] = base_quantity * quantity
        for mat_item, mat_quantity in mat2.items():
            try:
                materials[mat_item] += mat_quantity * quantity
            except KeyError:
                materials[mat_item] = mat_quantity * quantity

    return base_materials, materials


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

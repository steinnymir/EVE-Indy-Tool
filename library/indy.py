# -*- coding: utf-8 -*-
"""
Created on Sat May 20 17:02:12 2017

@author: Stymir
"""
from library import sde
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def main():
    # timer = gfs.Timer()
    # timer.tic()

    # test_bp = Blueprint(28675)
    # test_bp.printName()
    # test_bp.fetch_bp_data()
    # print(test_bp.get_manufacturing_materials(20))

    # sde = SDE()
    # sde.import_data('blueprints')
    # sde.export_pickle('blueprints')
    #
    # timer.toc()

    sde = sde.SDE()
    SDE.import_quick()
    bp = Blueprint(3529)
    print(bp.__dict__.keys())




class EVEItem(object):
    """ an object in new eden """

    def __init__(self, itemID, SDE):
        """ initialzie"""
        self.itemID = itemID
        self.itemName = '' # todo: make the id to name interpreter
        self.sde = SDE  # the full database
    # from typeIDs.p
        self.capacity = float
        self.description = str
        self.factionID = int
        self.graphicID = int
        self.groupID = int
        self.marketGroupID = int
        self.mass = int
        self.masteries = dict
        self.name = str
        self.portionSize = int
        self.published = bool
        self.raceID = int
        self.radius = float
        self.soundID = int
        self.traits = dict
        self.volume = float


        self.initialize_typeIDs()

    def printName(self):
        """ prints ItemID and item name"""
        print(self.itemName + ' has ID: ' + str(self.itemID))

    def initialize_typeIDs(self, sde=None):
        """ Fetch all data from typeIDs"""
        if sde is None:
            sde = self.sde
        self.capacity = float(sde.typeIDs[self.itemID]['itemName'])
        self.description = str(sde.typeIDs[self.itemID]['itemName'])
        self.factionID = int(sde.typeIDs[self.itemID]['itemName'])
        self.graphicID = int(sde.typeIDs[self.itemID]['itemName'])
        self.groupID = int(sde.typeIDs[self.itemID]['itemName'])
        self.marketGroupID = int(sde.typeIDs[self.itemID]['itemName'])
        self.mass = int(sde.typeIDs[self.itemID]['itemName'])
        self.masteries = dict(sde.typeIDs[self.itemID]['itemName'])
        self.name = str(sde.typeIDs[self.itemID]['itemName'])
        self.portionSize = int(sde.typeIDs[self.itemID]['itemName'])
        self.published = bool(sde.typeIDs[self.itemID]['itemName'])
        self.raceID = int(sde.typeIDs[self.itemID]['itemName'])
        self.radius = float(sde.typeIDs[self.itemID]['itemName'])
        self.soundID = int(sde.typeIDs[self.itemID]['itemName'])
        self.traits = dict(sde.typeIDs[self.itemID]['itemName'])
        self.volume = float(sde.typeIDs[self.itemID]['itemName'])


class Blueprint(EVEItem):  # todo: fix import of SDE in EVEitem and Blueprint
    """ a blueprint class """

    def __init__(self, blueprintID, SDE):
        """ """
        super(Blueprint, self).__init__(blueprintID, SDE)
        self.bpID = blueprintID
        self.activities = {'copying', 'manufacturing', 'research_material', 'research_time'}
        self.blueprintTypeID = blueprintID
        self.maxProductionLimit = 0
        self.product = 0
        self.product_quantity = 0
        # from blueprints.p
        self.copying_materials = dict
        self.copying_skills = dict
        self.copying_time = int
        self.invention_materials = dict
        self.invention_products_probability = float
        self.invention_products = dict
        self.manufacturing_materials = dict
        self.manufacturing_products = dict
        self.manufacturing_skills = dict
        self.manufacturing_time = int
        self.research_material_materials = dict
        self.research_material_skills = dict
        self.research_material_time = int
        self.research_time_materials = dict
        self.research_time_skills = dict
        self.research_time_time = int
        self.blueprintTypeID = int
        self.maxProductionLimit = int


    def initialize_BP(self, sde=None):
        """ initializes all BP related attributes"""
        if sde is None:
            sde = self.sde
        self.copying_materials = dict
        self.copying_skills = dict
        self.copying_time = int
        self.invention_materials = dict
        self.invention_products_probability = float
        self.invention_products = dict
        self.manufacturing_materials = dict
        self.manufacturing_products = dict
        self.manufacturing_skills = dict
        self.manufacturing_time = int
        self.research_material_materials = dict
        self.research_material_skills = dict
        self.research_material_time = int
        self.research_time_materials = dict
        self.research_time_skills = dict
        self.research_time_time = int
        self.blueprintTypeID = int
        self.maxProductionLimit = int







    def fetch_bp_data(self):
        """ load info from SDE """
        # if sde == None:
        #     sde = SDE()
        #     print('Loading Blueprints to SDE')
        #     sde.import_pickle('blueprints')
        try:
            bpDict = SDE.blueprints[self.bpID]
        except KeyError:
            print('invalid BP ID')

        for key in bpDict:
            setattr(self, key, bpDict[key])

        self.product = self.activities['manufacturing']['products'][0]['typeID']
        self.product_quantity = self.activities['manufacturing']['products'][0]['quantity']

    def get_manufacturing_materials(self, runs=1, out='ID'):
        """ returns materials required for n runs"""
        requirement_list = self.activities['manufacturing']['materials']
        requirement_dict = {}
        for item in requirement_list:
            quantity = item['quantity'] * runs
            if out == 'ID':
                requirement_dict[item['typeID']] = [quantity]
            elif out == 'name':
                name = SDE.invTypes[item['typeID']]['typeName']
                requirement_dict[name] = quantity
        return requirement_dict




# %% Database Management



if __name__ == '__main__':
    main()

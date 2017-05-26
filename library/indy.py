# -*- coding: utf-8 -*-
"""
Created on Sat May 20 17:02:12 2017

@author: Stymir
"""
from library import sde, gfs
import pprint

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def main():
    timer = gfs.Timer()
    timer.tic()

    # test_bp = Blueprint(28675)
    # test_bp.printName()
    # test_bp.fetch_bp_data()
    # print(test_bp.get_manufacturing_materials(20))

    # sde = SDE()
    # sde.import_data('blueprints')
    # sde.export_pickle('blueprints')
    #
    # timer.toc()

    db = sde.SDE()
    db.import_quick()

    itemList = [30245,30329,30244,34,15686,13004]
    materials = []
    value = 0
    for item in itemList:
        bp = Blueprint(item,db)
        bp.printName()
        if bp.basePrice is not None:
            value += bp.basePrice
        materials.append(bp.manufacturing_materials)
    print(value)
        # print(bp.manufacturing_materials)

    timer.toc()
    # timer.reset()
    # timer.tic()
    #
    # for item in itemList:
    #     bp = Blueprint(30245)
    #     # bp.printName()
    #     # print(bp.manufacturing_materials)
    #
    # timer.toc()

class EVEItem(object):
    """ an object in new eden """

    def __init__(self, itemID, SDE=None):
        """ initialzie"""
        self.itemID = itemID
        self.itemName = None
        self._sde = SDE  # the full database

        self.attr_list = []
        self.typeIDs_attr_list = ['basePrice', 'marketGroupID', 'capacity', 'description',
                                  'factionID', 'graphicID', 'groupID', 'mass', 'masteries', 'name', 'portionSize',
                                  'published', 'raceID', 'radius', 'soundID', 'traits', 'volume']
        self._typeIDs_attr_list_types = {'float': ['basePrice', 'capacity', 'radius', 'volume'],
                                         'int': ['marketGroupID', 'factionID', 'graphicID', 'groupID', 'marketGroupID',
                                                 'mass', 'portionSize', 'raceID', 'soundID'],
                                         'dict': ['description', 'masteries', 'name', 'traits'],
                                         'bool': ['published']
                                         }
        # from typeIDs.p
        self.basePrice = None
        self.marketGroupID = None
        self.capacity = None
        self.description = None
        self.factionID = None
        self.graphicID = None
        self.groupID = None
        self.marketGroupID = None
        self.mass = None
        self.masteries = None
        self.name = None
        self.portionSize = None
        self.published = None
        self.raceID = None
        self.radius = None
        self.soundID = None
        self.traits = None
        self.volume = None

        self.initialize_typeIDs()

    def printName(self):
        """ prints ItemID and item name"""
        print(self.name + ' has ID: ' + str(self.itemID))

    def initialize_typeIDs(self):
        """ Fetch all data from typeIDs"""

        if self._sde is None:
            print('WARNING: SDE manually imported for each item. Heavy computation time required.')
            self._sde = sde.SDE()
            self._sde.import_quick()

        for key in self._typeIDs_attr_list_types:
            for attribute in self._typeIDs_attr_list_types[key]:
                try:
                    value = self._sde.typeIDs[self.itemID][attribute]
                    if key == 'int':
                        value = int(value)
                    elif key == 'dict':
                        try:
                            value = str(value['en'])
                        except KeyError:
                            value = dict(value)
                    elif key == 'float':
                        value = float(value)
                    elif key == 'bool':
                        value = bool(value)
                    setattr(self, attribute, value)
                except KeyError:
                    pass





                    # self.basePrice = float(sde.typeIDs[self.itemID]['capacity'])
                # self.marketGroupID = int(sde.typeIDs[self.itemID]['capacity'])
                #
                # self.capacity = float(sde.typeIDs[self.itemID]['capacity'])
                # self.description = str(sde.typeIDs[self.itemID]['description'])
                # self.factionID = int(sde.typeIDs[self.itemID]['factionID'])
                # self.graphicID = int(sde.typeIDs[self.itemID]['graphicID'])
                # self.groupID = int(sde.typeIDs[self.itemID]['groupID'])
                # self.marketGroupID = int(sde.typeIDs[self.itemID]['marketGroupID'])
                # self.mass = int(sde.typeIDs[self.itemID]['mass'])
                # self.masteries = dict(sde.typeIDs[self.itemID]['masteries'])
                # self.name = str(sde.typeIDs[self.itemID]['name'])
                # self.portionSize = int(sde.typeIDs[self.itemID]['portionSize'])
                # self.published = bool(sde.typeIDs[self.itemID]['published'])
                # self.raceID = int(sde.typeIDs[self.itemID]['raceID'])
                # self.radius = float(sde.typeIDs[self.itemID]['radius'])
                # self.soundID = int(sde.typeIDs[self.itemID]['soundID'])
                # self.traits = dict(sde.typeIDs[self.itemID]['traits'])
                # self.volume = float(sde.typeIDs[self.itemID]['volume'])


class Blueprint(EVEItem):
    """ a blueprint class """

    def __init__(self, blueprintID, SDE=None):  # todo: fix import of SDE in EVEitem and Blueprint
        """ """
        super(Blueprint, self).__init__(blueprintID, SDE)
        # self.activities = {'copying', 'manufacturing', 'research_material', 'research_time'}
        # self.blueprintTypeID = blueprintID
        # self.maxProductionLimit = 0
        # self.product = 0
        # self.product_quantity = 0
        # from blueprints.p

        self.blueprints_attr_list = ['copying_materials',
                                     'copying_skills', 'copying_time', 'invention_materials',
                                     # 'invention_products_probability',
                                     'invention_products', 'invention_time', 'manufacturing_materials',
                                     'manufacturing_products', 'manufacturing_skills', 'manufacturing_time',
                                     'research_material_materials', 'research_material_skills',
                                     'research_material_time',
                                     'research_time_materials', 'research_time_skills', 'research_time_time',
                                     'blueprintTypeID', 'maxProductionLimit']

        self.copying_materials = None
        self.copying_skills = None
        self.copying_time = None
        self.invention_materials = None
        # self.invention_products_probability = None
        self.invention_products = None
        self.invention_time = None
        self.manufacturing_materials = None
        self.manufacturing_products = None
        self.manufacturing_skills = None
        self.manufacturing_time = None
        self.research_material_materials = None
        self.research_material_skills = None
        self.research_material_time = None
        self.research_time_materials = None
        self.research_time_skills = None
        self.research_time_time = None
        self.blueprintTypeID = None
        self.maxProductionLimit = None

        self.initialize_BP()

    def initialize_BP(self, sde=None):
        """ initializes all BP related attributes"""
        if sde is None:
            sde = self._sde

        # for attribute in self.blueprints_attr_list:
        #     setattr(self,attribute,)
        try:
            self.copying_materials = dict(sde.blueprints[self.itemID]['activities']['copying']['materials'][0])
            self.copying_skills = dict(sde.blueprints[self.itemID]['activities']['copying']['skills'][0])
            self.copying_time = int(sde.blueprints[self.itemID]['activities']['copying']['time'])
        except KeyError:
            pass
        try:
            self.invention_materials = dict(sde.blueprints[self.itemID]['activities']['invention']['materials'][0])
            # self.invention_products_probability = float(sde.blueprints[self.itemID]['activities']['invention']['products'])
            self.invention_products = dict(sde.blueprints[self.itemID]['activities']['invention']['products'][0])
            self.invention_time = int(sde.blueprints[self.itemID]['activities']['invention']['time'])
        except KeyError:
            pass
        try:
            self.manufacturing_materials = dict(sde.blueprints[self.itemID]['activities']['manufacturing']['materials'][0])
            self.manufacturing_products = dict(sde.blueprints[self.itemID]['activities']['manufacturing']['products'][0])
            self.manufacturing_skills = dict(sde.blueprints[self.itemID]['activities']['manufacturing']['skills'][0])
            self.manufacturing_time = int(sde.blueprints[self.itemID]['activities']['manufacturing']['time'])
        except KeyError:
            pass
        try:
            self.research_material_materials = dict(sde.blueprints[self.itemID]['research_material']['materials'][0])
            self.research_material_skills = dict(sde.blueprints[self.itemID]['research_material']['skills'][0])
            self.research_material_time = int(sde.blueprints[self.itemID]['research_material']['time'])
        except KeyError:
            pass
        try:
            self.research_time_materials = dict(sde.blueprints[self.itemID]['research_time']['materials'][0])
            self.research_time_skills = dict(sde.blueprints[self.itemID]['research_time']['skills'][0])
            self.research_time_time = int(sde.blueprints[self.itemID]['research_time']['time'])
        except KeyError:
            pass
        try:
            self.blueprintTypeID = int(sde.blueprints[self.itemID]['blueprintTypeID'])
            self.maxProductionLimit = int(sde.blueprints[self.itemID]['maxProductionLimit'])
        except KeyError:
            pass

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

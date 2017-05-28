# -*- coding: utf-8 -*-
"""
Created on Sat May 20 17:02:12 2017

@author: Stymir
"""
from library import data, gfs

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def main():

    timer = gfs.Timer()
    timer.tic()

    db = data.SDE()
    db.import_quick()
    print('\n\n\n')

    name = 'condor'

    ID = db.get_ID_from_name(name)
    item = EVEItem(ID, db)
    print(ID)
    itemBP = item.get_parent_blueprint()
    print('parent bp: ' + str(itemBP))

    item.printName()
    print(item.basePrice)

    timer.toc()


class MassProduction(object):
    """ class for managing multiple items, in production, invention or whatever """

    def __init__(self):
        """ init attributes"""
        self.materials_list = {}

    def get_manufacturing_materials_list(self, itemList):  # todo: make me
        """ calculate list of required materials from a list of bpIDs.
        :type itemList: list of itemIDs of blueprints.
        :return materials_dict:
        """

        for item in itemList:
            bp = Blueprint(item, db)
            bp.printName()
            try:  # check whether itemID is a blueprint with material requirement for manufacturing
                for key in bp.manufacturing_materials:
                    quantity = bp.manufacturing_materials[key]
                    try:
                        self.materials_list[key] += quantity
                    except KeyError:  # if key (material) not present yet, create it
                        self.materials_list[key] = quantity
            except TypeError:
                pass


class EVEItem(object):
    """ an object in new eden """

    def __init__(self, itemID, SDE=None):
        """ initialzie"""
        self.itemID = itemID
        self.itemName = None
        self.sde = SDE  # the full database

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

        if self.sde is None:
            print('WARNING: SDE manually imported for each item. Heavy computation time required.')
            self.sde = data.SDE()
            self.sde.import_quick()

        for key in self._typeIDs_attr_list_types:
            for attribute in self._typeIDs_attr_list_types[key]:
                try:
                    value = self.sde.typeIDs[self.itemID][attribute]
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

    def get_parent_blueprint(self):
        """ :returns itemID of blueprint that would produce this item"""
        return self.sde.get_parent_blueprint(self.itemID)


class Blueprint(EVEItem):
    """ a blueprint class """

    def __init__(self, blueprintID, SDE=None):
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
                                     'invention_probability',
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
        self.invention_probability = None
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
            sde = self.sde

        try:  # --------------  copying  --------------
            self.copying_materials = self.translate_to_dict(
                requirement_list=sde.blueprints[self.itemID]['activities']['copying']['materials'],
                key_label='typeID',
                quantity_label='quantity')

            self.copying_skills = self.translate_to_dict(
                requirement_list=sde.blueprints[self.itemID]['activities']['copying']['skills'],
                key_label='typeID',
                quantity_label='level')

            self.copying_time = int(sde.blueprints[self.itemID]['activities']['copying']['time'])

        except KeyError:
            pass

        try:  # --------------  invention  --------------
            self.invention_materials = self.translate_to_dict(
                requirement_list=sde.blueprints[self.itemID]['activities']['invention']['materials'],
                key_label='typeID',
                quantity_label='quantity')
            self.invention_products, self.invention_probability = self.translate_to_dict(
                requirement_list=sde.blueprints[self.itemID]['activities']['invention']['products'],
                key_label='typeID',
                quantity_label='quantity',
                is_invention=True)
            self.invention_time = int(sde.blueprints[self.itemID]['activities']['invention']['time'])
        except KeyError:
            print()

        try:  # --------------  manufacturing  --------------
            self.manufacturing_materials = self.translate_to_dict(
                requirement_list=sde.blueprints[self.itemID]['activities']['manufacturing']['materials'],
                key_label='typeID',
                quantity_label='quantity')
            self.manufacturing_products = self.translate_to_dict(
                requirement_list=sde.blueprints[self.itemID]['activities']['manufacturing']['products'],
                key_label='typeID',
                quantity_label='quantity')
            self.manufacturing_skills = self.translate_to_dict(
                requirement_list=sde.blueprints[self.itemID]['activities']['manufacturing']['skills'],
                key_label='typeID',
                quantity_label='level')
            self.manufacturing_time = int(sde.blueprints[self.itemID]['activities']['manufacturing']['time'])
        except KeyError:
            pass

        try:  # --------------  research material  --------------
            self.research_material_materials = self.translate_to_dict(
                requirement_list=sde.blueprints[self.itemID]['research_material']['materials'],
                key_label='typeID',
                quantity_label='quantity')
            self.research_material_skills = self.translate_to_dict(
                requirement_list=sde.blueprints[self.itemID]['research_material']['skills'],
                key_label='typeID',
                quantity_label='level')
            self.research_material_time = int(sde.blueprints[self.itemID]['research_material']['time'])
        except KeyError:
            pass

        try:  # --------------  research time  --------------
            self.research_time_materials = self.translate_to_dict(
                requirement_list=sde.blueprints[self.itemID]['research_time']['materials'],
                key_label='typeID',
                quantity_label='quantity')

            self.research_time_skills = self.research_material_skills = self.translate_to_dict(
                requirement_list=sde.blueprints[self.itemID]['research_time']['skills'],
                key_label='typeID',
                quantity_label='level')

            self.research_time_time = int(sde.blueprints[self.itemID]['research_time']['time'])
        except KeyError:
            pass

        try:  # --------------  other  --------------
            self.blueprintTypeID = int(sde.blueprints[self.itemID]['blueprintTypeID'])
            self.maxProductionLimit = int(sde.blueprints[self.itemID]['maxProductionLimit'])
        except KeyError:
            pass

    def translate_to_dict(self, requirement_list, key_label, quantity_label, is_invention=False):
        """ returns a dictionary with a more usable structure than what offered by sde.
        if is_invention is true returns also a float for invention probability"""
        requirement_dict = {}
        probability = 0.0
        for item in requirement_list:
            requirement_dict[item[key_label]] = item[quantity_label]
            # if it is an invention bp, return also probability
            if is_invention:
                probability = float(item['probability'])
            return requirement_dict, probability
        else:
            return requirement_dict


if __name__ == '__main__':
    main()

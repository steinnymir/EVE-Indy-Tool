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

    name = 'Standup L-Set Advanced Component Manufacturing Efficiency I'

    # ID = db.get_ID_from_name(name)
    item = EVEItem(name)
    print(item.name)
    itemBPID = item.get_blueprintID()
    itemBP = Blueprint(itemBPID)
    print('\nMaterials List:\n')
    for name, quantity in itemBP.manufacturing_materials.items():
        print('{0}  {1}'.format(EVEItem(name).name,quantity))
    print()
    item.printName()
    print('parent bp: ' + str(itemBP.name))

    print('{0} minimum cost is {1} ISK'.format(item.name,item.price))
    print(item.categoryName)
    print(item.groupName)


    timer.toc()


class Indy(object):
    """ wrapper class to give data to all EVEItem, Blueprints etc instances"""
    sde = data.SDE()
    market = data.Market()
    api = data.API()
    def __init__(self):
        """ nothing to initialize"""

    def refresh_database(self):
        self.sde.reload_all()
        self.api.update_All()
        self.market.update_marketData()

class Character(Indy):
    """ """
    def __init__(self):
        """ """
        self.name
        self.skills = {}

    def get_skills(self):
        """ """

class AssemblyLine(Indy):
    """ the object which does all industry stuff: manufacture, invention etc"""
    def __init__(self, assemblyLine):
        super.__init__()
        """ """


        self.assemblyLineTypeID = None
        self.assemblyLineTypeName = None
        #from ramAssemblyLineTypes
        self.activityID = None
        self.baseCostMultiplier = None
        self.baseMaterialMultiplier = None
        self.baseTimeMultiplier = None
        self.description = None
        self.volume = None
        self.categoryIDmultipliers = None
        self.groupIDmultipliers = None

    def initialize_multipliers(self):
        """ init groupID and categoryID based multipliers"""

        for key in self.sde.ramAssemblyLineTypeDetailPerCategory:
            if self.sde.ramAssemblyLineTypeDetailPerCategory[key][assemblyLineTypeID] == self.assemblyLineTypeID:
                self.categoryIDmultipliers = self.sde.ramAssemblyLineTypeDetailPerCategory[key]

        for key in self.sde.ramAssemblyLineTypeDetailPerGroup:
            if self.sde.ramAssemblyLineTypeDetailPerGroup[key][assemblyLineTypeID] == self.assemblyLineTypeID:
                self.groupIDmultipliers = self.sde.ramAssemblyLineTypeDetailPerGroup[key]

    def append_blueprint(self, bpID):

        self.blueprints[bpID] = { 'obj':Blueprint(bpID), 'quantity':number}


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


class EVEItem(Indy):
    """ an object in new eden """


    def __init__(self, item):
        """ initialzie"""
        if type(item) is str:  # allows for initialization with name or ID (str) or ID (int)
            try:  # try ID int
                self.itemID = int(item)
            except ValueError: #  if not a number: its a name!
                self.itemID = self.sde.get_ID_from_name(item)
        elif type(item) is int:
            self.itemID = item
        else:
            print('Invalid item name or ID')

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
        #from groupIDs
        self.categoryID = None
        self.fittableNonSingleton = None
        self.iconID = None
        self.groupName = None
        #from categoryIDs
        self.categoryName = None
        self.categoriIconID = None
        self.price = self.market.get_min_sellprice(self.itemID)

        self.blueprintID = self.sde.get_parent_blueprintID(self.itemID)


        self.initialize_typeIDs()
        self.initialize_groupIDs()
        self.initialize_categoryIDs()

    def refresh(self):
        """ re-initialize item"""
        self.__init__()

    def initialize_price(self):
        """ get price from current market"""
        self.price = self.market.get_min_sellprice(self.itemID)

    def printName(self):
        """ prints ItemID and item name"""
        print(self.name + ' has ID: ' + str(self.itemID))

    def initialize_typeIDs(self):
        """ Fetch all data from typeIDs"""

        # if self.sde is None:
        #     print('WARNING: SDE manually imported for each item. Heavy computation time required.')
        #     self.sde = data.SDE()

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

    def initialize_groupIDs(self):
        """ """
        self.categoryID = self.sde.groupIDs[self.groupID]['categoryID']
        self.fittableNonSingleton = self.sde.groupIDs[self.groupID]['fittableNonSingleton']
        try:
            self.iconID = self.sde.groupIDs[self.groupID]['iconID']
        except KeyError:
            pass
        self.groupName = self.sde.groupIDs[self.groupID]['name']['en']

    def initialize_categoryIDs(self):
        """" """
        self.categoryName = self.sde.categoryIDs[self.categoryID]['name']['en']
        try:
            self.categoriIconID = self.sde.groupIDs[self.categoryID]['iconID']
        except KeyError:
            pass



class Blueprint(EVEItem):
    """ a blueprint class """



    def __init__(self, blueprintID):
        """ """
        super(Blueprint, self).__init__(blueprintID)

        self.blueprints_attr_list = ['copying_materials',
                                     'copying_skills', 'copying_time', 'invention_materials',
                                     'invention_probability',
                                     'invention_products', 'invention_time', 'manufacturing_materials',
                                     'manufacturing_products', 'manufacturing_skills', 'manufacturing_time',
                                     'research_material_materials', 'research_material_skills',
                                     'research_material_time',
                                     'research_time_materials', 'research_time_skills', 'research_time_time',
                                     'blueprintTypeID', 'maxProductionLimit']

        self.blueprintID = self.itemID
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

        self.inventionBP = self.sde.get_parent_invention_blueprintID(self.itemID)

        self.initialize_BP()

    def initialize_BP(self):
        """ initializes all BP related attributes"""

        try:  # --------------  copying  --------------
            self.copying_materials = self.translate_to_dict(
                requirement_list= self.sde.blueprints[self.itemID]['activities']['copying']['materials'],
                key_label='typeID',
                quantity_label='quantity')

            self.copying_skills = self.translate_to_dict(
                requirement_list= self.sde.blueprints[self.itemID]['activities']['copying']['skills'],
                key_label='typeID',
                quantity_label='level')

            self.copying_time = int(self.sde.blueprints[self.itemID]['activities']['copying']['time'])

        except KeyError:
            pass

        try:  # --------------  invention  --------------
            self.invention_materials = self.translate_to_dict(
                requirement_list=self.sde.blueprints[self.itemID]['activities']['invention']['materials'],
                key_label='typeID',
                quantity_label='quantity')
            self.invention_products, self.invention_probability = self.translate_to_dict(
                requirement_list=self.sde.blueprints[self.itemID]['activities']['invention']['products'],
                key_label='typeID',
                quantity_label='quantity',
                is_invention=True)
            self.invention_time = int(self.sde.blueprints[self.itemID]['activities']['invention']['time'])
        except KeyError:
            print()

        try:  # --------------  manufacturing  --------------
            self.manufacturing_materials = self.translate_to_dict(
                requirement_list=self.sde.blueprints[self.itemID]['activities']['manufacturing']['materials'],
                key_label='typeID',
                quantity_label='quantity')
            self.manufacturing_products = self.translate_to_dict(
                requirement_list=self.sde.blueprints[self.itemID]['activities']['manufacturing']['products'],
                key_label='typeID',
                quantity_label='quantity')
            self.manufacturing_skills = self.translate_to_dict(
                requirement_list=self.sde.blueprints[self.itemID]['activities']['manufacturing']['skills'],
                key_label='typeID',
                quantity_label='level')
            self.manufacturing_time = int(self.sde.blueprints[self.itemID]['activities']['manufacturing']['time'])
        except KeyError:
            pass

        try:  # --------------  research material  --------------
            self.research_material_materials = self.translate_to_dict(
                requirement_list=self.sde.blueprints[self.itemID]['research_material']['materials'],
                key_label='typeID',
                quantity_label='quantity')
            self.research_material_skills = self.translate_to_dict(
                requirement_list=self.sde.blueprints[self.itemID]['research_material']['skills'],
                key_label='typeID',
                quantity_label='level')
            self.research_material_time = int(self.sde.blueprints[self.itemID]['research_material']['time'])
        except KeyError:
            pass

        try:  # --------------  research time  --------------
            self.research_time_materials = self.translate_to_dict(
                requirement_list=self.sde.blueprints[self.itemID]['research_time']['materials'],
                key_label='typeID',
                quantity_label='quantity')

            self.research_time_skills = self.research_material_skills = self.translate_to_dict(
                requirement_list=self.sde.blueprints[self.itemID]['research_time']['skills'],
                key_label='typeID',
                quantity_label='level')

            self.research_time_time = int(self.sde.blueprints[self.itemID]['research_time']['time'])
        except KeyError:
            pass

        try:  # --------------  other  --------------
            self.blueprintTypeID = int(self.sde.blueprints[self.itemID]['blueprintTypeID'])
            self.maxProductionLimit = int(self.sde.blueprints[self.itemID]['maxProductionLimit'])
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

        if is_invention:
            return requirement_dict, probability
        else:
            return requirement_dict

    def get_invention_parent_bp(self): # todo: make this function


    def print_manufacturing_materials(self):
        """ prints the shopping list!"""
        print('\nMaterials List:\n')
        for name, quantity in self.manufacturing_materials.items():
            print('{0}  {1}'.format(EVEItem(name).name, quantity))

if __name__ == '__main__':
    main()

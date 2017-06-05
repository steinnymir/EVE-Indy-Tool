# -*- coding: utf-8 -*-
"""
Created on Sat May 20 17:02:12 2017

@author: Stymir
"""
from library import data, gfs
import os

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def main():
    timer = gfs.Timer()
    timer.tic()

    bpName = 'Enyo'
    bp = Blueprint(Item('Enyo').parent_blueprintID)

    bpc = BPC(bp.blueprintID,runs=4,ME=10,TE=20)
    station = Station(station_class='Azbel',system_class='HighSec')
    print(station.get_material_efficiency(bpc))


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


class Station(Indy):
    """ """

    def __init__(self, station_class, system_class='HighSec'):
        super(Station, self).__init__()

        self.station_typeID = None
        self.station_class = station_class

        if self.station_class == 'Azbel':
            self.ME_bonus = 0.01
            self.TE_bonus = 0.2
            self.cost_bonus = 0.04
        elif self.station_class == 'Raitaru':
            self.ME_bonus = 0.01
            self.TE_bonus = 0.15
            self.cost_bonus = 0.03
        elif self.station_class == 'Sotiyo':
            self.ME_bonus = 0.01
            self.TE_bonus = 0.3
            self.cost_bonus = 0.05

        if system_class == 'HighSec':
            self.system_mod = 1
        elif system_class == 'LowSec':
            self.system_mod = 1.9
        elif system_class == 'NullSec':
            self.system_mod = 2.1

        self.fuel_consumption_bonus = 0.25
        # self.init_station_bonuses()

        self.rigs_bonus = {
            'Advanced Component': {'ME': False, 'TE': False},
            'Advanced Large Ship': {'ME': False, 'TE': False},
            'Advanced Medium Ship': {'ME': False, 'TE': False},
            'Advanced Small Ship': {'ME': True, 'TE': False},
            'Ammunition': {'ME': False, 'TE': False},
            'Basic Capital Component': {'ME': False, 'TE': False},
            'Basic Large Ship': {'ME': False, 'TE': False},
            'Basic Medium Ship': {'ME': False, 'TE': False},
            'Basic Small Ship': {'ME': False, 'TE': False},
            'Blueprint Copy': {'ME': False, 'TE': False},
            'Capital Ship': {'ME': False, 'TE': False},
            'Drone and Fighter': {'ME': False, 'TE': False},
            'Equipment': {'ME': False, 'TE': False},
            'Invention': {'ME': False, 'TE': False},
            'ME Research': {'ME': False, 'TE': False},
            'Structure': {'ME': False, 'TE': False},
            'TE research': {'ME': False, 'TE': False},
        }

        self.rigs_bonus_categories = {}
        self.rigs_bonus_groups = {  # todo: correct this shit, add implementation for med and large ships
            'Advanced Component': ('Construction Components', 'Tools'),
            'Advanced Large Ship': ('Black Ops', 'Elite Battleship', 'Marauders' 'Jump Freighter'),
            'Advanced Medium Ship': ('Strategic Cruiser',
                                     'Attack Battlecruiser',
                                     'Combat Battlecruiser',
                                     'Combat Recon Ship',
                                     'Force Recon Ship',
                                     'Heavy Assault Ship',
                                     'Heavy Interdictors',
                                     'Logistics',
                                     'Command Ship',
                                     'Transport Ship',
                                     'Blockade Runner'),
            'Advanced Small Ship': ('Assault Ship',
                                    'Covert Ops',
                                    'Electronic Attack Ship',
                                    'Interceptor',
                                    'Stealth Bomber',
                                    'Assault Frigate',
                                    'Exhumer',
                                    'Interdictor'
                                    'Command Destroyer'),
            'Ammunition': ('', ','''),
            'Basic Capital Component': (),
            'Basic Large Ship': ('Battleship'),
            'Basic Medium Ship': ('Cruiser',
                                  'Battlecruiser',
                                  'Industrial'),
            'Basic Small Ship': ('Frigate',
                                 'Destroyer',
                                 'Mining Barge'),
            'Blueprint Copy': (),
            'Capital Ship': (),
            'Drone and Fighter': (),
            'Equipment': (),
            'Invention': (),
            'ME Research': (),
            'Structure': (),
            'TE research': (),
        }


    def init_station_bonuses(self):
        """ depending on station name, set the right bonuses"""
        if self.station_class == 'Azbel':
            self.ME_bonus = 0.01
            self.TE_bonus = 0.2
            self.cost_bonus = 0.04
        elif self.station_class == 'Raitaru':
            self.ME_bonus = 0.01
            self.TE_bonus = 0.15
            self.cost_bonus = 0.03
        elif self.station_class == 'Sotiyo':
            self.ME_bonus = 0.01
            self.TE_bonus = 0.3
            self.cost_bonus = 0.05
        else:
            raise TypeError('{} is not an Engineering Complex'.format(self.station_class))

    def get_material_efficiency(self, blueprint):
        """
        get the material efficiency of the given blueprint in this station, with its assembly lines.
        calculated as (1-base_ME) * (1-rig_ME_bonus) *(1 - station_ME_bonus) * (1 - skill_ME_bonus)
        :blueprint: BPO or BPC
            blueprint copy or original
        :return: float
            effective material efficiency: multiplier for materials.
        """
        if isinstance(blueprint, BPC):
            base_ME = blueprint.ME
            base_TE = blueprint.TE
            # fetch name of first manufacturing product
            prod_dict = blueprint.manufacturing_products
            for key in prod_dict:
                product = Item(key)
            # product = Item(list(blueprint.manufacturing_products.keys())[0])

            rig_ME_bonus = 0
            rig_TE_bonus = 0
            print(product.categoryName, product.groupName)

            if product.categoryName == 'Charge':
                if self.rigs_bonus['Ammunition']['ME']:
                    rig_ME_bonus = 0.02
                if self.rigs_bonus['Ammunition']['TE']:
                    rig_TE_bonus = 0.2
            elif product.categoryName == 'Drone':
                if self.rigs_bonus['Drone and Fighter']['ME']:
                    rig_ME_bonus = 0.02
                if self.rigs_bonus['Drone and Fighter']['TE']:
                    rig_TE_bonus = 0.2
            elif product.categoryName == 'Ship':  # todo: make difference between small med and large ships
                print('true')
                if product.metaGroupID == 2:
                    if self.rigs_bonus['Advanced Small Ship']['ME']:
                        rig_ME_bonus = 0.02
                    if self.rigs_bonus['Advanced Small Ship']['TE']:
                        rig_TE_bonus = 0.2
                else:
                    if self.rigs_bonus['Basic Small Ship']['ME']:
                        rig_ME_bonus = 0.02
                    if self.rigs_bonus['Basic Small Ship']['TE']:
                        rig_TE_bonus = 0.2
            elif product.categoryName == 'Module':
                if self.rigs_bonus['Equipment']['ME']:
                    rig_ME_bonus = 0.02
                if self.rigs_bonus['Equipment']['TE']:
                    rig_TE_bonus = 0.2
            elif product.categoryName == 'Commodity':
                if blueprint.groupName == 'Capital Construction Part':
                    if self.rigs_bonus['Basic Capital Component']['ME']:
                        rig_ME_bonus = 0.02
                    if self.rigs_bonus['Basic Capital Component']['TE']:
                        rig_TE_bonus = 0.2
                else:
                    if self.rigs_bonus['Advanced Component']['ME']:
                        rig_ME_bonus = 0.02
                    if self.rigs_bonus['Advanced Component']['TE']:
                        rig_TE_bonus = 0.2

            skill_TE_bonus = 0.2
            ME = (1 - base_ME/100) * (1 - rig_ME_bonus * self.system_mod) * (1 - self.ME_bonus)
            TE = (1 - base_TE/100) * (1 - rig_TE_bonus * self.system_mod) * (1 - self.TE_bonus) * (1 - skill_TE_bonus)
            print(base_ME,rig_ME_bonus,self.system_mod,self.ME_bonus)
            return ME, TE
        else:
            raise TypeError('given blueprint is neither a BPO or a BPC')


    def acivity_manufacture(self, blueprintID):
        """ use an assembly line of the station to manufacture the given blueprint.
        """
        pass  # todo: get from masterscript

    def acivity_invent(self, blueprintID):
        """ use an assembly line of the station to invent the given blueprint.
        """
        pass  # todo: get from masterscript


class AssemblyLine(Indy):
    """ the object which does all industry stuff: manufacture, invention etc"""

    def __init__(self, assemblyLine):
        super(self).__init__()
        """ """

        self.assemblyLineTypeID = None
        self.assemblyLineTypeName = None
        # from ramAssemblyLineTypes
        self.activityID = None
        self.baseCostMultiplier = None
        self.baseMaterialMultiplier = None
        self.baseTimeMultiplier = None
        self.description = None
        self.volume = None
        self.categoryID_multipliers = None
        self.groupID_multipliers = None

    def initialize_multipliers(self):
        """ init groupID and categoryID based multipliers"""

        for key in self.sde.ramAssemblyLineTypeDetailPerCategory:
            if self.sde.ramAssemblyLineTypeDetailPerCategory[key]['assemblyLineTypeID'] == self.assemblyLineTypeID:
                self.categoryID_multipliers = self.sde.ramAssemblyLineTypeDetailPerCategory[key]

        for key in self.sde.ramAssemblyLineTypeDetailPerGroup:
            if self.sde.ramAssemblyLineTypeDetailPerGroup[key]['assemblyLineTypeID'] == self.assemblyLineTypeID:
                self.groupID_multipliers = self.sde.ramAssemblyLineTypeDetailPerGroup[key]


class Item(Indy):
    """ an object in new eden """

    def __init__(self, item):
        super(Item, self).__init__()
        """ initialzie"""
        if type(item) is str:  # allows for initialization with name or ID (str) or ID (int)
            try:  # try ID int
                self.itemID = int(item)
            except ValueError:  # if not a number: its a name!
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
        # from invMetaTypes and invMetaGroups
        self.metaGroupID = None
        self.metaGroupName = None
        self.parentTypeID = None
        # from groupIDs
        self.categoryID = None
        self.fittableNonSingleton = None
        self.iconID = None
        self.groupName = None
        # from categoryIDs
        self.categoryName = None
        self.categoryIconID = None
        try:
            self.price = self.market.get_min_sellprice(self.itemID)
        except KeyError:
            self.price = None
        self.parent_blueprintID = self.sde.get_parent_blueprintID(self.itemID)

        self.initialize_typeIDs()
        self.initialize_groupIDs()
        self.initialize_categoryIDs()
        self.initialize_invMetaTypes()

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

    def initialize_invMetaTypes(self):
        self.metaGroupID = self.sde.invMetaTypes[self.itemID]['metaGroupID']
        self.parentTypeID = self.sde.invMetaTypes[self.itemID]['parentTypeID']
        self.metaGroupName = self.sde.invMetaGroups[self.itemID]['metaGroupName']


class Blueprint(Item):
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
                requirement_list=self.sde.blueprints[self.itemID]['activities']['copying']['materials'],
                key_label='typeID',
                quantity_label='quantity')

            self.copying_skills = self.translate_to_dict(
                requirement_list=self.sde.blueprints[self.itemID]['activities']['copying']['skills'],
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

    def get_invention_parent_bp(self):  # todo: make this function
        self.inventionBP = self.sde.get_parent_invention_blueprintID(self.itemID)
        return self.inventionBP

    def print_manufacturing_materials(self):
        """ prints the shopping list!"""
        print('\nMaterials List:\n')
        for name, quantity in self.manufacturing_materials.items():
            print('{0}  {1}'.format(Item(name).name, quantity))


class BPC(Blueprint):
    """ a real bpc"""

    def __init__(self, blueprintID, runs=None, ME=0, TE=0):
        """ define the bpc properties"""
        super(BPC, self).__init__(blueprintID)

        self.blueprintID = blueprintID
        self.runs = runs
        self.ME = ME
        self.TE = TE
        self.initialize_BP()



if __name__ == '__main__':
    os.chdir('../')
    main()

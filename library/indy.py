# -*- coding: utf-8 -*-
"""
Created on Sat May 20 17:02:12 2017

@author: Stymir
"""
from openpyxl import load_workbook
from . import gfs, indy
import csv
import os
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def main():
#    sde = SDE()
#    sde.import_indy_DB()
#    timer.tic()

    testbp = Blueprint(28675)
    testbp.fetchBpData()

    print(testbp.getMaterials(20))



#%% Eve Item classes



class Blueprint(object):
    ''' a blueprint class '''
    def __init__(self, blueprintID):
        ''' '''
        self.bpID = blueprintID
        self.activities = {'copying', 'manufacturing', 'research_material', 'research_time'}
        self.blueprintTypeID = blueprintID
        self.maxProductionLimit = 0
        self.product = 0
        self.product_quantity = 0


    def fetchBpData(self, sde = None):
        ''' load info from SDE '''
        if sde == None:
            sde = SDE()
            print('Loading Blueprints to SDE')
            sde.importData('blueprints')
        try:
            bpDict = sde.blueprints[self.bpID]
        except KeyError:
            print('invalid BP ID')

        for key in bpDict:
            setattr(self,key,bpDict[key])

        self.product = self.activities['manufacturing']['products'][0]['typeID']
        self.product_quantity = self.activities['manufacturing']['products'][0]['quantity']

    def getMaterials(self, runs = 1, buyT1 = False):
        ''' returns materials required for n runs'''
        requirement_list = self.activities['manufacturing']['materials']
        requirement_dict={}
        for item in requirement_list:
            quantity = item['quantity'] * runs
            requirement_dict[item['typeID']] = [quantity]
        return(requirement_dict)






class EVEItem(object):
    ''' an object i new eden '''
    def __init__(self, itemID):
        ''' initialzie'''
        self.itemID = itemID


    def printName(self):
        ''' initializes '''
        val = 'ID is ' + str(self.itemID)
        setattr(self,'name',val)


    def loadAttributes(self, sde = None):
        ''' load info from SDE '''
        if sde == None:
            sde = SDE()



#%% Database Management

class SDE(object):
    ''' Containts a series of dictionaries containing necessary sde data'''
    def __init__(self):
        ''' '''
        self.db_location_csv = 'D:/Documents/py_code/EVE_database/csv/'
        self.db_location_YAML = 'D:/Documents/py_code/EVE_database/sde/fsd/'
        self.db_list = []

        self.db_coreIndy =  ['invTypes',
                             'invCategories',
                             'invGroups',
                             'invMetaTypes',
                             'invMetaGroups',
                             'blueprints']

        self.db_coreIndy_old =  ['invTypes',
                             'invCategories',
                             'invGroups',
                             'invMetaTypes',
                             'invMetaGroups',
                             'industryActivity',
                             'industryActivityMaterials',
                             'industryActivityProbabilities']

        self.activityTypeID = { 0:'None',
                                1:'Manufacturing',
                                2:'Researching Technology',
                                3:'Researching Time Efficiency',
                                4:'Researching Material Efficiency',
                                5:'Copying',
                                6:'Duplicating',
                                7:'Reverse Engineering',
                                8:'Invention'}





    def importData(self,db_name):
        ''' imports data from a database file (csv)'''
        if db_name in ['blueprints', 'typeIDs', 'groupIDs', 'graphicIDs']:
            print('importing: ' + self.getFilepath(db_name,'yaml'))
            data = self.getFile_yaml(db_name)
        else:
            print('importing: ' + self.getFilepath(db_name,'csv'))
            data = self.getFile_csv(db_name)

        setattr(self,db_name,data)
        print('import completed')

    def getFilepath(self,db_name,ext):
        return(self.db_location_csv + db_name + '.'+ext)

    def init_db_list(self):
        file_list = os.listdir(self.db_location_csv)
        for name in file_list:
            self.db_list.append(name[:-4])

    def importALL(self):
        if len(self.db_list) == 0:
            self.init_db_list()

        for name in self.db_list:
            print(name)
            self.importData(self.getFilepath(name))

    def import_db_coreIndy(self):

        for name in self.db_coreIndy_old:
            self.importData(name)

    def import_indy_DB(self):
        '''imports databases necessary for the Industrial calculation tool'''
        for name in self.db_coreIndy:
            self.importData(name)

    def openFile_xlsx(self, file):
        ''' '''
        wb = load_workbook(file)
        ws = wb.active
        self.name = ws['A1'].value
        # get column headers
        for col in ws.iter_cols(max_row=1):
            for cell in col:
                self.headers.append(cell.value)

        # write to data
        row_i = 0

        for row in ws.iter_rows(min_row = 2):

            row_i +=1
            key = ws.cell(row = row_i, column=1).value
            col_i = 0
            self.data[key] = {}
            for header in self.headers:
                col_i +=1
                self.data[key][header] = ws.cell(row = row_i, column=col_i).value

    def getFile_yaml(self,db_name):
        ''' imports a YAML database to same name attribute'''
        f = open(self.db_location_YAML + db_name + '.yaml', 'r')
        data = yaml.load(f)
        return(data)


    def getFile_csv(self, db_name):
        ''' '''
        headline = True
        data = {}
        with open(self.db_location_csv + db_name + '.csv', 'r',  encoding="utf8") as f:
            reader = csv.reader(f)

            for line in reader: #get headers for dict key names
                if headline:
                    headers = line
                    headline = False
                else:
                    key = int(line[0])
                    pos = 0

                    try: # try appending new values to repeated 1st column items
                         # otherwise just add new entry
                        _ = data[key]
                        for word in line:
                            label = headers[pos]
                            pos += 1
                            val = getNum_or_Str(word)
                            try:
                                data[key][label].append(val)
                            except AttributeError:
                                tmp = data[key][label]
                                data[key][label] = [tmp]
                                data[key][label].append(val)

                    except KeyError:
                        data[key] = {}
                        for word in line:
                            label = headers[pos]
                            pos += 1
                            val = getNum_or_Str(word)

                            data[key][label] = val
        return(data)




if __name__ == '__main__':
    main()
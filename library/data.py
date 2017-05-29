# -*- coding: utf-8 -*-
"""
Created on Sat May 20 17:02:12 2017

@author: Stymir
"""

import csv
import json
import pickle
from urllib import request
from xml.dom import minidom

import yaml
from openpyxl import load_workbook

from library import gfs


def main():
    """ this refreshes import of data from yaml sde to pickle format"""
    # sde = SDE()
    # sde.import_quick()
    # # dbList = ['blueprints', 'typeIDs']
    # # # import yaml / csv and dump pickle
    # # sde.export_multiple_pickle(dbList)
    # name = sde.typeIDs[34]['name']['en']
    #
    # ID = sde.get_ID_from_name('condor')
    #
    # print(sde.get_blueprintID(ID))

    requestURL = 'https://api.eveonline.com/corp/AccountBalance.xml.aspx?keyID=3287371&vCode=U3gp6wIb3MnLOeRpCKlqk4eL2fF4Tz4cPyBFdES85FUcFp6KfrFPCMOHrUjsTpmO'
    requestURL = 'https://api.eveonline.com/corp/Blueprints.xml.aspx?KeyID=3289868&vCode=34Gvs33mzfGvPUv3d2vXENhRbrgtEGdqAD0LXYGpJ6kI2Q38uvbUSXaqoTM9G111'
    market_api = 'https://api.eve-marketdata.com/api/item_prices2.xml?char_name=demo&region_ids=10000002&buysell=s'




    # apidata = API()
    # apis = list(apidata.api_URLs.keys())
    # print(apis)
    # for api in apis:
    #     apidata.fetch_eveapi_data(api)


    # for s in itemlist:
    #     print(s.attributes['name'].value)


    market = Market()
    #market.update_marketData()

    print(len(market.data[34].keys()))

    # market2.load_marketData()
    item = '3332'

    cost = market.get_min_sellprice(3332)
    print('{0} minimum cost is {1} ISK'.format(item,cost))

class SDE(object):
    """ Contains a series of dictionaries containing necessary sde data"""

    def __init__(self):

        DB_LOCATION = '../database/'
        DB_LOCATION = 'D:/Documents/py_code/EVEIndyTool/database/'  # comment when at home

        self.DB_LOCATION_CSV = 'D:/Documents/py_code/EVE_database/' + 'csv/'
        self.DB_LOCATION_PRIMARY = 'D:/Documents/py_code/EVE_database/' + 'sde/fsd/'
        self.DB_LOCATION_SECONDARY = 'D:/Documents/py_code/EVE_database/' + 'sde/bsd/'  # todo: implement secondary import

        self.DB_LOCATION_PICKLE = DB_LOCATION
        self.QUICK_IMPORT_LIST = ('typeIDs', 'blueprints', 'categoryIDs', 'groupIDs')
        self.PRIMARY_IMPORT_LIST = ('typeIDs', 'blueprints', 'categoryIDs', 'groupIDs')
        self.SECONDARY_IMPORT_LIST = ('invMarketGroups', 'invMetaGroups','invMetaTypes','ADD MORE' 'ram...')

        self.db_list = []
        # primary
        self.typeIDs = None
        self.blueprints = None
        self.categoryIDs = None
        self.groupIDs = None
        # secondary
        self.invMetaGroups = None
        self.invMetaTypes = None
        self.invTypes = None
        # todo: add more secondary imports

    def import_data(self, dbName):
        """ imports data from a database file (csv or yaml)"""
        timer = gfs.Timer()
        timer.tic()
        if dbName in ['blueprints', 'typeIDs', 'groupIDs', 'graphicIDs']:
            print('importing: ' + dbName + '.yaml')
            data = self.get_data_yaml(dbName)
        else:
            print('importing: ' + dbName + '.csv')
            data = self.get_data_csv(dbName)
        setattr(self, dbName, data)
        dt = timer.toc(out='return')
        print('Imported {0} in {1:.3f} ms'.format(dbName, dt))

    def export_pickle(self, dbName):
        """ create a pickle for each database loaded"""
        filePath = self.DB_LOCATION_PICKLE + dbName + '.p'
        try:
            timer = gfs.Timer()
            timer.tic()
            data = getattr(self, dbName)
            with open(filePath, 'wb+') as f:
                pickle.dump(data, f)
            dt = timer.toc(out='return')
            print('Exported {0} in {1:.3f} ms'.format(dbName, dt))
        except AttributeError:
            print('no data found with name ' + dbName)

    def export_multiple_pickle(self, dbList):
        """ import from sde and export to pickle the list of databases given """
        for db_name in dbList:
            print('importing: ' + db_name)
            self.import_data(db_name)
            print('exporting: ' + db_name)
            self.export_pickle(db_name)

    def import_pickle(self, dbName):
        """ imports data from pickle dumped file"""
        # try:
        timer = gfs.Timer()
        timer.tic()
        print('Importing: ' + dbName)
        filePath = self.DB_LOCATION_PICKLE + dbName + '.p'
        with open(filePath, 'rb') as f:
            data = pickle.load(f)
            setattr(self, dbName, data)
        dt = timer.toc(out='return')
        print('Imported {0} in {1:.3f} ms'.format(dbName, dt))

    def import_quick(self):
        """ import databases relevant for indy calculator"""
        for dbName in self.QUICK_IMPORT_LIST:
            self.import_pickle(dbName)

    def get_filepath(self, db_name, ext):
        """
        :return : returns str of database file path.
        :param db_name: name of database file to load
        :type ext: str representing db_name file format

        """
        if ext == 'yaml':
            return self.DB_LOCATION_CSV + db_name + '.' + ext
        elif ext == 'csv':
            return self.DB_LOCATION_PRIMARY + db_name + '.' + ext
        else:
            return 'Incorrect file extension.'

    def get_data_yaml(self, db_name):
        """ imports a YAML database to same name attribute"""
        with  open(self.DB_LOCATION_PRIMARY + db_name + '.yaml', 'r', encoding="utf8") as f:
            data = yaml.load(f)
        return data

    def get_data_csv(self, db_name):
        """ imports a CSV database to same name attribute """
        headline = True
        data = {}
        with open(self.DB_LOCATION_CSV + db_name + '.csv', 'r', encoding="utf8") as f:
            reader = csv.reader(f)

            for line in reader:  # get headers for dict key names
                if headline:
                    headers = line
                    headline = False
                else:
                    key = int(line[0])
                    pos = 0

                    try:  # try appending new values to repeated 1st column items
                        # otherwise just add new entry
                        _ = data[key]
                        for word in line:
                            label = headers[pos]
                            pos += 1
                            val = gfs.getNum_or_Str(word)
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
                            val = gfs.getNum_or_Str(word)

                            data[key][label] = val
        return (data)

    def get_ID_from_name(self, name):
        """ returns the itemID from a given name

        :return: int
        """
        itemName = ''
        for key in self.typeIDs:
            try:
                itemName = str(self.typeIDs[key]['name']['en']).lower()
                if itemName == name.lower():
                    return key
            except KeyError:
                pass

    def get_blueprintID(self, itemID):  # todo: Fix me
        """ returns the blueprintID that produces the item with given itemID
        :return: int
        """
        parent_tipeID = 0
        for key in self.blueprints:
            try:
                product_list = self.blueprints[key]['activities']['manufacturing']['products']
                for item in product_list:  # products is a list. so we need to break the dcit style and add list parser
                    parent_tipeID = item['typeID']
                    if parent_tipeID == itemID:
                        return key
            except KeyError:
                pass



                # --------------- Old and deprectated methods ------------------

    def open_file_xlsx(self, file):
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

        for row in ws.iter_rows(min_row=2):

            row_i += 1
            key = ws.cell(row=row_i, column=1).value
            col_i = 0
            self.data[key] = {}
            for header in self.headers:
                col_i += 1
                self.data[key][header] = ws.cell(row=row_i, column=col_i).value


class API(object):  # todo: transfer api data to login.ini
    """ """

    def __init__(self):
        """ """
        self.AccountBalance = {}
        self.AssetList = {}
        self.Blueprints = {}
        self.IndustryJobs = {}
        self.MarketOrders = {}

        self.credentials = {  # todo: make character key iteration
            'Pax Correl': {'KeyID': '3802771',
                           'vCode': 'dJkO006gOITgaBGloymLL6DLs2Zuxt0qGHO263tTE9bHMsmfghr3HlP7ZmLZ869w'},
            'Freyja Correl': {'KeyID': '3289868',
                              'vCode': '34Gvs33mzfGvPUv3d2vXENhRbrgtEGdqAD0LXYGpJ6kI2Q38uvbUSXaqoTM9G111'},
            'mamoc mant': {'KeyID': '4190790',
                           'vCode': 'Py18Ybm98U4RimRciHEolXQ4WAABrqLmsiovtPrrGfmByXzVDlW8uTWbPq8nZurA'},
            'Steinn Ymir': {'KeyID': '3932915',
                            'vCode': 'fOP7WYgafX0Jd3wnxIX9krC1mDfNJpiXjoiZ1lg45tVkqenSxt7e74QKhxljfjIG'},
            'Arnok Senklis': {'KeyID': '3287371',
                              'vCode': 'U3gp6wIb3MnLOeRpCKlqk4eL2fF4Tz4cPyBFdES85FUcFp6KfrFPCMOHrUjsTpmO'},
            'Juliet Senklis': {'KeyID': '3932917',
                               'vCode': 'P0F9mLsh6piP4sBdApZQK6HUUrkztqigisG6k1cN9zREv8Uf7Bjm1EsJcjDjkh3U'},
            'Tibus Khan': {'KeyID': '4193331',
                           'vCode': 'm9tJQS2FH6dn5tp8Aw4V6LoiFm1RNAZHJmp842hxThRCEsqsb3JLy2Ko4tIavgib'},
            'Aerie Khan': {'KeyID': '4193333',
                           'vCode': 'CdsX1iRif4pA3UqXtoQt65OxYr75ZGAlsJZaDRfVqooBxMk5CzVbqK3OUgjCyVQB'},
            'Khaylin Greystar': {'KeyID': '4193336',
                                 'vCode': 'DqrDfrJ5ZKK7w2zSkwVjjFtKqpxTaD1IpwKpK1Q1tFWzb8FdZwckNLe3QqeBsAV8'},
            'zalatex': {'KeyID': '4193326',
                        'vCode': 'wapB06YsJt7OpuGJBz1DoHrsVAMErFfVeAsxF6Md2rOpLok83G3zNyIFuS7ZqQFO'},
            'Tania Redstar': {'KeyID': '4193325',
                              'vCode': '1afM85e8AL5Zk0JE7Q4VW66sUVDYZwZCaOKv9VVXickTsk3ykEKN69a6TyqrzED3'},
            'Aerie Bluestar': {'KeyID': '4193327',
                               'vCode': 'FqLD4XKD9YKLplSRy8eAapKaC7E8LfnYsLn0jtpnH1Xvr2DFBHv0VZNWIVI9WDie'},
        }
        self.api_URLs = {'AssetList': "https://api.eveonline.com/corp/AssetList.xml.aspx?flat=1&",
                         'Blueprints': "https://api.eveonline.com/corp/Blueprints.xml.aspx?",
                         'MarketOrders': "https://api.eveonline.com/corp/MarketOrders.xml.aspx?",
                         'IndustryJobs': "https://api.eveonline.com/corp/IndustryJobs.xml.aspx?",
                         'AccountBalance': "https://api.eveonline.com/corp/AccountBalance.xml.aspx?",
                         }

    def update_AssetList(self):  # todo: add cachedUntill check
                                 # todo: check keys for optimized data import
        self.AssetList = self.fetch_eveapi_data('AssetList')

    def update_Blueprints(self):
        self.Blueprints = self.fetch_eveapi_data('Blueprints')

    def update_MarketOrders(self):
        self.MarketOrders = self.fetch_eveapi_data('MarketOrders')

    def update_IndustryJobs(self):
        self.IndustryJobs = self.fetch_eveapi_data('IndustryJobs')

    def update_AccountBalance(self):
        self.AccountBalance = self.fetch_eveapi_data('AccountBalance')

    def update_All(self):
        self.update_AccountBalance()
        self.update_AssetList()
        self.update_Blueprints()
        self.update_IndustryJobs()
        self.update_MarketOrders()

    def get_api_url(self, api_type, char):
        """ """
        url = str(self.api_URLs[api_type] +
                  'keyID=' + self.credentials[char]['KeyID'] +
                  '&vCode=' + self.credentials[char]['vCode'])
        return url

    def fetch_eveapi_data(self, api_type, dict_key=None):

        """ get data from api"""
        url = self.get_api_url(api_type, 'Pax Correl')
        # if api_type == 'AssetList': # different structure, requires different method
        #     self.fetch_assetsList()
        # else:

        print('Requesting {} data from API system'.format(api_type))
        print(url)
        xmldoc = minidom.parse(request.urlopen(url))  # parse the url, fetch data from xml into xmldoc

        currentTime = xmldoc.getElementsByTagName('currentTime')[0].firstChild.nodeValue
        cachedUntil = xmldoc.getElementsByTagName('cachedUntil')[0].firstChild.nodeValue

        data_dict = {'times': {'cachedUntil': cachedUntil,  # initialize output dictionary appending time medatada
                               'currentTime': currentTime}}

        header_line = xmldoc.getElementsByTagName('rowset')  # get xml table legend
        api_name = header_line[0].attributes['name'].value

        if dict_key is None:  # unless specified, assign value in key as title for sub-dictionaries in data output
            dict_key = header_line[0].attributes['key'].value
        column_headers = header_line[0].attributes['columns'].value.split(',')
        data_body = xmldoc.getElementsByTagName('row')

        for line in data_body:
            data_dict[line.attributes[dict_key].value] = {}
            for col in column_headers:
                data_dict[line.attributes[dict_key].value][col] = line.attributes[col].value

        print('successfully imported {} data'.format(api_type))
        return data_dict


class ESI(object):  # todo: find out how to make authorized requests
    """ class managing esi data download"""

    def __init__(self):
        """ """
        self.url_serverStatus = 'https://esi.tech.ccp.is/latest/status/?datasource=tranquility&user_agent=eveindytool'
        self.DB_LOCATION = 'D:/Documents/py_code/EVEIndyTool/database/'
        self.root = 'https://esi.tech.ccp.is/latest/'
        self.user_agent = 'eveindytool_Pax_Correl'
        DB_LOCATION = 'D:/Documents/py_code/EVEIndyTool/database/'  # comment when at home





    def fetch_esi_data(self, url=None):  # todo: cached time check and error management

        if url is None:
            url = self.url_serverStatus
        j = request.urlopen(url)
        data = json.load(j)
        return data


class Market(ESI):
    """ """
    def __init__(self):
        super().__init__()
        self.data = {}
        try:
            self.load_marketData()
        except EOFError:
            pass

    def get_min_sellprice(self, item_id, stationID=60003760):  # todo: expand functionalities as min volume etc
        """ returns the minimum sell price for given item_id"""
        minprice = 999999999999
        for key in self.data[item_id]:
            if not self.data[item_id][key]['is_buy_order']:
                price = self.data[item_id][key]['price']
                loc = self.data[item_id][key]['location_id']
                if loc == stationID:  # if it is in jita 4-4
                    minprice = min([minprice, price])
        return minprice




    def load_marketData(self):
        filePath = self.DB_LOCATION + 'marketdata.p'
        with open(filePath, 'rb') as f:
            self.data = pickle.load(f)

    def update_marketData(self):
        """ update from web and dump to pickle database"""
        data = self.get_market_data()
        print(type(data))
        print(data)
        self.data = data
        filePath = self.DB_LOCATION + 'marketdata.p'

        print('dumping data to ' + filePath)
        with open(filePath, 'wb+') as f:
            pickle.dump(data,f)

    def import_price_history(self, type_id, location=10000002):
        """ get price statistics for given item in given location, default is The Forge"""

        request_url = (self.root + 'markets' + str(location) +
                       'history/?datasource=tranquility&type_id=' +
                       type_id + '&user_agent=' + self.user_agent)
        return self.fetch_esi_data(request_url)

    def get_market_data(self, itemID=None, location=10000002, ordertype='all', maxpages=0):
        """ return dict of full market data,
        location: default location The Forge
        ordertype: 'buy' 'sell' or 'all' - only works when typeID is given
        maxpages: number of pages to download, 0 means all

        :returns data_dict, dictionary in format: {itemID : {sell: {0: data, 1:data},
                                                             buy{0: data, 1:data}}}"""

        pagenum = 0
        got_empty_page = False
        data_list = []
        data_dict = {}
        print('requesting Market data from locationID: ' + str(location) + ' through ESI')
        while not got_empty_page:
            pagenum += 1
            request_url = (self.root + 'markets/' + str(location) +
                           '/orders/?datasource=tranquility' +
                           '&order_type=' + ordertype +
                           '&page=' + str(pagenum))
            if itemID is not None:
                request_url += '&type_id=' + str(itemID)
            request_url += '&user_agent=' + self.user_agent
            print('page ' + str(pagenum))
            print(request_url)
            result = self.fetch_esi_data(request_url)
            # when result contains less than the 10000 limit per page, stop iterating pages
            if len(result) != 10000 or pagenum == maxpages or itemID is not None:
                got_empty_page = True
            for item in result:
                data_list.append(item)
        print(str(len(data_list)) + ' market entries imported.')

        # sort results in a better dictionary
        for item in data_list:
            try:
                num = len(data_dict[item['type_id']].keys())
                data_dict[item['type_id']][num + 1] = item
            except KeyError:
                data_dict[item['type_id']] = {1: item}
        print(data_dict)
        #
        #
        # for item in data_list:
        #     if item['is_buy_order']:
        #         try:
        #             buynum = len(data_dict[item['type_id']]['buy'].keys())
        #             data_dict[item['type_id']]['buy'][str(buynum + 1)] = item
        #         except KeyError:
        #             data_dict[item['type_id']] = {'buy': {'0': item}}
        #     else:
        #         try:
        #             sellnum = len(data_dict[item['type_id']]['sell'].keys())
        #             data_dict[item['type_id']]['sell'][str(sellnum + 1)] = item
        #         except KeyError:
        #             data_dict[item['type_id']] = {'sell': {'0': item}}
        return data_dict


if __name__ == '__main__':
    DB_LOCATION = 'D:/Documents/py_code/EVEIndyTool/database/'  # todo: remove if not used

    main()

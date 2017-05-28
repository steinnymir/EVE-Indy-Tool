from urllib import request
import xml.etree.ElementTree as ET
from xml.dom import minidom
import json


class API(object):
    """ """

    def __init__(self):
        """ """
        pass

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
        self.market_api = 'https://api.eve-marketdata.com/api/item_prices2.xml?char_name=demo&region_ids=10000002&buysell=s'

    def get_api_url(self, api_type, char):
        """ """
        url = str(self.api_URLs[api_type] +
                  'keyID=' + self.credentials[char]['KeyID'] +
                  '&vCode=' + self.credentials[char]['vCode'])
        return url

    def fetch_eveapi_data(self, api_type, dict_key=None):  # todo: check if ...

        """ get data from api"""
        url = self.get_api_url(api_type, 'Pax Correl')
        # if api_type == 'AssetList': # different structure, requires different method
        #     self.fetch_assetsList()
        # else:

        print('Requesting {} data'.format(api_type))
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

    def fetch_assetsList(self):

        url = 'https://api.eveonline.com/corp/AssetList.xml.aspx?keyID=3802771&vCode=dJkO006gOITgaBGloymLL6DLs2Zuxt0qGHO263tTE9bHMsmfghr3HlP7ZmLZ869w'

        # print('Requesting {} data'.format('AssetList'))
        # print(url)
        # xmldoc = minidom.parse(request.urlopen(url))  # parse the url, fetch data from xml into xmldoc
        #
        # currentTime = xmldoc.getElementsByTagName('currentTime')[0].firstChild.nodeValue
        # cachedUntil = xmldoc.getElementsByTagName('cachedUntil')[0].firstChild.nodeValue
        #
        # data_dict = {'times': {'cachedUntil': cashedUntill,  # initialize output dictionary appending time medatada
        #                        'currentTime': currentTime}}
        #
        # result = xmldoc.getElementsByTagName('result')
        #
        #
        # if root[0].childNodes:
        #     for node in root.childNodes:
        #         if node.nodeType == node.ELEMENT_NODE:
        #             print(node.tagName, "has value:", node.nodeValue, "and is child of:", node.parentNode.tagName)
        #             print_node(node)


        tree = ET.parse(request.urlopen(url))
        root = tree.getroot()
        currentTime = root.find('currentTime').text
        cachedUntil = root.find('cachedUntil').text

        data_dict = {'times': {'cachedUntil': cachedUntil,  # initialize output dictionary appending time medatada
                               'currentTime': currentTime}}

        result = root.find('result')

        for child in result:
            name = child.attrib['name']
            key = child.attrib['key']
            columns = child.attrib['columns'].split(',')
            print(columns)


class ESI(object):  # todo: find out how to make authorized requests
    """ class managing esi data download"""

    def __init__(self):
        """ """
        self.url_serverStatus = 'https://esi.tech.ccp.is/latest/status/?datasource=tranquility&user_agent=eveindytool'
        self.esi_request_type = {'market_orders': ''}

        self.root = 'https://esi.tech.ccp.is/latest/'
        self.user_agent = 'eveindytool_ingame_Pax_Correl'

    def get_market_data(self, itemID=None, location=10000002, ordertype='sell', maxpages=0):
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
        print('requesting Market data from locationID: ' + str(location))
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
            #
            if len(result) != 10000 or pagenum == maxpages or itemID is not None:
                got_empty_page = True
            for item in result:
                data_list.append(item)
        print(len(data_list))

        for item in data_list:
            if item['is_buy_order'] is True:
                try:
                    entrynumber = len(data_dict[item['type_id']]['buy'].keys())
                    data_dict[item['type_id']]['buy'][entrynumber + 1] = item
                except KeyError:
                    data_dict[item['type_id']] = {'buy': {0: item}}
            elif item['is_buy_order'] is False:
                try:
                    entrynumber = len(data_dict[item['type_id']]['sell'].keys())
                    data_dict[item['type_id']]['sell'][entrynumber + 1] = item
                except KeyError:
                    data_dict[item['type_id']] = {'sell': {0: item}}
        return data_dict

    def import_price_history(self, itemID, location=10000002):
        """ get price statistics for given item in given location, default is The Forge"""

        request_url = (self.root + 'markets' + str(location) +
                       'history/?datasource=tranquility&type_id=' +
                       typeID + '&user_agent=' + self.user_agent)
        return self.fetch_esi_data(request_url)

    def fetch_esi_data(self, url=None):  # todo: cachtime chekc and error management

        if url is None:
            url = self.url_serverStatus
        j = request.urlopen(url)
        data = json.load(j)
        return data


def main():
    requestURL = 'https://api.eveonline.com/corp/AccountBalance.xml.aspx?keyID=3287371&vCode=U3gp6wIb3MnLOeRpCKlqk4eL2fF4Tz4cPyBFdES85FUcFp6KfrFPCMOHrUjsTpmO'
    requestURL = 'https://api.eveonline.com/corp/Blueprints.xml.aspx?KeyID=3289868&vCode=34Gvs33mzfGvPUv3d2vXENhRbrgtEGdqAD0LXYGpJ6kI2Q38uvbUSXaqoTM9G111'
    market_api = 'https://api.eve-marketdata.com/api/item_prices2.xml?char_name=demo&region_ids=10000002&buysell=s'

    esi = ESI()
    data = esi.get_market_data(34)
    print(data[34])



    # apidata = API()
    # apis = list(apidata.api_URLs.keys())
    # print(apis)
    # for api in apis:
    #     apidata.fetch_eveapi_data(api)


# for s in itemlist:
#     print(s.attributes['name'].value)
if __name__ == '__main__':
    main()

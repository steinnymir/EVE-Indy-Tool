from urllib import request

from xml.dom import minidom
import json


class API(object):
    """ """

    def __init__(self):
        """ """
        pass

        self.credentials = {
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
            'zalatex': {'KeyID': '4193326', 'vCode': 'wapB06YsJt7OpuGJBz1DoHrsVAMErFfVeAsxF6Md2rOpLok83G3zNyIFuS7ZqQFO'},
            'Tania Redstar': {'KeyID': '4193325',
                              'vCode': '1afM85e8AL5Zk0JE7Q4VW66sUVDYZwZCaOKv9VVXickTsk3ykEKN69a6TyqrzED3'},
            'Aerie Bluestar': {'KeyID': '4193327',
                               'vCode': 'FqLD4XKD9YKLplSRy8eAapKaC7E8LfnYsLn0jtpnH1Xvr2DFBHv0VZNWIVI9WDie'},
        }
        self.api_URLs = {'AssetList': "https://api.eveonline.com/corp/AssetList.xml.aspx?",
                         'Blueprints': "https://api.eveonline.com/corp/Blueprints.xml.aspx?",
                         'MarketOrders': "https://api.eveonline.com/corp/MarketOrders.xml.aspx?",
                         'IndustryJobs': "https://api.eveonline.com/corp/IndustryJobs.xml.aspx?",
                         'AccountBalance': "https://api.eveonline.com/corp/AccountBalance.xml.aspx?",
                         'AssetList': "https://api.eveonline.com/corp/AssetList.xml.aspx?",
                         }
        self.market_api = 'https://api.eve-marketdata.com/api/item_prices2.xml?char_name=demo&region_ids=10000002&buysell=s'


    def get_api_url(self, api_type, char):
        """ """
        url = str(self.api_URLs[api_type] +
               'keyID=' + self.credentials[char]['keyID'] +
               '&vCode=' + self.credentials[char]['vCode'])
        return url

    def fetch_eveapi_data(requestURL, dict_key=None):

        """ get data from api"""

        xmldoc = minidom.parse(request.urlopen(requestURL))

        currentTime = xmldoc.getElementsByTagName('currentTime')
        cashedUntill = xmldoc.getElementsByTagName('currentTime')
        print(getText(currentTime))
        header_line = xmldoc.getElementsByTagName('rowset')
        api_name = header_line[0].attributes['name'].value
        if dict_key is None:
            dict_key = header_line[0].attributes['key'].value
        column_headers = header_line[0].attributes['columns'].value.split(',')
        print(column_headers)

        data_body = xmldoc.getElementsByTagName('row')
        data_dict = {}
        for line in data_body:
            data_dict[line.attributes[dict_key].value] = {}
            for col in column_headers:
                data_dict[line.attributes[dict_key].value][col] = line.attributes[col].value

        return (data_dict)


class ESI(object):  # todo: write me
    """ """
    def __init__(self):
        """ """
        pass



def main():
    requestURL = 'https://api.eveonline.com/corp/AccountBalance.xml.aspx?keyID=3287371&vCode=U3gp6wIb3MnLOeRpCKlqk4eL2fF4Tz4cPyBFdES85FUcFp6KfrFPCMOHrUjsTpmO'
    requestURL = 'https://api.eveonline.com/corp/Blueprints.xml.aspx?KeyID=3289868&vCode=34Gvs33mzfGvPUv3d2vXENhRbrgtEGdqAD0LXYGpJ6kI2Q38uvbUSXaqoTM9G111'
    market_api = 'https://api.eve-marketdata.com/api/item_prices2.xml?char_name=demo&region_ids=10000002&buysell=s'

    esi_url_status = 'https://esi.tech.ccp.is/latest/status/?datasource=tranquility&user_agent=eveindytool'
    #
    # with open(request.urlopen(esi_url_status)) as data_file:
    #     data = json.load(data_file)

    j = request.urlopen(esi_url_status)

    data = json.load(j)


    print(data)
    # apidata = API()
    # apidata.fetch_eveapi_data(market_api)



# for s in itemlist:
#     print(s.attributes['name'].value)
if __name__ == '__main__':
    main()

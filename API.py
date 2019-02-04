
import numpy as np
import json,requests
import urllib.request

#TODO:
#Pull API Data for players from WG API
#Pull Server Average Data for ships from wows-numbers (and credit OG author)


class API():

    ID = ''
    claninfoep = 'https://api.worldofwarships.com/wows/clans/info/'
    clanlistep = 'https://api.worldofwarships.com/wows/clans/list/'
    accinfoep = 'https://api.worldofwarships.com/wows/account/info/'
    acclistep = 'https://api.worldofwarships.com/wows/account/list/'
    pediaep = 

    wowsnumep = 'https://wows-numbers.com/personal/rating/expected/json/'
    #Data for expected values used to calculate PR pulled 
    #from the official wows-numbers website: https://wows-numbers.com

    def __init__(self):
        self.ID=open('ID.txt',"r").read().strip()
    
    def getClanMembers(self,name):
        data={'application_id':self.ID,'search':name.strip()}
        r = requests.post(self.acclistep,data)
        return json.loads(r.text)['data'][0]['account_id']

    def getPlayerID(self,name):
        data={'application_id':self.ID,'search':name.strip()}
        r = requests.post(self.acclistep,data)
        return json.loads(r.text)['data'][0]['account_id']

    def getPlayerStats(self,ID):
        data={'application_id':self.ID,'account_id':ID}
        r = requests.post(self.accinfoep,data)
        return json.loads(r.text)['data'][str(ID)]
    
    def getClanID(self,name):
        data={'application_id':self.ID,'search':name.strip()}
        r = requests.post(self.clanlistep,data)
        return json.loads(r.text)['data'][0]['clan_id']

    def getClanTag(self,ID):
        data={'application_id':self.ID,'clan_id':ID}
        r = requests.post(self.claninfoep,data)
        return json.loads(r.text)['data'][str(ID)]['tag']

    def getClanName(self,ID):
        data={'application_id':self.ID,'clan_id':ID}
        r = requests.post(self.claninfoep,data)
        return json.loads(r.text)['data'][str(ID)]['name']

    def getShipName(self,ID):
        data 


    def expectedValues(self):
        r = requests.get(self.wowsnumep)
        data = json.loads(r.text)
        return data

if(__name__=="__main__"):
    a = API()
    print(a.ID)
    print(a.getClanID('MIA-E'))
    print(a.getClanTag('1000044001'))
    print(a.getClanName('1000044001'))
    print(a.getPlayerStats(a.getPlayerID('Modulatus')))
    #print(a.expectedValues())
    

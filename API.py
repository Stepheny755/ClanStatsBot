
import numpy as np
import json,requests
import urllib.request

#TODO:
#Pull API Data for players from WG API

class API():

    ID = ''
    claninfoep = 'https://api.worldofwarships.com/wows/clans/info/'
    clanlistep = 'https://api.worldofwarships.com/wows/clans/list/'
    accinfoep = 'https://api.worldofwarships.com/wows/account/info/'
    acclistep = 'https://api.worldofwarships.com/wows/account/list/'
    pediaep = 'https://api.worldofwarships.com/wows/encyclopedia/ships/'

    wowsnumep = 'https://wows-numbers.com/personal/rating/expected/json/'
    #Data for expected values used to calculate PR pulled
    #from the official wows-numbers website: https://wows-numbers.com

    def __init__(self):
        self.ID=open('ID.txt',"r").read().strip()

    def getClanMembers(self,ID):
        data={'application_id':self.ID,'clan_id':ID}
        r = requests.post(self.claninfoep,data)
        try:
            return json.loads(r.text)['data'][str(ID)]['members_ids']
        except:
            return None

    def getPlayerID(self,name):
        data={'application_id':self.ID,'search':name.strip()}
        r = requests.post(self.acclistep,data)
        try:
            return json.loads(r.text)['data'][0]['account_id']
        except:
            return None

    def getPlayerName(self,ID):
        data={'application_id':self.ID,'account_id':ID}
        r = requests.post(self.accinfoep,data)
        try:
            return json.loads(r.text)['data'][str(ID)]['nickname']
        except:
            return None

    def getPlayerStats(self,ID):
        data={'application_id':self.ID,'account_id':ID}
        r = requests.post(self.accinfoep,data)
        try:
            return json.loads(r.text)['data'][str(ID)]
        except:
            return None

    def getClanID(self,name):
        data={'application_id':self.ID,'search':name.strip()}
        r = requests.post(self.clanlistep,data)
        try:
            return json.loads(r.text)['data'][0]['clan_id']
        except:
            return None

    def getClanTag(self,ID):
        data={'application_id':self.ID,'clan_id':ID}
        r = requests.post(self.claninfoep,data)
        try:
            return json.loads(r.text)['data'][str(ID)]['tag']
        except:
            return None

    def getClanName(self,ID):
        data={'application_id':self.ID,'clan_id':ID}
        r = requests.post(self.claninfoep,data)
        try:
            return json.loads(r.text)['data'][str(ID)]['name']
        except:
            return None

    def getShipName(self,ID):
        data={'application_id':self.ID,'ship_id':ID}
        r = requests.post(self.pediaep,data)
        if json.loads(r.text)['data'][str(ID)] is not None:
            out = json.loads(r.text)['data'][str(ID)]['name']
            print(out)
            return out
        else:
            pass

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
    #print(a.getPlayerStats(a.getPlayerID('Modulatus')))
    print(a.expectedValues())
    #print(a.getShipName(4287510224))

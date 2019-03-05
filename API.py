
import numpy as np
import json,requests
import urllib.request

#TODO:
#Pull API Data for players from WG API

class API():

    ID = ''
    claninfoep = 'https://api.worldofwarships.com/wows/clans/info/'
    clanlistep = 'https://api.worldofwarships.com/wows/clans/list/'
    accinfoep =  'https://api.worldofwarships.com/wows/account/info/'
    acclistep =  'https://api.worldofwarships.com/wows/account/list/'
    pediaep =    'https://api.worldofwarships.com/wows/encyclopedia/ships/'
    shipstatep = 'https://api.worldofwarships.com/wows/ships/stats/'

    wowsnumep =  'https://wows-numbers.com/personal/rating/expected/json/'
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

    def getPlayerCard(self,ID):
        data={'application_id':self.ID,'account_id':ID}
        r = requests.post(self.accinfoep,data)
        try:
            return json.loads(r.text)['data'][str(ID)]
        except:
            return None

    def getPlayerStats(self,ID):
        data=self.getPlayerCard(ID)
        return data['statistics']

    def getPlayerShipStats(self,pID):
        data={'application_id':self.ID,'account_id':pID}
        r = requests.post(self.shipstatep,data)
        try:
            return json.loads(r.text)['data'][str(pID)]
        except:
            return None

    def getShipDmg(self,data):
        return float(data['pvp']['damage_dealt'])

    def getShipWR(self,data):
        if(data['pvp']['wins']==0 or data['pvp']['battles']==0):
            return 0.0
        return float(data['pvp']['wins']/data['pvp']['battles']*100)

    def getShipWins(self,data):
        if(data['pvp']['wins']==0 or data['pvp']['battles']==0):
            return 0.0
        return int(data['pvp']['wins'])

    def getShipKills(self,data):
        return float(data['pvp']['frags'])

    def getShipBattles(self,data):
        return int(data['pvp']['battles'])

    def getShipID(self,data):
        return int(data['ship_id'])

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
    #print(a.ID)
    #print(a.getClanID('MIA-E'))
    #print(a.getClanTag('1000044001'))
    #print(a.getClanName('1000044001'))
    #print(a.getPlayerStats(a.getPlayerID('Modulatus')))
    #print(a.getShipName(4287510224))
    temp = a.getPlayerStats(a.getPlayerID("Modulatus"))
    print(temp)

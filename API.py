import numpy as np
import json,requests

#TODO:
#Pull API Data for players from WG API
#Pull Server Average Data for ships from wows-numbers (and credit OG author)


class API():

    ID = ''
    claninfoep = 'https://api.worldofwarships.com/wows/clans/info/'
    clanlistep = 'https://api.worldofwarships.com/wows/clans/list/'
    accinfoep = 'https://api.worldofwarships.com/wows/account/info/'
    acclistep = 'https://api.worldofwarships.com/wows/account/list/'

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
        data={'application_id':self.ID,'search':name.strip()}
        r = requests.post(self.accinfoep,data)
        return json.loads(r.text)['data'][ID]
    
    def getClanID(self,name):
        data={'application_id':self.ID,'search':name.strip()}
        r = requests.post(self.clanlistep,data)
        return json.loads(r.text)['data'][0]['clan_id']

    def getClanTag(self,ID):
        data={'application_id':self.ID,'clan_id':ID}
        r = requests.post(self.claninfoep,data)
        return json.loads(r.text)['data'][ID]['tag']

    def getClanName(self,ID):
        data={'application_id':self.ID,'clan_id':ID}
        r = requests.post(self.claninfoep,data)
        return json.loads(r.text)['data'][ID]['name']

if(__name__=="__main__"):
    a = API()
    print(a.ID)
    print(a.getClanID('MIA-E'))
    print(a.getClanTag('1000044001'))
    print(a.getClanName('1000044001'))
    print(a.getPlayerStats(a.getPlayerID))
    

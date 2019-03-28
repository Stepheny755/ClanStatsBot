import json,requests
import urllib.request

from time import sleep
from util import Util

import asyncio
import time
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
        self.data = {}

        self.backoff_tries = 20
        self.backoff_start_interval_sec = 1

    def post_with_backoff(self, uri, payload):

        # Backoff but retry 407 errors (rate limiting from WG)
        backoff = self.backoff_start_interval_sec
        for i in range(self.backoff_tries):
            r = requests.post(uri, payload)
            j = r.json()
            if 'error' in j:
                if j['error']['code'] == 407:
                    if j['error']['message'] == 'REQUEST_LIMIT_EXCEEDED':
                        time.sleep(backoff)
                        backoff = backoff * 2
                    else:
                        print ('error:{}'.format(j))
                        raise RuntimeError('Unexpected error from WG API')
            else:
                return r
        raise RuntimeError('Exceeded allowed backoff attempts!')

# INIT
# PLAYER RELATED FUNCTIONS

    def getPlayerID(self,name):
        data={'application_id':self.ID,'search':name.strip()}
        r = self.post_with_backoff(self.acclistep,data)
        try:
            return json.loads(r.text)['data'][0]['account_id']
        except:
            return None

    def getPlayerName(self,ID):
        data={'application_id':self.ID,'account_id':ID}
        r = self.post_with_backoff(self.accinfoep,data)
        try:
            return json.loads(r.text)['data'][str(ID)]['nickname']
        except:
            return None

    def getPlayerCard(self,ID):
        if ID not in self.data:
            # print('Getting player card for id={}'.format(ID) )

            data={'application_id':self.ID,'account_id':ID}
            r = self.post_with_backoff(self.accinfoep,data)
            try:
                self.data[ID] = json.loads(r.text)['data'][str(ID)]
            except Exception as e:
                print('hit exception {e} for player={id}'.format(e=e.with_traceback, id=ID))
        else:
            pass
            # print('using cached data for id={}'.format(ID) )
        return self.data[ID]

    def getPlayerStats(self,ID):
        # sleep(0.1)
        data=self.getPlayerCard(ID)
        return data['statistics']

    def getPlayerBattles(self,ID):
        data = self.getPlayerStats(ID)
        return int(data['pvp']['battles'])

    def getPlayerWins(self,ID):
        data=self.getPlayerStats(ID)
        return int(data['pvp']['wins'])

    def getPlayerAvgWR(self,ID):
        u = Util()
        return u.round3(float(self.getPlayerWins(ID))/float(self.getPlayerBattles(ID))*100)

    def getPlayerAvgDmg(self,ID):
        data = self.getPlayerStats(ID)
        battles = self.getPlayerBattles(ID)
        u = Util()
        temp = float(data['pvp']['damage_dealt'])/float(battles)
        return u.round2(temp)

    def getPlayerAvgKills(self,ID):
        data = self.getPlayerStats(ID)
        battles = self.getPlayerBattles(ID)
        u = Util()
        temp = float(data['pvp']['frags'])/float(battles)
        return u.round3(temp)

    def getPlayerAvgSpottingDmg(self,ID):
        data = self.getPlayerStats(ID)
        battles = self.getPlayerBattles(ID)
        u = Util()
        temp = float(data['pvp']['damage_scouting'])/float(battles)
        return u.round2(temp)

    def getPlayerAvgPotentialDmg(self,ID):
        data = self.getPlayerStats(ID)
        battles = self.getPlayerBattles(ID)
        u = Util()
        temp = float(data['pvp']['torpedo_agro']+data['pvp']['art_agro'])/float(battles)
        return u.round2(temp)

# PLAYER RELATED FUNCTIONS
# SHIP RELATED FUNCTIONS

    def getPlayerShipStats(self,pID):
        data={'application_id':self.ID,'account_id':pID}
        r = self.post_with_backoff(self.shipstatep,data)
        try:
            return json.loads(r.text)['data'][str(pID)]
        except Exception as e:
            return None

    def getShipName(self,ID):
        data={'application_id':self.ID,'ship_id':ID}
        r = self.post_with_backoff(self.pediaep,data)
        if json.loads(r.text)['data'][str(ID)] is not None:
            out = json.loads(r.text)['data'][str(ID)]['name']
            #print(out)
            return out
        else:
            pass

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

# SHIP RELATED FUNCTIONS
# CLAN RELATED FUNCTIONS

    def getClanID(self,name):
        data={'application_id':self.ID,'search':name.strip()}
        r = self.post_with_backoff(self.clanlistep,data)
        try:
            return json.loads(r.text)['data'][0]['clan_id']
        except:
            return None

    def getClanTag(self,ID):
        data={'application_id':self.ID,'clan_id':ID}
        r = self.post_with_backoff(self.claninfoep,data)
        try:
            return json.loads(r.text)['data'][str(ID)]['tag']
        except:
            return None

    def getClanName(self,ID):
        data={'application_id':self.ID,'clan_id':ID}
        r = self.post_with_backoff(self.claninfoep,data)
        try:
            return json.loads(r.text)['data'][str(ID)]['name']
        except:
            return None

    def getClanMembers(self,ID):
        data={'application_id':self.ID,'clan_id':ID}
        r = self.post_with_backoff(self.claninfoep,data)
        try:
            return json.loads(r.text)['data'][str(ID)]['members_ids']
        except:
            return None

# CLAN RELATED FUNCTIONS
# OTHER

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
    # print(a.expectedValues())
    print(a.getPlayerAvgSpottingDmg(a.getPlayerID("Modulatus")))
    print(a.getPlayerAvgPotentialDmg(a.getPlayerID("Modulatus")))

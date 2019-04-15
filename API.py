import json,requests
import urllib.request

from time import sleep
from util import Util

import asyncio
import time

class API():

    key = ''
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
        self.key=open('ID.txt',"r").read().strip()
        self.playercard = {}
        self.shipid = {}

        self.

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
        """
        Parameters:
        name: name of player

        Returns:
        WG ID of player (int)
        """
        data={'application_id':self.key,'search':name.strip()}
        r = self.post_with_backoff(self.acclistep,data)
        try:
            return json.loads(r.text)['data'][0]['account_id']
        except:
            return None

    def getPlayerName(self,pID):
        """
        Parameters:
        pID: WG player ID

        Returns:
        name of player (str)
        """
        data={'application_id':self.key,'account_id':pID}
        r = self.post_with_backoff(self.accinfoep,data)
        try:
            return json.loads(r.text)['data'][str(pID)]['nickname']
        except:
            return None

    def getPlayerCard(self,pID):
        """
        Caches to reduce # of api calls and runtime

        Parameters:
        pID: WG player ID

        Returns:
        All the data on a players overall values from the WG api (dict)
        """
        if pID not in self.playercard:
            # print('Getting player card for id={}'.format(ID) )

            data={'application_id':self.key,'account_id':pID}
            r = self.post_with_backoff(self.accinfoep,data)
            try:
                self.data[pID] = json.loads(r.text)['data'][str(pID)]
            except Exception as e:
                print('hit exception {e} for player={pID}'.format(e=e.with_traceback, pID=pID))
        else:
            pass
            # print('using cached data for id={}'.format(ID) )
        return self.data[pID]

    def getPlayerStats(self,pID):
        """
        Parameters:
        pID: WG player ID

        Returns:
        the statistics portion of the data from WG api (dict)
        """
        # sleep(0.1)
        data=self.getPlayerCard(pID)
        return data['statistics']

    def getPlayerBattles(self,pID):
        """
        Parameters:
        pID: WG player ID

        Returns:
        number of battles played by player (int)
        """
        data = self.getPlayerStats(pID)
        return int(data['pvp']['battles'])

    def getPlayerWins(self,pID):
        """
        Parameters:
        pID: WG player ID

        Returns:
        number of wins player has (int)
        """
        data=self.getPlayerStats(pID)
        return int(data['pvp']['wins'])

    def getPlayerAvgWR(self,pID):
        """
        Parameters:
        pID: WG player ID

        Returns:
        overall win rate of player (float)
        """

        return self.u.round3(float(self.getPlayerWins(pID))/float(self.getPlayerBattles(pID))*100)

    def getPlayerAvgDmg(self,pID):
        """
        Parameters:
        pID: WG player ID

        Returns:
        overall average damage of player (float)
        """
        data = self.getPlayerStats(pID)
        battles = self.getPlayerBattles(pID)

        temp = float(data['pvp']['damage_dealt'])/float(battles)
        return self.u.round2(temp)

    def getPlayerAvgKills(self,pID):
        """
        Parameters:
        pID: WG player ID

        Returns:
        overall average kills of player (float)
        """
        data = self.getPlayerStats(pID)
        battles = self.getPlayerBattles(pID)

        temp = float(data['pvp']['frags'])/float(battles)
        return self.u.round3(temp)

    def getPlayerAvgSpottingDmg(self,pID):
        """
        Parameters:
        pID: WG player ID

        Returns:
        overall average spotting damage (float)
        """
        data = self.getPlayerStats(pID)
        battles = self.getPlayerBattles(pID)

        temp = float(data['pvp']['damage_scouting'])/float(battles)
        return self.u.round2(temp)

    def getPlayerAvgPotentialDmg(self,pID):
        """
        Parameters:
        pID: WG player ID

        Returns:
        overall average potential damage (float)
        """
        data = self.getPlayerStats(pID)
        battles = self.getPlayerBattles(pID)

        temp = float(data['pvp']['torpedo_agro']+data['pvp']['art_agro'])/float(battles)
        return self.u.round2(temp)

# PLAYER RELATED FUNCTIONS
# SHIP RELATED FUNCTIONS

    def getPlayerShipStats(self,pID):
        """
        Function not cached because we expect it to only run once per player
        Note: Similar to getPlayerCard(), but instead of overall values this
        returns ship valuess

        Parameters:
        pID: WG player ID

        Returns:
        all the data on every ship that a player has played (list of dicts)
        - Each index in the list is an individual ship (represented by a dict)
        - Feed the individual dicts into the functions below
        """
        data={'application_id':self.key,'account_id':pID}
        r = self.post_with_backoff(self.shipstatep,data)
        try:
            return json.loads(r.text)['data'][str(pID)]
        except Exception as e:
            return None

    def getShipName(self,sID):
        """
        Parameters:
        sID: WG ship ID

        Returns:
        Name of the ship (str)
        """
        data={'application_id':self.key,'ship_id':sID}
        r = self.post_with_backoff(self.pediaep,data)
        if json.loads(r.text)['data'][str(sID)] is not None:
            out = json.loads(r.text)['data'][str(sID)]['name']
            #print(out)
            return out
        else:
            pass

    def getShipInfo(self, sID):
        """
        Parameters:
        sID: WG ship ID

        Returns:
        Name of the ship (str)
        Ship Class
        Ship Tier
        """
        data={'application_id':self.key,'ship_id':sID}
        r = self.post_with_backoff(self.pediaep,data)
        if json.loads(r.text)['data'][str(sID)] is not None:
            t = json.loads(r.text)['data'][str(sID)]
            out = (t['name'], t['type'], t['tier'])
            #print(out)
            return out
        else:
            pass

    def getShipDmg(self,data):
        """
        Parameters:
        data: dict returned by getPlayerShipStats()

        Returns:
        average damage of a ship (float)
        """
        return float(data['pvp']['damage_dealt'])

    def getShipWR(self,data):
        """
        Parameters:
        data: dict returned by getPlayerShipStats()

        Returns:
        average win rate of a ship (float)
        """
        if(data['pvp']['wins']==0 or data['pvp']['battles']==0):
            return 0.0
        return float(data['pvp']['wins']/data['pvp']['battles']*100)

    def getShipWins(self,data):
        """
        Parameters:
        data: dict returned by getPlayerShipStats()

        Returns:
        total wins of a ship (int)
        """
        if(data['pvp']['wins']==0 or data['pvp']['battles']==0):
            return 0.0
        return int(data['pvp']['wins'])

    def getShipKills(self,data):
        """
        Parameters:
        data: dict returned by getPlayerShipStats()

        Returns:
        average kills of a ship (float)
        """
        return float(data['pvp']['frags'])

    def getShipBattles(self,data):
        """
        Parameters:
        data: dict returned by getPlayerShipStats()

        Returns:
        tota battles of a ship (int)
        """
        return int(data['pvp']['battles'])

    def getShipID(self,data):
        """
        Parameters:
        data: dict returned by getPlayerShipStats()

        Returns:
        the ID of the ship in dict data (int)
        """

        return int(data['ship_id'])

# SHIP RELATED FUNCTIONS
# CLAN RELATED FUNCTIONS

    def getClanID(self,name):
        """
        Parameters:
        name: tag of a clan (e.g. MIA,MIA-E)

        Returns:
        WG ID of the clan (int)
        """
        data={'application_id':self.key,'search':name.strip()}
        r = self.post_with_backoff(self.clanlistep,data)
        try:
            return int(json.loads(r.text)['data'][0]['clan_id'])
        except:
            return None

    def getClanTag(self,cID):
        """
        Parameters:
        cID: WG clan ID

        Returns:
        the name/tag of the clan (e.g. MIA,MIA-E) (str)
        """
        data={'application_id':self.key,'clan_id':cID}
        r = self.post_with_backoff(self.claninfoep,data)
        try:
            return json.loads(r.text)['data'][str(cID)]['tag']
        except:
            return None

    def getClanName(self,cID):
        """
        Parameters:
        cID: WG clan ID

        Returns:
        the full name of the clan (e.g. Mortem in Aquam) (str)
        """
        data={'application_id':self.key,'clan_id':cID}
        r = self.post_with_backoff(self.claninfoep,data)
        try:
            return json.loads(r.text)['data'][str(cID)]['name']
        except:
            return None

    def getClanMembers(self,cID):
        """
        Parameters:
        cID: WG clan ID

        Returns:
        the member id's of all players in a clan (lst)
        """
        data={'application_id':self.key,'clan_id':cID}
        r = self.post_with_backoff(self.claninfoep,data)
        try:
            return json.loads(r.text)['data'][str(cID)]['members_ids']
        except:
            return None

# CLAN RELATED FUNCTIONS
# OTHER

    def expectedValues(self):
        """
        Returns:
        expected values from wows-numbers.com
        (link to website: https://wows-numbers.com/personal/rating)
        """
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
    #t = a.getPlayerShipStats(a.getPlayerID('Modulatus'))
    #print(type(t))
    #for items in t:
    #    print(items)
    #print(a.getShipName(4287510224))
    print(a.getShipInfo(3751753168))
    # print(a.expectedValues())
    #print(a.getClanMembers(a.getClanID("MIA")))
    #print(a.getPlayerAvgSpottingDmg(a.getPlayerID("Modulatus")))
    #print(a.getPlayerAvgPotentialDmg(a.getPlayerID("Modulatus")))

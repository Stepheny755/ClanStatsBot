from API import API
from data import Data
import json

class Player():

    lbt = 0 #last_battle_time
    playerID = 0 #account_id
    playerName = '' #nickname

    avgDmg = 0
    avgKills = 0
    avgCaps = 0
    avgSpotting = 0
    avg = 0

    wins = 0
    losses = 0
    draws = 0
    battles = 0

    distance = 0

    def __init__(self,clan,name):
        #TODO:get Player 'name' Data from WG API
        api = API()
        dt = Data()

        self.playerName=name
        self.playerID=api.getPlayerID(name)

        #TODO:If directory playerclan/playername does not exist and contains no files, then pull data directly from wg api without saving (temp lookup)
        temppath = str(str(clan).strip()+"/"+str(name).strip())
        filestring = dt.getSMostRecent(temppath)
        #print(filestring)
        filestring = filestring.replace("'",'"')
        filestring = filestring.replace("None",'0')
        filestring = filestring.replace("False",'0')
        #print(filestring)
        #print(filestring[189])
        lst = json.loads(filestring)
        print(lst)
        print()

        stats = lst['statistics']
        self.battles = stats['battles']
        self.distance = stats['distance']

        stats = stats['pvp']

        for i in stats:
            print(i)


        for i in lst:
            #print(str(i)+": "+str(lst[i]))
            break
        #print(lst['statistics'])

        #print(Player.calcwr(self.wins,self.losses))
        pass

    def calcwr(w,l):
        value = float(w/(w+l))*100 #w+l can be replaced with number of battles later
        return float("%.3f" % value)


if(__name__=="__main__"):
    p = Player("MIA-E","Modulatus")

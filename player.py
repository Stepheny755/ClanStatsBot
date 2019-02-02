from API import API

class Player():

    avgDmg = 0
    avgKills = 0
    avgCaps = 0
    avgSpotting = 0
    avg = 0

    wins = 0
    losses = 0
    draws = 0
    battles = 0

    def __init__(self,name):
        #TODO:get Player 'name' Data from WG API
        self.avgDmg=1000
        self.wins=75800
        self.losses=2200
        self.battles=
        print(Player.calcwr(self.wins,self.losses))
        pass

    def calcwr(w,l):
        value = float(w/(w+l))*100 #w+l can be replaced with number of battles later
        return float("%.3f" % value)


if(__name__=="__main__"):
    p = Player("modsucks")

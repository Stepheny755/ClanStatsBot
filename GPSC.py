from API import API
import pickle
import numpy as np
from stats_v import Stats

class ClanStats:
    def __init__(self, CL):
        self.clanList = CL #List of Clans
        self.a = API()
        self.s = Stats()
    
    def getAllPlayers(self): #Gets every in clan within clanlist
        self.pID = [] #Player ids of every player in every clan #player with index here will have same index value in stats array
        #self.totalPlayers = 0
        self.pName = {} #{PID: name, ...}
        #self. = {}
        for ci in range(len(self.clanList)):
            clan = self.clanList[ci]
            #print(clan)
            #cid = self.a.getClanID(clan)
            t = self.a.getClanMembers(self.a.getClanID(clan))
            #print(t)
            self.pID.extend(t)
            for pID in t:
                n = self.a.getPlayerName(pID)
                self.pName[pID] = (n, ci)
                #print(str(pID) + ': ' + n)
        self.totalPlayers = len(self.pID)
        #print(self.pID)

    #v WOWSNUMBERS STUFF v
    def updateExpected(self):
        r = self.a.expectedValues()
        self.time = r['time']
        self.expected = r['data']

        self.shiplength = len(self.expected)

    def saveExpected(self):
        with open('Expected-' + str(self.time) + '.pkl', 'wb') as f:
            pickle.dump([self.time, self.expected, self.SID],f)
    
    def getExpected(self, name):
        with open(name, 'rb') as f:
            self.time, self.expected, self.SID = pickle.load(f)
            
        self.shiplength = len(self.expected)

    def getShipIDs(self): #Gets every ship ID within expected
        self.SID = {} #{name: SID...}
        for shipid in self.expected:
            self.SID[self.a.getShipName(shipid)] = shipid
    
    def expectedProcessing(self):
        self.updateExpected()
        print('Update Completed')
        #self.getShipIDs()
        print('ShipID Completed')
        #self.saveExpected()
        print('Save Completed')
        self.extractExpected()
        print('Extract Completed')
    
    def extractExpected(self):
        self.expectedstats = np.zeros((self.shiplength, 3))
        self.shipArrPos = {}
        counter = 0
        try:
            for shipid in self.expected:
                shipdata = self.expected[shipid]
                if len(shipdata) != 0:
                    self.expectedstats[counter, 0] = shipdata['average_damage_dealt']
                    self.expectedstats[counter, 1] = shipdata['average_frags']
                    self.expectedstats[counter, 2] = shipdata['win_rate'] / 100
                else:
                    self.expectedstats[counter,:] = np.array([-1,-1,-1]) #if shipid has no stats
                    print('no stats' + str(shipid))
                self.shipArrPos[int(shipid)] = counter
                #print(self.a.getShipName(shipid))
                #print(self.shipArrPos)
                counter += 1
            #self.expectedstats[-1,:] = np.sum(self.expectedstats[:-1,:],axis=1)
        except:
            print(self.expected)
        #print(self.expectedstats[:-1,:])
        #print(np.sum(self.expectedstats[:-1,:],axis=0))
        
                
    #^ WOWSNUMBERS STUFF ^
    def getTotalPlayerStats(self):
        self.nf = set()
        for pI in range(self.totalPlayers):
            players = self.pID[pI]
            data = self.a.getPlayerShipStats(players)
            for ships in data:
                shipid = self.a.getShipID(ships)
                battles = self.a.getShipBattles(ships)
                dmg = self.a.getShipDmg(ships)
                frags = self.a.getShipKills(ships)
                wins = self.a.getShipWins(ships)
                #print(str(battles) + ' ' + str(frags) + ' ' + str(dmg) )
                if shipid in self.shipArrPos:
                    self.playerShipStats[pI][self.shipArrPos[shipid]][:4] = np.array([battles, dmg, frags, wins])
                    #print(self.expectedstats[self.shipArrPos[shipid]] * battles)
                    self.playerExpected[pI,:] += self.expectedstats[self.shipArrPos[shipid]] * battles #I think I can replace this with a matrix multiplication later...
                else:
                    #print('not found: ' + str(shipid))
                    if shipid not in self.nf:
                        self.nf.add(shipid)

        #print(self.playerShipStats[:,:-1,:])
        #print(np.sum(self.playerShipStats[:,:-1,:], axis=1))
        #self.playerShipStats[:,-1,:] = np.sum(self.playerShipStats[:,:-1,:], axis=1)
        #print(self.playerShipStats[:,-1,:])
        #self.expectedstats[-1,:] = np.sum(np.where(self.playerShipStats[:,:,0] > 0,self.expectedstats[:-1,:], 0))
        #b = self.playerShipStats[:,:,0]
        #self.playerShipStats[:,:,4] = np.where(b > 0, self.playerShipStats[:,:,1] / b, 0)
        #self.playerShipStats[:,:,5] = np.where(b > 0, self.playerShipStats[:,:,2] / b, 0)
        #self.playerShipStats[:,:,6] = np.where(b > 0, self.playerShipStats[:,:,3] / b, 0)
        #print('Player Stats')
        #print(self.playerShipStats[:,:,1])
        #print(b)
        #print(self.playerShipStats[:,:,4:7])

    def calcPR(self, pd, ed, pf, ef, pw, ew):
        return 700*self.s.PRnormDmg(pd, ed) + 300*self.s.PRnormKil(pf, ef) + 150*self.s.PRnormWin(pw, ew)

    def calcShipPR(self):
        #print(self.playerShipStats[:,:,7].shape)
        #print(self.expectedstats[:,0].shape)
        b = self.playerShipStats[:,:,0]
        #print(700*self.s.PRnormDmg(self.playerShipStats[:,:,4], self.expectedstats[:,0]) + 300*self.s.PRnormKil(self.playerShipStats[:,:,5], self.expectedstats[:,1]) + 150*self.s.PRnormWin(self.playerShipStats[:,:,6], self.expectedstats[:,2]))
        self.playerShipStats[:,:,4] = self.calcPR(self.playerShipStats[:,:,1], self.expectedstats[:,0] * b, self.playerShipStats[:,:,2], self.expectedstats[:,1] * b, self.playerShipStats[:,:,3], self.expectedstats[:,2] * b)

    def calcPlayerPR(self):
        
        playersum = np.sum(self.playerShipStats[:,:-1,:], axis=1)
        print(playersum[:1,4])
        print(playersum.shape)
        print(self.playerExpected)
        self.playerPR = self.calcPR(playersum[:,1], self.playerExpected[:,0], playersum[:,2], self.playerExpected[:,1], playersum[:,3], self.playerExpected[:,2])
    def calcPlayerPR_O(self):
        #print(np.sum(self.playerShipStats[:,:,0], axis=1))
        #print(np.sum(self.playerShipStats[:,:,4]))
        b = self.playerShipStats[:,:,0]
        #print(np.sum(self.playerShipStats[:,:,4] * self.playerShipStats[:,:,0], axis=1))
        self.playerPR = np.sum(self.playerShipStats[:,:,4] * b, axis=1) / np.sum(b, axis=1)

    def calcStats(self):
        print('Starting Player Collection')
        self.getAllPlayers()
        print('Completed Player Collection\nStarting Expected Processing')
        self.expectedProcessing()
        print('Completed Expected Processing\nStarting Player Ship Stats')
        self.playerShipStats = np.zeros((self.totalPlayers, self.shiplength, 5))
        self.playerExpected = np.zeros((self.totalPlayers, 3))
        """
        [player][ship][stat] stats: [0] - number of battles [1] - Dmg [2] - Frags [3] - Wins [4] - PR [post calc] 
        """
        self.getTotalPlayerStats()
        print('Completing Player Ship Stats\nStarting Ship PR Calculation')
        self.calcShipPR()
        print('Completing Ship PR Calculation\nStarting Player PR Calculation')

        #self.playerPR = np.zeros(self.totalPlayers)
        self.calcPlayerPR()
        print('Completing Player PR Calculation')

    def printStats(self):
        for w in range(self.totalPlayers):
            pName = self.pName[self.pID[w]][0]
            print(pName + ': '+ str(int(np.round(self.playerPR[w]))))
    
    def findMissingShips(self):
        for shipid in self.nf:
            print(self.a.getShipName(shipid))
    
if (__name__ == '__main__'):
    clanstats = ClanStats(['MIA',])
    clanstats.calcStats()
    clanstats.printStats()
    #clanstats.findMissingShips()








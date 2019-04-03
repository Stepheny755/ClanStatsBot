from API import API
import pickle
import numpy as np
from stats_v import Stats
import operator

class ClanStats:
    def __init__(self, CL):
        self.clanList = CL #List of Clans
        self.a = API()
        self.s = Stats()
    
    def getAllPlayers(self): #Gets every in clan within clanlist
        print('Starting Player Collection')
        self.pID = [] #Player ids of every player in every clan #player with index here will have same index value in stats array
        #self.totalPlayers = 0
        self.pName = {} #{PID: name, ...}
        #self. = {}
        for ci in range(len(self.clanList)): 
            clan = self.clanList[ci]
            #print(clan)
            #cid = self.a.getClanID(clan)
            t = self.a.getClanMembers(self.a.getClanID(clan))
            self.pID.extend(t)
            for pID in t:
                #print(type(pID))
                n = self.a.getPlayerName(pID)
                self.pName[pID] = (n, ci)
                #print(str(pID) + ': ' + n)
        #self.pID.sort()
        self.totalPlayers = len(self.pID)
        print('Completed Player Collection')
    #v WOWSNUMBERS STUFF v
    def updateExpected(self):
        print('Acquiring Expected')
        r = self.a.expectedValues()
        self.time = r['time']
        self.expected = r['data']

        self.shipLength = len(self.expected)
        print('Acquisition Completed')

    def saveExpected(self): #Kind of pointless atm
        print('Saving...')
        with open('Expected-' + str(self.time) + '.pkl', 'wb') as f:
            pickle.dump([self.time, self.expected, self.SID],f)
        print('Save Completed')
    
    def getExpected(self, name): #Kind of pointless atm
        with open(name, 'rb') as f:
            self.time, self.expected, self.SID = pickle.load(f)
            
        self.shipLength = len(self.expected)

    def getShipIDs(self): #Gets every ship ID within expected - No longer needed
        self.SID = {} #{name: SID...}
        for shipid in self.expected:
            self.SID[self.a.getShipName(shipid)] = shipid
    
    def extractExpected(self):
        print('Extracting Expected...')
        """
        Takes data from Expected and converts into Numpy Array
        """
        self.expectedStats = np.zeros((self.shipLength, 3))
        """
        Dimensions: [ship counter] [stat type]: stat type 0- exp avg dmg 1- exp avg frags 2- exp wr [decimals not %]
        """
        self.shipArrPos = {} #used to make sure all ships are aligned correctly in playerShipStats [shipid] : position
        counter = 0
        #try: 
        self.SID = {}
        self.ns = set() #find ships with no stats
        for shipid in self.expected:
            self.SID[self.a.getShipName(shipid)] = shipid
            shipdata = self.expected[shipid]
            if len(shipdata) != 0:
                self.expectedStats[counter, 0] = shipdata['average_damage_dealt']
                self.expectedStats[counter, 1] = shipdata['average_frags']
                self.expectedStats[counter, 2] = shipdata['win_rate'] / 100
            else:
                self.expectedStats[counter,:] = np.array([-1,-1,-1]) #if shipid has no stats
                self.ns.add(shipid)
                #print('no stats' + str(shipid))
            self.shipArrPos[int(shipid)] = counter
            counter += 1
        print('Expected Extract Completed')
                
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
                if shipid in self.shipArrPos:
                    self.playerShipStats[pI][self.shipArrPos[shipid]][:4] = np.array([battles, dmg, frags, wins])
                else:
                    #print('not found: ' + str(shipid))
                    if shipid not in self.nf:
                        self.nf.add(shipid)
    #Calculations
    def calcPR(self, pd, ed, pf, ef, pw, ew):
        return 700*self.s.PRnormDmg(pd, ed) + 300*self.s.PRnormKil(pf, ef) + 150*self.s.PRnormWin(pw, ew)

    def calcShipPR(self, playerStats, expected): 
        """
        Takes: 
        playerShipStats like array Dimensions:[player index][ship index][0:battles, 1:dmg, 2:frags, 3:wins, 4:pr]
        expectedShipStats like array Dimensions:[ship][0:avg dmg 1:avg frags 2:wr]
        Returns: 
        playerStats[:,:,4]
        """
        b = playerStats[:,:,0]
        #self.playerShipStats[:,:,4] = 
        return self.calcPR(playerStats[:,:,1], expected[:,0] * b, playerStats[:,:,2], expected[:,1] * b, playerStats[:,:,3], expected[:,2] * b)

    def calcPlayerOverall(self, playerStats, shipExpected):
        """
        Takes: 
        playerShipStats like array Dimensions:[player index][ship index][0:battles, 1:dmg, 2:frags, 3:wins, 4:pr]
        expectedShipStats like array Dimensions:[ship][0:avg dmg 1:avg frags 2:wr]
        Returns: 
        playersum - Dimensions:[player index][total battles, dmg, frags, battles won, overall pr]
        """
        playersum = np.sum(playerStats[:,:-1,:], axis=1)
        expected = np.matmul(playerStats[:,:,0], shipExpected)
        playersum[:,4] = self.calcPR(playersum[:,1], expected[:,0], playersum[:,2], expected[:,1], playersum[:,3], expected[:,2])
        playersum[:,1:4] = np.transpose(np.where(playersum[:,0] > 0, np.transpose(playersum[:,1:4]) / playersum[:,0], 0))
        return playersum

    def calcPlayerPR_O(self): #Technically the correct way to do it, but wowsnumbers is dumb I guess shrug
        """
        Not Used
        """
        #print(np.sum(self.playerShipStats[:,:,0], axis=1))
        #print(np.sum(self.playerShipStats[:,:,4]))
        b = self.playerShipStats[:,:,0]
        #print(np.sum(self.playerShipStats[:,:,4] * self.playerShipStats[:,:,0], axis=1))
        self.playerPR = np.sum(self.playerShipStats[:,:,4] * b, axis=1) / np.sum(b, axis=1)
    #Clusted Execution Functions
    def updatePlayerExpected(self):
        self.getAllPlayers()
        self.updateExpected()
        self.extractExpected()

    def calcCurrent(self):
        print('Starting Player Ship Stats')
        self.playerShipStats = np.zeros((self.totalPlayers, self.shipLength, 5))
        self.playerExpected = np.zeros((self.totalPlayers, 3))
        """
        [player][ship][stat] stats: [0] - number of battles [1] - Dmg [2] - Frags [3] - Wins [4] - PR [post calc] 
        """
        self.getTotalPlayerStats()
        print('Completed Player Ship Stats\nStarting Ship PR Calculation')
        self.playerShipStats[:,:,4] = self.calcShipPR(self.playerShipStats, self.expectedStats)
        print('Completed Ship PR Calculation\nStarting Player PR Calculation')

        #self.playerPR = np.zeros(self.totalPlayers)
        self.playerOverall = self.calcPlayerOverall(self.playerShipStats, self.expectedStats)
        print('Completed Player PR Calculation')
    
    def saveStats(self):
        with open('Stats_' + str(self.time) + '.pkl', 'wb') as f:
            pickle.dump([self.playerShipStats, self.playerOverall, self.shipArrPos, self.expected, self.pID, self.clanList, self.time], f)
    
    def getStats(self, name):
        with open(name, 'rb') as f:
            self.pPlayerShipStats, self.pPlayerOverall, self.pShipArrPos, self.pExpected, self.pPID, self.pClanList, self.ptime = pickle.load(f)
    
    def usePreLoaded(self, name):
        #binds previous stats to used global variables
        self.playerShipStats = self.pPlayerShipStats
        self.playerOverall = self.pPlayerOverall
        self.shipArrPos = self.pShipArrPos
        self.pExpected = self.pExpected
        self.pID = self.pPID
        self.clanList = self.pClanList
    
    def alignPastArray(self, prevData, cPlayers, pPlayers, cShipArr, pShipArr):
        aligned = np.full((len(cPlayers), len(cShipArr), 5), -1) # -1 means no value
        counter = 0
        cPD = {}
        for index in range(len(cPlayers)):
            cPD[cPlayers[index]] = index

        shipadj = np.full((len(pPlayers), len(cShipArr), 5), -1) #temporary array: place to dump the ship corrected prevData array
        #Aligns Ships
        for ship, pos in pShipArr:
            if ship in cShipArr:
                shipadj[:,cPlayers[ship],:] = prevData[:,pos,:]
        #Aligns Players
        for w in range(len(pPlayers)):
            if pPlayers[w] in cPlayers:
                aligned[cPlayers[pPlayers[w]],:,:] = shipadj[w,:,:]
        return aligned
    
    def calcRecent(self, name):
        self.updatePlayerExpected()
        self.getStats(name)

        self.time_difference = self.time - self.ptime

        aligned = self.alignPastArray(self.pPlayerShipStats, self.PID, self.pPID, self.shipArrPos, self.pShipArr)
        self.recent = np.where(aligned != -1, self.playerShipStats - aligned, 0)
        self.recent[:,:,4] = self.calcShipPR(aligned, self.expectedStats)
        self.recentOverall = self.calcPlayerOverall(difference, self.expectedStats)
    
    #Printing
    def getStats(self, stats, SN, minbattles):
        outlist = []
        pr = np.zeros((self.totalPlayers, 5))
        shape = stats.shape
        error = False
        if SN == None:
            if shape == (self.totalPlayers, 5):
                pr = np.where(self.playerOverall[:,0] >= minbattles,self.playerOverall[:,4],-1)
                outlist = self.produceList(pr)
            else:
                print('Incorrect Input array')
        else:
            if shape == (self.totalPlayers, self.shipLength, 5):
                if SN in self.SID:
                    SID = int(self.SID[SN])
                    #print(SID)
                    if SID in self.shipArrPos:
                        shippos = self.shipArrPos[SID]
                        pr = np.where(self.playerShipStats[:,shippos,0] >= minbattles,self.playerShipStats[:,shippos,4],-1)
                        outlist = self.produceList(pr)
                    else:
                        print('SID Not Found')
                else:
                    print('Ship Not Entried')
            else:
                print('Incorrect Input array')
        return outlist

    def produceList(self, pr):
        outlist = []
        for w in range(self.totalPlayers):
            if pr[w] != -1:
                pName, ci = self.pName[self.pID[w]]
                outlist.append([ci,pName,int(np.round(pr[w]))])
        return outlist

    def printStats(self, stats, SN=None, minbattles=-1):
        """
        SN - Ship Name
        Minbattles - Minimum Required Battles
        """
        outlist = self.getStats(stats, SN=SN,minbattles=minbattles) 
        if len(outlist) != 0:
            PRstrTag = 'PR'
            if SN != None:
                PRstrTag = SN + ' ' + PRstrTag
            
            if minbattles == -1:
                PRstrTag = PRstrTag + ': '
            else:
                PRstrTag = PRstrTag + ' (Minimum Battles: ' + str(minbattles) + '): '
            sortedlist = sorted(outlist, key=operator.itemgetter(2), reverse=True) #Sort by pr, clan, name
            #sortedlist = sorted(outlist, key=operator.itemgetter(0, 1)) #Sort by clan, name
            print(PRstrTag)
            for items in sortedlist:
                print('Clan: [' + self.clanList[items[0]] + '] Player Name: ' + items[1] + ' PR: ' + str(items[2]))
    
    def printStatsFromGlobal(self, SN=None, minbattles=-1):
        if SN==None:
            self.printStats(self.playerOverall, SN=SN, minbattles=minbattles)
        else:
            self.printStats(self.playerShipStats, SN=SN, minbattles=minbattles)
    
    def printStatsFromRecent(self, SN=None, minbattles=-1):
        if SN==None:
            self.printStats(self.recentOverall, SN=SN, minbattles=minbattles)
        else:
            self.printStats(self.recent, SN=SN, minbattles=minbattles)
    
    def findMissingShips(self):
        for shipid in self.nf:
            print(self.a.getShipName(shipid))
    
    def findStatLessShips(self):
        for shipid in self.ns:
            print(self.a.getShipName(shipid))

if (__name__ == '__main__'):
    clanstats = ClanStats(['MIA', 'MIA-P', 'MIA-E', 'MIA-I'])
    clanstats.updatePlayerExpected()
    clanstats.calcCurrent()
    #clanstats.printStats(minbattles=6000)
    clanstats.printStatsFromGlobal(minbattles=20)
    #clanstats.findMissingShips()








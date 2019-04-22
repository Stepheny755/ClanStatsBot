from ClanStats import ClanStats
from data import Data

d = Data()

clanstats = ClanStats(d.readClanList())
clanstats.updatePlayerExpected()
clanstats.calcCurrent()
clanstats.saveStats()

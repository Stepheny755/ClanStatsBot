from GPSC import ClanStats

clanstats = ClanStats(['MIA', 'MIA-P', 'MIA-E', 'MIA-I', 'MIA-C'])
clanstats.updatePlayerExpected()
clanstats.calcCurrent()
clanstats.saveStats()
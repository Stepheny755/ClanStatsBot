# import numpy as np
import json

import numpy as np
from API import API
from data import Data
from util import Util

class Stats():
    def __init__(self):
        pass

    expected = []

    def PRnormDmg(self,dmg,edmg):
        """
        Note: not average dmg, total dmg (per ship)
        To find edmg, multiply expected average damage by number of battles a player has played

        Parameters:
        dmg: actual damage
        edmg: expected damage

        Returns:
        normalized damage value (float)
        """
        return np.where(edmg > 0, np.maximum(0,(dmg / edmg-0.4)/(1.0-0.4)), 0)

        """
        - prev version
        if(edmg!=0):
            dmg/=edmg
        else:
            return 0
        nDmg = float(max(0,(dmg-0.4)/(1.0-0.4)))
        return nDmg
        """

    def PRnormWin(self,wins,ewins):
        """
        Note: not win rate, total wins (per ship)
        To find ewins, multiply expected WR by number of battles a player has played

        Parameters:
        wins: actual wins
        ewins: expected wins

        Returns:
        normalized WR value (float)
        """
        return np.where(ewins > 0, np.maximum(0,(wins/ewins-0.7)/(1.0-0.7)), 0)
        """
        if(ewins!=0):
            wins/=ewins
        else:
            return 0
        nWins = float(max(0,(wins-0.7)/(1.0-0.7)))
        return nWins
        """

    def PRnormKil(self,kills,ekills):
        """
        Note: not average kills, total kills (per ship)
        To find ekills, multiple expected average kills by number of battles a player has played

        Parameters:
        kills: actual kills
        ekills: expected kills

        Returns:
        normalized kills value (float)
        """
        return np.where(ekills > 0, np.maximum(0,(kills/ekills-0.1)/(1.0-0.1)), 0)
        """
        if(ekills!=0):
            kills/=ekills
        else:
            return 0
        nKills = float(max(0,(kills-0.1)/(1.0-0.1)))
        return nKills
        """

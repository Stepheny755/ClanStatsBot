# ClanStatsBot
###### Made by [MIA]Modulatus

A (WIP) World of Warships discord bot that mainly focuses on calculating and tracking changes in clan statistics :~)

## Data
All the data used in this bot is either retrieved from the Wargaming API for World of Warships, or the official wows-numbers website ([na.wows-numbers.com](https://wows-numbers.com))

PR Calculation Formula is provided by [na.wows-numbers.com](https://na.wows-numbers.com/personal/rating)

If you would like to copy the source code, you can [generate your own Wargamimg API ID](https://developers.wargaming.net/)

A couple of assumptions are made when taking statistics of players:
1. Individual player statistics are not hidden
2.

## Structure

* bot.py
  * stats.py
    * data.py
    * API.py
    * update.py
      * data.py
      * API.py
  * clan.py
  * player.py

* util.py

# ClanStatsBot
###### Made by [MIA]Modulatus,[MIA]enderland07,[MIA]901234

A (WIP) World of Warships discord bot that mainly focuses on calculating and tracking changes in clan statistics :~)

## Data
All the data used in this bot is either retrieved from the Wargaming API for World of Warships, or the official wows-numbers website ([na.wows-numbers.com](https://wows-numbers.com))

PR Calculation Formula is provided by [na.wows-numbers.com](https://na.wows-numbers.com/personal/rating)

A couple of assumptions are made when taking statistics of players:
1. Individual player statistics are not hidden
2. Players have played at least 1 battle in random battles/PvP
 

## Requirements

If you would like to copy the source code, you can [generate your own Wargamimg API ID](https://developers.wargaming.net/)
Use `pip3 install -r requirements.txt` to install required libraries

## Structure

* bot.py
  * update.py
  * post.py
     * stats.py
     * data.py
     * API.py

* util.py

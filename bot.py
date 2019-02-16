import discord
import asyncio
import time
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler
#from stats import Stats
from clan import Clan,Time
from API import API
from update import Update
from util import Util

token = open('token.txt',"r").read().strip()

RENAMETIME=1547524924
CDDUR = 2592000

client = discord.Client()

@client.event
async def on_read():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send(message.channel, 'Done sleeping')

    elif message.content.startswith('!available EST'):
        await client.send_message(message.channel,'Rename available at '+Time.available('EST')+' EST')

    elif message.content.startswith('!available PST'):
        await client.send_message(message.channel,'Rename available at '+Time.available('PST')+' PST')

    elif message.content.startswith('!available'):
        await client.send_message(message.channel,'Rename available at '+Time.available('UTC')+' UTC')

    #elif message.content.find("cv"):
        #await client.send_message(message.channel,'ree')

    #elif(int(message.content.find('cv'))>=0):
        #print(str(message.channel)+": "+message.content+" "+str(message.timestamp))
        #await client.send_message(message.channel,'ree')

    elif(message.content.startswith('cv')):
        await client.send_message(message.channel,'reee')

    elif(message.content.startswith('!stop')):
        exit()
        sys.exit()

    elif(message.content.startswith('!getID')):
        temp = message.content
        inputname = temp[7:]
        api = API()

        playerID = api.getPlayerID(inputname)
        playername = api.getPlayerName(playerID)

        ret = playername+"'s ID: "+str(playerID)
        await client.send_message(message.channel,ret)

    elif(message.content.startswith("!stats")):
        temp = message.content
        inputname = temp[7:]
        api = API()

        playerID = api.getPlayerID(inputname)
        playername = api.getPlayerName(playerID)
        playerstats = api.getPlayerStats(playerID)
        print(playerstats)

        ret = str(api.getPlayerStats(playerID))[:2000]
        await client.send_message(message.channel,ret)

    print(str(message.channel)+": "+message.content)

def scheduled_job():
    print("Updated Started")
    #TODO: send a discord message
    u = Update()
    u.saveExpValues()
    u.saveStats()
    t = Util()
    print("Update Finished: "+str(t.getGMTTime()))

if(__name__=="__main__"):
    sched = AsyncIOScheduler()
    sched.add_job(scheduled_job,'cron',hour=4,minute=20,timezone='UTC')
    sched.start()
    print("Scheduler Started")
    client.run(token)
    print("Bot Started")

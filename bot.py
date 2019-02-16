import discord
import asyncio
import time
import sys

#from stats import Stats
from clan import Clan,Time
from API import API
from update import Update

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

        playerID = api.getPlayerID(playername)
        playername = api.getPlayerName(playerID)

        ret = playername+"'s ID: "+playerID
        await client.send_message(message.channel,ret)

    print(str(message.channel)+": "+message.content)

if(__name__=="__main__"):
    sched = AsyncIOScheduler()
    sched.start()
    client.run(token)

@sched.scheduled_job('cron', hour=4, minute=20, timezone='UTC')
def scheduled_job():
    u = Update()
    u.saveExpValues()
    u.saveStats()
    t = Util()
    print("Update Finished: "+str(t.getGMTTime()))

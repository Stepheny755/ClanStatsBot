import discord
import asyncio
import time
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler
#from stats import Stats
from API import API
from update import Update
from util import Util
from post import Post

token = open('token.txt',"r").read().strip()

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

    elif(message.content.startswith('!embed')):
        temp = message.content
        input = temp[7:]
        await client.send_message(message.channel,str('Processing '+input+' Statistics'))
        a = API()
        if(len(a.getClanMembers(a.getClanID(input)))>25):
            embed0 = await postValues(input,0,10)
            await client.send_message(message.channel,embed=embed0)
            #embed1 = await postValues(input,25,50)
            #await client.send_message(message.channel,embed=embed1)
        else:
            embed = await postValues(input,0,25)
            await client.send_message(message.channel,embed=embed)

    print(str(message.channel)+": "+message.content)

async def postValues(clanname,start,end):
    start_time=time.time()
    embed = discord.Embed(description="Note: Colors only represent PR changes")
<<<<<<< HEAD
=======
    #TODO: Check member size to determine if multiple embeds are required
>>>>>>> a000fafb4bd121bedb74f58d8fad8008499843c5
    p = Post()
    a = API()
    u = Util()

    embed = p.createEmbed(clanname,embed,start,end)
    postname = "["+str(clanname)+"] "+a.getClanName(a.getClanID(clanname))+" Statistics"
    embed.set_author(name=postname, icon_url=client.user.default_avatar_url)
    runtime = "Runtime: "+str(u.round3(time.time()-start_time))+" Seconds"
    embed.set_footer(text=str(runtime))
    return embed


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
    print("Bot Started")
    client.run(token)

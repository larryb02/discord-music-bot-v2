import discord
from discord.ext import commands
import time 
import os
from dotenv import load_dotenv
import logging
import utils
import os


file = './secret.env' #THIS FILE DOESNT EXIST ANYMORE HAHAHAHAHA laptop broke >:(
load_dotenv(file)
logging.basicConfig(level=logging.INFO)


#TODO:
#inactivity = leave channel
#finish play command, probly need some helper functions (get link, stuff like that)
#add other functionalities i.e. actually play song, pause, skip
#also fix var naming convention/style need it to all be consistent


token = os.getenv('TOKEN')
class musicBot(commands.Bot):

    def __init__(self, *, command_prefix='$'):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=command_prefix, intents=intents)
        


client = musicBot()


@client.event
async def on_ready():
    print(f'{client.user} is online')
'''
play: plays music as queued by users

implementation:

Need a queue to store songs
Bot streams songs stored in queue
if queue is empty bot can leave (may add a timer for this)
'''
@client.command(name='play')
async def play(ctx, *, song):
    songQ = [] #probly gonna make this a class attr or something, so i can use in other places
    #bot joins user's channel
    try:
        channel = ctx.author.voice.channel
        print(f"{client.user} is joining {channel}!\n")
        await (channel.connect(timeout=60.0, reconnect=False) if ctx.voice_client is None else ctx.voice_client.move_to(channel))
    except AttributeError:
        await ctx.send(f"You must be in a voice channel to use this command!\ncurrent voice info: {ctx.author.voice}")
        return
    #add song to queue
    songQ.append(song)
    #streaming has its own caveats that i must handle
    link = utils.resolveLink(songQ.pop())
    ctx.send(f'Now Playing {link}')
    os.sleep(3)
    await ctx.voice_client.disconnect()




client.run(token)




     





     
     










    

   



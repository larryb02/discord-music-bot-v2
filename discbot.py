import discord
from discord.ext import commands
import time 
import os
from dotenv import load_dotenv
import logging


file = '../secrets/bot.env'
load_dotenv(file)
#logging.basicConfig(level=logging.INFO)
#intents = discord.Intents.default()
#intents.message_content = True


#TODO:
#inactivity = leave channel
#finish play command, probly need some helper functions (get link, stuff like that)
#add other functionalities i.e. actually play song, pause, skip


token = os.getenv('TOKEN')
class musicBot(commands.Bot):

    def __init__(self, *, command_prefix='$'):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=command_prefix, intents=intents)
        #self.tree = app_commands.CommandTree(self)


client = musicBot()


@client.event
async def on_ready():
    print(f'{client.user} is online')

@client.command(name='play')
async def join(ctx, *, song):
    try:
        channel = ctx.author.voice.channel
    except AttributeError:
        await ctx.send("You must be in a voice channel to use this command!")
        return
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    await channel.connect()
    #check for inactivity
    #next is call streaming function... need to make


def getTimeMilis(): #will possibly move this func somewhere else, doesnt make much sense here
    return time.time() * 1000




client.run(token)




     





     
     










    

   



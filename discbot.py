import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging


file = 'bot.env'
load_dotenv(file)
logging.basicConfig(level=logging.INFO)
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='>', intents=intents)

token = os.getenv('TOKEN')


@client.event
async def on_ready():
    print(f'{client.user} is online')

#play <song>
#stop 
#skip 


client.run(token)




     





     
     










    

   



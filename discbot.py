import discord
from discord.ext import commands
import time
import os
from dotenv import load_dotenv
import logging
import utils


file = "./secret.env"
load_dotenv(file)
logging.basicConfig(level=logging.INFO)
token = os.getenv("TOKEN")

# TODO:
# inactivity = leave channel
# add other functionalities i.e. actually play song, pause, skip


class musicBot(commands.Bot):
    Q = []

    def __init__(self, *, command_prefix="$"):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=command_prefix, intents=intents)


client = musicBot()


@client.event
async def on_ready():
    print(f"{client.user} is online")


"""

joinChannel:

Function made so bot joins the channel that ctx.author is in

"""


async def joinChannel(ctx):
    channel = ctx.author.voice.channel
    print(f"{client.user} is joining {channel}!\n")
    await (
        channel.connect(
            timeout=60.0, reconnect=False
        )  # doesnt seem to handle inactivity, will do later
    )
    if ctx.voice_client is None:
        ctx.voice_client.move_to(channel)


"""
play: plays music as queued by users

implementation:

Need a queue to store songs
Bot streams songs stored in queue
if queue is empty bot can leave (may add a timer for this)

TODO:

sit down and think about how to handle this queue,

"""


@client.command(name="play")
async def playSong(ctx, *, song):
    # bot joins user's channel
    try:
        await joinChannel(ctx)
        # Do Q stuff
        metaData = utils.resolveLink(song)
        songQ = client.Q
        songQ.append(metaData)  # for now add the entire dictionary
        # play song, pop from q
        cur = songQ.pop()
        await ctx.send(f"Now Playing {cur['title']}!\n{cur['readableUrl']}")
        src = discord.FFmpegOpusAudio(cur["streamableUrl"])
        ctx.voice_client.play(src, after=None)
    except AttributeError:
        await ctx.send(f"You must be in a voice channel to use this command!")
    # if list not empty
    # playSong(ctx, song=songQ[-1])


@client.command(name="leave")
async def leaveChannel(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()


client.run(token)

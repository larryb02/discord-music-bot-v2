#!/usr/bin/python3

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging
import yt_dlp
import asyncio

file = "./secret.env"
load_dotenv(file)
logging.basicConfig(level=logging.INFO)
token = os.getenv("TOKEN")

# TODO:
# add other functionalities: pause, skip, inactivity


class musicBot(commands.Bot):

    def __init__(self, *, command_prefix="$"):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.Q = list()

    async def resolveLink(self, query: str):
        ydl_opts = {
            "format": "worstaudio/worst",  # since i refuse to download files
            "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
            "restrictfilenames": True,
            "noplaylist": True,
            "nocheckcertificate": True,
            "ignoreerrors": False,
            "logtostderr": False,
            "quiet": True,
            "no_warnings": True,
            "default_search": "auto",
            "source_address": "0.0.0.0",
        }
        # need to append ytsearch to strings
        formattedQuery = f"ytsearch:{query}"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None, lambda: ydl.extract_info(formattedQuery, download=False)
            )
        # parts that i may want:
        title = results["entries"][0]["title"]
        extractedUrl = results["entries"][0]["webpage_url"]
        returnedUrl = results["entries"][0]["url"]
        info = {
            "title": title,
            "readableUrl": extractedUrl,  # readable link
            "streamableUrl": returnedUrl,  # streamable link
        }
        return info  # change this to return a tuple (metadata, FFmpegPCMAudio)

    """
    joinChannel:

    Function made so bot joins the channel that ctx.author is in

    """

    async def joinChannel(self, ctx, channel: discord.VoiceChannel):
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    """
    getNext:

    check for remaining songs and play them

    """

    async def getNext(self, ctx):
        if len(self.Q) > 0:
            ctx.voice_client.stop()
            cur = self.Q.pop(0)  # pop from top
            await self.stream(ctx, cur)
        else:
            async with ctx.typing():
                await ctx.send(f"Queue is empty")

    """
    stream:

    stream audio output

    """

    async def stream(self, ctx, data):
        # can handle opus here
        discord.opus.load_opus(
            "/opt/homebrew/Cellar/libopusenc/0.2.1/lib/libopusenc.0.dylib"
        )
        ffmpeg_options = {
            "options": "-vn",
        }
        async with ctx.typing():
            src = discord.FFmpegPCMAudio(data["streamableUrl"], **ffmpeg_options)
            ctx.voice_client.play(
                src, after=lambda e: client.loop.create_task(self.getNext(ctx))
            )
        await ctx.send(f"Now Playing {data['title']}!\n{data['readableUrl']}")

    async def addToQueue(self, ctx, song):
        async with ctx.typing():
            metadata = await self.resolveLink(song)
            self.Q.append(metadata)
            print([[song["title"], song["readableUrl"]] for song in self.Q])
        await ctx.send(f"{metadata['title']} has been added to queue")


client = musicBot()


@client.event
async def on_ready():
    print(f"{client.user} is online")


"""
    play: plays music as queued by users

"""


@client.command(name="play")
async def playSong(ctx, *, song):
    # bot joins user's channel
    try:
        await client.joinChannel(ctx, ctx.author.voice.channel)
    except AttributeError:
        await ctx.send(f"You must be in a voice channel to use this command!")
        return
    await client.addToQueue(ctx, song)
    if not ctx.voice_client.is_playing():
        cur = client.Q.pop()
        await client.stream(ctx, cur)


"""
leave:

bot leaves channel, need to cut loose ends
"""


@client.command(name="leave")
async def leaveChannel(ctx):
    if ctx.voice_client.is_connected():
        #clear q on disconnect
        client.Q = list()
        await ctx.voice_client.disconnect()
    else:
        ctx.send(f"I am currently not in a channel!")


"""
pause:

pause current song
"""
@client.command(name="pause")
async def pauseAudio(ctx):
    #only if audio is currently being played
    if ctx.voice_client.is_playing():
        ctx.voice_client.pause()
    else:
        async with ctx.typing():
            await ctx.send(f"Audio is already paused!!!")
    
"""
resume:

"""
@client.command(name="resume")
async def resumeAudio(ctx):
    if ctx.voice_client.is_paused():
        ctx.voice_client.resume()
    else:
        async with ctx.typing():
            await ctx.send(f"Audio is playing!!!")
            
"""
skip:

skips current song
"""
@client.command(name="skip")
async def skipSong(ctx):
    #stop output
    #getNext...
    async with ctx.typing():
        await ctx.send(f"Skipping Current Song") #be more specific later
        ctx.voice_client.stop()
    await client.getNext(ctx)
"""
list:

list current songs in queue
"""
# @client.command(name="queue")
# async def printQueue(): #once i figure out how to make this look nice ill write
#     pass
"""
remove:

remove a song from queue based on index
"""
@client.command(name="remove")
async def removeSong(ctx, index):
    #probably need to create a prompt showing the list
    pass
client.run(token)

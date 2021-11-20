import discord
from discord.utils import get
import youtube_dl
from discord.ext import commands
from discord import FFmpegPCMAudio

queue_list = []
YDL_OPTIONS = {'formats' : 'bestaudio', 'noplaylist' : 'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

class music_command(commands.Cog):
    
    def __init__(self, client):
        self.clinet = client
    @commands.command()
    async def check(self, ctx): # เช็คคิวเพลง
        voice_client = get(commands.voice_clients, guild=ctx.guild)
        await ctx.channel.send(queue_list)

    @commands.command()
    async def moveto(self, ctx): # ให้บอทมาห้องที่เราอยู่
        voice_client = get(commands.voice_clients, guild=ctx.guild)
        await voice_client.move_to(ctx.author.voice.channel)


    @commands.command()
    async def play(self, ctx, url): # ให้บอทเล่นเพลง ตาม url
        voice_client = get(commands.voice_clients, guild=ctx.guild)
        if ctx.author.voice == None:
            await ctx.channel.send("You are't in VC")
            return

        if voice_client == None:
            await ctx.author.voice.channel.connect()
        else:
            await voice_client.move_to(ctx.author.voice.channel)

        voice_client = get(commands.voice_clients, guild=ctx.guild)

        if not voice_client.is_playing():
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                URL = info['formats'][0]['url']
            voice_client.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda x=None: self.queued(ctx))
            voice_client.source = discord.PCMVolumeTransformer(voice_client.source,volume=0.1)
            voice_client.is_playing()
        else:
            queue_list.append(url)
            await ctx.channel.send("Added to queue")

    def queued(self, ctx): # ส่วนที่จะทำการเล่นเพลงในคิว
        if len(queue_list) > 0:
            voice_client = get(commands.voice_clients, guild=ctx.guild)
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(queue_list.pop(0), download=False)
                URL = info['formats'][0]['url']
            voice_client.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda x=None: self.queued(ctx))
            voice_client.source = discord.PCMVolumeTransformer(voice_client.source,volume=0.1)

    @commands.command()
    async def leave(self, ctx): # สั่งให้บอทออกจากห้อง
        voice_client = get(commands.voice_clients, guild=ctx.guild)

        if ctx.author.voice == None or ctx.author.voice.channel != voice_client.channel:
            await ctx.channel.send("You are't in VC")
            return
        if voice_client == None:
            await ctx.channel.send("Bot isn't in VC")
            return
        await ctx.voice_client.disconnect()

    @commands.command()
    async def pause(self, ctx): # สั่งให้บอทหยุดเล่นเหลง
        voice_client = get(commands.voice_clients, guild=ctx.guild)

        if ctx.author.voice == None or ctx.author.voice.channel != voice_client.channel:
            await ctx.channel.send("You aren't in VC")
            return
        if not voice_client.is_playing():
            await ctx.channel.send("Music isn't playing")
            return
        voice_client.pause()

    @commands.command()
    async def resume(self, ctx): # สั่งให้บอทเล่นเพลงต่อ
        voice_client = get(commands.voice_clients, guild=ctx.guild)

        if ctx.author.voice == None or ctx.author.voice.channel != voice_client.channel:
            await ctx.channel.send("You aren't in VC")
            return
        if not voice_client.is_paused():
            await ctx.channel.send("Music wasn't paused")
            return
        voice_client.resume()

    @commands.command()
    async def stop(self, ctx): # สั่งให้บอทลบเพลงทั้งหมด
        voice_client = get(commands.voice_clients, guild=ctx.guild)

        if ctx.author.voice == None or ctx.author.voice.channel != voice_client.channel:
            await ctx.channel.send("You aren't in VC")
            return
        if not voice_client.is_playing():
            await ctx.channel.send("Music isn't playing")
            return
        voice_client.stop()
        queue_list = []

    @commands.command()
    async def skip(self, ctx): # สั่งให้บอท ข้ามที่เล่นอยู่
        voice_client = get(commands.voice_clients, guild=ctx.guild)

        if ctx.author.voice == None or ctx.author.voice.channel != voice_client.channel:
            await ctx.channel.send("You aren't in VC")
            return
        if not voice_client.is_playing():
            await ctx.channel.send("Music isn't playing")
            return
        voice_client.stop()


def setup(client):
    client.add_cog(music_command(client))
    

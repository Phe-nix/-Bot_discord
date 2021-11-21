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
        self.client = client
    @commands.command()
    async def check(self, ctx): # เช็คคิวเพลง
        await ctx.channel.send(queue_list)

    @commands.command()
    async def moveto(self, ctx): # ให้บอทมาห้องที่เราอยู่
        voice_client = ctx.author.voice.channel
        await voice_client.move_to(ctx.author.voice.channel)


    @commands.command()
    async def play(self, ctx, url): # ให้บอทเล่นเพลง ตาม url
        vc = ctx.voice_client
        if ctx.author.voice == None:
            await ctx.channel.send("You are't in VC")
            return

        if vc == None:
            await ctx.author.voice.channel.connect()
        else:
            await vc.move_to(ctx.author.voice.channel)
        vc = ctx.voice_client
        if not vc.is_playing():
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                URL = info['formats'][0]['url']
            vc.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda x=None: self.queued(ctx))
            vc.source = discord.PCMVolumeTransformer(vc.source,volume=0.1)
        else:
            queue_list.append(url)
            await ctx.channel.send("Added to queue")

    def queued(self, ctx): # ส่วนที่จะทำการเล่นเพลงในคิว
        if len(queue_list) > 0:
            vc = ctx.voice_client
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(queue_list.pop(0), download=False)
                URL = info['formats'][0]['url']
            vc.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda x=None: self.queued(ctx))
            vc.source = discord.PCMVolumeTransformer(vc.source,volume=0.1)

    @commands.command()
    async def leave(self, ctx): # สั่งให้บอทออกจากห้อง
        await ctx.voice_client.disconnect()

    @commands.command()
    async def pause(self, ctx): # สั่งให้บอทหยุดเล่นเหลง
        vc = ctx.voice_client

        if ctx.author.voice == None or ctx.author.voice.channel != vc.channel:
            await ctx.channel.send("You aren't in VC")
            return
        if not vc.is_playing():
            await ctx.channel.send("Music isn't playing")
            return
        vc.pause()

    @commands.command()
    async def resume(self, ctx): # สั่งให้บอทเล่นเพลงต่อ
        vc = ctx.voice_client

        if ctx.author.voice == None or ctx.author.voice.channel != vc.channel:
            await ctx.channel.send("You aren't in VC")
            return
        if not vc.is_paused():
            await ctx.channel.send("Music wasn't paused")
            return
        vc.resume()

    @commands.command()
    async def stop(self, ctx): # สั่งให้บอทลบเพลงทั้งหมด
        vc = ctx.voice_client

        if ctx.author.voice == None or ctx.author.voice.channel != vc.channel:
            await ctx.channel.send("You aren't in VC")
            return
        if not vc.is_playing():
            await ctx.channel.send("Music isn't playing")
            return
        vc.stop()
        queue_list = []

    @commands.command()
    async def skip(self, ctx): # สั่งให้บอท ข้ามที่เล่นอยู่
        vc = ctx.voice_client
        if ctx.author.voice == None or ctx.author.voice.channel != vc.channel:
            await ctx.channel.send("You aren't in VC")
            return
        if not vc.is_playing():
            await ctx.channel.send("Music isn't playing")
            return
        vc.stop()

def setup(client):
    client.add_cog(music_command(client))
    

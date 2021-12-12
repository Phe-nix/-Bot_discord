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
    async def moveto(self, ctx): # ให้บอทมาห้องที่เราอยู่
        voice_client = ctx.author.voice.channel
        if ctx.author.voice == None:# ถ้าผู้ใช้ไม่ได้อยู่ในห้อง
            await ctx.channel.send("คุณไม่ได้อยู่ในห้อง")# ส่งข้อความ
            return
        await voice_client.move_to(ctx.author.voice.channel)# ให้ botมาห้องที่เราอยู่


    @commands.command()
    async def play(self, ctx, url): # ให้บอทเล่นเพลง ตาม url
        vc = ctx.voice_client
        if ctx.author.voice == None:# ถ้าผู้ใช้ไม่ได้อยู่ในห้อง
            await ctx.channel.send("คุณไม่ได้อยู่ในห้อง")# ส่งข้อความ
            return
        if vc == None:# ถ้า botไม่ได้อยู่ในห้อง
            await ctx.author.voice.channel.connect()
        else:# ถ้าไม่ ย้าย botมาอยู่ห้องเดียวกับผู้ใช้
            await vc.move_to(ctx.author.voice.channel)
        vc = ctx.voice_client
        if not vc.is_playing():# ถ้าเพลงไม่ได้เปิดอยู่
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                URL = info['formats'][0]['url']
            vc.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda x=None: self.queued(ctx))# สั่งให้ botเปิดเพลงตามลิ้ง URL
            vc.source = discord.PCMVolumeTransformer(vc.source,volume=0.1)# ตั้งระดับเสียงที่ 0.1
        else:# ถ้ามีเพลงเปิดอยู่แล้ว
            queue_list.append(url)# เพิ่มเพลงลงไปในคิว
            await ctx.channel.send("เพิ่มเพลงเรียบร้อย")# ส่งข้อความ

    def queued(self, ctx): # ส่วนที่จะทำการเล่นเพลงในคิว
        if len(queue_list) > 0: # ถ้ามีคิว
            vc = ctx.voice_client
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(queue_list.pop(0), download=False)
                URL = info['formats'][0]['url']
            vc.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda x=None: self.queued(ctx))# สั่งให้ botเปิดเพลงตามลิ้ง URL
            vc.source = discord.PCMVolumeTransformer(vc.source,volume=0.1)# ตั้งระดับเสียงที่ 0.1

    @commands.command()
    async def leave(self, ctx): # สั่งให้บอทออกจากห้อง
        if ctx.author.voice == None or ctx.author.voice.channel != vc.channel:# ถ้า ผู้ใช้ไม่ได้อยู่ในห้อง หรือ botไม่ได้อยู่ห้องเดียวกันกับผู้ใช้
            await ctx.channel.send("คุณไม่ได้อยู่ในห้อง")# ส่งข้อความ
            return
        await ctx.voice_client.disconnect()# สั่งให้ botจากห้อง

    @commands.command()
    async def pause(self, ctx): # สั่งให้บอทหยุดเล่นเหลง
        vc = ctx.voice_client
        if ctx.author.voice == None or ctx.author.voice.channel != vc.channel:# ถ้า ผู้ใช้ไม่ได้อยู่ในห้อง หรือ botไม่ได้อยู่ห้องเดียวกันกับผู้ใช้
            await ctx.channel.send("คุณไม่ได้อยู่ในห้อง")# ส่งข้อความ
            return
        if not vc.is_playing():# ถ้าเพลงไม่ได้เล่นอยู่
            await ctx.channel.send("เพลงไม่ได้เปิดอยู่")# ส่งข้อความ
            return
        vc.pause()# สั่งหยุดเล่นเพลง

    @commands.command()
    async def resume(self, ctx): # สั่งให้บอทเล่นเพลงต่อ
        vc = ctx.voice_client
        if ctx.author.voice == None or ctx.author.voice.channel != vc.channel:# ถ้า ผู้ใช้ไม่ได้อยู่ในห้อง หรือ botไม่ได้อยู่ห้องเดียวกันกับผู้ใช้
            await ctx.channel.send("คุณไม่ได้อยู่ในห้อง")# ส่งข้อความ
            return
        if not vc.is_paused():# ถ้าเพลงไม่ได้หยุด
            await ctx.channel.send("เพลงไม่ได้หยุดอยู่")# ส่งข้อความ
            return
        vc.resume()# สั่งให้เเพลงเปิดต่อ

    @commands.command()
    async def stop(self, ctx): # สั่งให้บอทลบเพลงทั้งหมด
        vc = ctx.voice_client
        if ctx.author.voice == None or ctx.author.voice.channel != vc.channel:# ถ้า ผู้ใช้ไม่ได้อยู่ในห้อง หรือ botไม่ได้อยู่ห้องเดียวกันกับผู้ใช้
            await ctx.channel.send("คุณไม่ได้อยู่ในห้อง")# ส่งข้อความ
            return
        if not vc.is_playing():# ถ้าเพลงไม่ได้เล่นอยู่
            await ctx.channel.send("เพลงไม่ได้เปิดอยู่")# ส่งข้อความ
            return
        vc.stop()# สั่งหยุดเล่นเพลง และลบทิ้ง
        queue_list = []# ลบคิวที่มีอยู่ออกทั้งหมด

    @commands.command()
    async def skip(self, ctx): # สั่งให้บอท ข้ามที่เล่นอยู่
        vc = ctx.voice_client
        if ctx.author.voice == None or ctx.author.voice.channel != vc.channel:# ถ้า ผู้ใช้ไม่ได้อยู่ในห้อง หรือ botไม่ได้อยู่ห้องเดียวกันกับผู้ใช้
            await ctx.channel.send("คุณไม่ได้อยู่ในห้อง")# ส่งข้อความ
            return
        if not vc.is_playing():# ถ้าเพลงไม่ได้เล่นอยู่
            await ctx.channel.send("เพลงไม่ได้เปิดอยู่")# ส่งข้อความ
            return
        vc.stop()# สั่งหยุดเล่นเพลง และลบทิ้ง

def setup(client):
    client.add_cog(music_command(client))

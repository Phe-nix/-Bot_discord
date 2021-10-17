import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.') # คำหน้าเพื่อเรียก bot

@client.event
async def ping(): # เช็คว่า bot มันกำลังทำงาน
    print('Bot is ready.')

@client.command()
async def ping(ctx): # ฟังชันก์ เช็คปิง ของ ผู้ใช้ (ยังมีปัญหา)
    await ctx.send(f'Ping: {round(client.latency * 1000)} ms')

client.run('TOKEN') # TOKEN ของ Bot

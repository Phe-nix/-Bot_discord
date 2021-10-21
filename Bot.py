import asyncio
from asyncio.tasks import wait
import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.') # คำหน้าเพื่อเรียก bot

@client.event
async def ping(): # เช็คว่า bot มันกำลังทำงาน
    print('Bot is ready.')

@client.command()
async def ping(ctx): # ฟังชันก์ เช็คปิง ของ ผู้ใช้ (ยังมีปัญหา)
    await ctx.send(f'Ping: {round(client.latency * 1000)} ms')
    # check spammer 
@client.event
async def on_ready():
    print("ready")
    while True:
        print("cleanred")
        await asyncio.sleep(10)
        with open("spam_detect.txt", "r+") as file:
            file.truncate(0)

@client.event
async def on_message(message):
    counter = 0
    with open("spam_detect.txt", "r+") as file:
        for lines in file:
            if lines.strip("\n") == str(message.author.id):
                counter += 1

        file.writelines(f"{str(message.author.id)}\n")
        if counter > 5:
            await message.guild.ban(message.author, reason="spam")
            await asyncio.sleep(1)
            await message.guild.unban(message.author)
            print("u are doommmmmm!!")
            
client.run('TOKEN') # TOKEN ของ Bot

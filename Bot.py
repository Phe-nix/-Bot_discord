import discord
import random
from discord import mentions
from discord import user
# import เพลง
from discord.utils import get
import youtube_dl
from discord.ext import commands
from discord import FFmpegPCMAudio
from googleapiclient.discovery import build
##########################
# ใช่ย่อ TOKEN ######
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TOKEN')
############################
client = commands.Bot(command_prefix='.', help_command=None) # คำหน้าเพื่อเรียก bot
@client.event
async def on_ready():
    print(f'Logged in as {client.user}.\n-----------')


@client.command()
async def poll(ctx,*,message):
    print("Poll's working")
    emb = discord.Embed(title = ' POLL', description = f'{message}')
    msg = await ctx.channel.send(embed = emb)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')
##############################################
api_key = "AIzaSyBZo45hMPWVPH0dvQ8ph73kRrxtS0E8MvQ"

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
@client.command(aliases=["show"])
async def showpic(ctx,*,search):
    ran = random.randint(0,9)
    resource = build("customsearch","v1",developerKey=api_key).cse()
    result = resource.list(q=f"{search}", cx="a3f26f1f654bd09c3", searchType="image").execute()
    url = result["items"][ran]["link"]
    embed1 = discord.Embed(title=f"Here Your Image ({search.title()})")
    embed1.set_image(url=url)
    await ctx.send(embed=embed1)

##############################################
# Game tictactoe

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send(" <@" + str(player1.id) + "> เริ่มก่อนน")
        elif num == 2:
            turn = player2
            await ctx.send(" <@" + str(player2.id) + "> เริ่มก่อนน")
    else:
        await ctx.send("เกมเริ่มอยู่ รอให้จบก่อนนะจ้ะ")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " เป็นผู้ชนะ")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("เสมออจร้าาาา")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("ต้องใส่เลข 1-9 นะ เช่น .place 2 (ช่องที่ 2)")
        else:
            await ctx.send("ไม่ใช่ตาของเธอน้าาา")
    else:
        await ctx.send("กรุณาพิมคำสั่งเริ่ม !tictactoe ")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("ต้องมีผู้เล่นสองคน")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("ต้องใช้ \"@ชื่อ\" น้าาา")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("เรียกตำแหน่งที่จะใส่ด้วย!!!")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("ใส่เลขที่เป็นจำนวนเต็มโว้ยยยยยย!!!")


##############################################
queue_list = []
YDL_OPTIONS = {'formats' : 'bestaudio', 'noplaylist' : 'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

@client.event
async def on_ready(): # เช็คว่า bot มันกำลังทำงาน
    print('Bot is ready.')

@client.command()
async def check(ctx): # เช็คคิวเพลง
    voice_client = get(client.voice_clients, guild=ctx.guild)
    await ctx.channel.send(queue_list)

@client.command()
async def moveto(ctx): # ให้บอทมาห้องที่เราอยู่
    voice_client = get(client.voice_clients, guild=ctx.guild)
    await voice_client.move_to(ctx.author.voice.channel)


@client.command()
async def play(ctx, url): # ให้บอทเล่นเพลง ตาม url
    voice_client = get(client.voice_clients, guild=ctx.guild)
    if ctx.author.voice == None:
        await ctx.channel.send("You are't in VC")
        return

    if voice_client == None:
        await ctx.author.voice.channel.connect()
    else:
        await voice_client.move_to(ctx.author.voice.channel)

    voice_client = get(client.voice_clients, guild=ctx.guild)

    if not voice_client.is_playing():
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda x=None: queued(ctx))
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source,volume=0.1)
        voice_client.is_playing()
    else:
        queue_list.append(url)
        await ctx.channel.send("Added to queue")

def queued(ctx): # ส่วนที่จะทำการเล่นเพลงในคิว
    if len(queue_list) > 0:
        voice_client = get(client.voice_clients, guild=ctx.guild)
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(queue_list.pop(0), download=False)
            URL = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda x=None: queued(ctx))
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source,volume=0.1)

@client.command()
async def leave(ctx): # สั่งให้บอทออกจากห้อง
    voice_client = get(client.voice_clients, guild=ctx.guild)

    if ctx.author.voice == None or ctx.author.voice.channel != voice_client.channel:
        await ctx.channel.send("You are't in VC")
        return
    if voice_client == None:
        await ctx.channel.send("Bot isn't in VC")
        return
    await ctx.voice_client.disconnect()

@client.command()
async def pause(ctx): # สั่งให้บอทหยุดเล่นเหลง
    voice_client = get(client.voice_clients, guild=ctx.guild)

    if ctx.author.voice == None or ctx.author.voice.channel != voice_client.channel:
        await ctx.channel.send("You aren't in VC")
        return
    if not voice_client.is_playing():
        await ctx.channel.send("Music isn't playing")
        return
    voice_client.pause()

@client.command()
async def resume(ctx): # สั่งให้บอทเล่นเพลงต่อ
    voice_client = get(client.voice_clients, guild=ctx.guild)

    if ctx.author.voice == None or ctx.author.voice.channel != voice_client.channel:
        await ctx.channel.send("You aren't in VC")
        return
    if not voice_client.is_paused():
        await ctx.channel.send("Music wasn't paused")
        return
    voice_client.resume()

@client.command()
async def stop(ctx): # สั่งให้บอทลบเพลงทั้งหมด
    voice_client = get(client.voice_clients, guild=ctx.guild)

    if ctx.author.voice == None or ctx.author.voice.channel != voice_client.channel:
        await ctx.channel.send("You aren't in VC")
        return
    if not voice_client.is_playing():
        await ctx.channel.send("Music isn't playing")
        return
    voice_client.stop()
    queue_list = []

@client.command()
async def skip(ctx): # สั่งให้บอท ข้ามที่เล่นอยู่
    voice_client = get(client.voice_clients, guild=ctx.guild)

    if ctx.author.voice == None or ctx.author.voice.channel != voice_client.channel:
        await ctx.channel.send("You aren't in VC")
        return
    if not voice_client.is_playing():
        await ctx.channel.send("Music isn't playing")
        return
    voice_client.stop()

############################
@client.command()
async def clear(ctx, amount=5): #ลบข้อความ nข้อความ
    await ctx.channel.purge(limit=amount)
############################
##### Guessing word game 
#words = ['computer', 'apple'] # คำทั้งหมด
#word = random.choice(words)
#spaces = ['_'] * len(word)
#@client.command()
#async def wordgame(ctx):
#    embed = discord.Embed(title="ทายสิว่าคำนี้คืออะไร?", description=spaces, color=0xFF5733)
#    embed.set_footer(text="test : %s"%(word))
#    await ctx.send(embed=embed)
#
#def  get_letter_position(guess, word, spaces):
#    """ใส่คำลงในช่อง"""
#    index = -2
#    while index != -1:
#        if guess in word:
#            index = word.find(guess)
#
#            removed_character = '*'
#            word = word[:index]+removed_character+word[index+1:]
#            spaces[index] = guess
#        else:
#            index = -1
#
#    return(word, spaces)
#
#def win_check():
#    for i in range(0, len(spaces)):
#        if spaces[i] == '_':
#            return -1
#
#    return 1
#
#@client.command()
#async def word(ctx, message):
#    global word
#    global spaces
#    guess = message
#    if guess in word:
#        word, spaces = get_letter_position(guess, word, spaces)
#        embed = discord.Embed(title="ทายสิว่าคำนี้คืออะไร?", description=spaces, color=0xFF5733)
#        await ctx.send(embed=embed)
#    else:
#        await ctx.sent("ไม่ใช่ตัว" + message + "นะ")
#    if win_check() == 1:
#        await ctx.sent('เย้ยยย เกมจบแล้ววว ยินดีด้วย')
#
@bot.command()
async def help(ctx):
    emBed = discord.Embed(title="อกหักอย่าถามเยอะ", description="รู้แล้วก็รีบไป", color=0xffff00)
    emBed.add_field(name="help", value="ช่วยเท่าที่ไหวนะ", inline=False)
    emBed.add_field(name="poll", value="ข้าจะสร้างทางเลือกให้เจ้า", inline=False)
    emBed.add_field(name="show", value="อยากเห็นอะๆรของข้ารึ", inline=False)
    emBed.add_field(name="tictactoe", value="XO อย่าลืม @p1 @p2", inline=False)
    emBed.add_field(name="place", value="วางตำแหน่งXOยังไงหละะ", inline=False)
    emBed.add_field(name="play", value="ma ma sing a song", inline=False)
    emBed.add_field(name="pause", value="หยุดเพลงแปป", inline=False)
    emBed.add_field(name="resume", value="มาๆ เล่นเพลงต่อ", inline=False)
    emBed.add_field(name="stop", value="stop sing a songg", inline=False)
    emBed.add_field(name="skip", value="เบื่อเพลงที่เปิดอยู่เนี่ย ข้ามไปนะ", inline=False)
    emBed.set_thumbnail(url="https://f.ptcdn.info/836/037/000/nyjdgsn6287E8tipq7m-o.jpg")
    await ctx.channel.send(embed=emBed)
    
client.run(token) # TOKEN ของ Bot

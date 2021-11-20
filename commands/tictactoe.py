import discord
from discord.ext import commands
import random


class tictactoe_command(commands.Cog):

    def __init__(self, clinet): 
        self.clinet = clinet
 
    
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

    @commands.command()
    async def tictactoe(self, ctx, p1: discord.Member, p2: discord.Member):
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

    @commands.command()
    async def place(self, ctx, pos: int):
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

                    self.checkWinner(winningConditions, mark)
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
    def checkWinner(self, winningConditions, mark):
        global gameOver
        for condition in winningConditions:
            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                gameOver = True
    @tictactoe.error
    async def tictactoe_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("ต้องมีผู้เล่นสองคน")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("ต้องใช้ \"@ชื่อ\" น้าาา")

    @place.error
    async def place_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("เรียกตำแหน่งที่จะใส่ด้วย!!!")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("ใส่เลขที่เป็นจำนวนเต็มโว้ยยยยยย!!!")


def setup(client):
    client.add_cog(tictactoe_command(client))


from discord.ext import commands
import random
import math

class guess_game(commands.Cog):
    """Commands for Guessing Right Number"""

    def __init__(self, client):
        self.client = client

    lower_bound = 1
    upper_bound = 10

    check_number = round(random.randint(lower_bound, upper_bound))  # สุ่มเลข.
    rounds_number = round(math.log(upper_bound - lower_bound + 1,
                                   2))  # สุ่มหยิบเลขมา

    
    count = 0

    @commands.command()
    async def bound(self, ctx, lower: int,upper: int): # ตั้งค่าเลขต้น และ เลขท้าย
        # ถ้าไม่ตั้ง เลขจะเป็นแบบ 1-10
        #lower_bound = 1
        #upper_bound = 10

        if lower < upper:
            # เปลี่ยนค่า bound
            guess_game.lower_bound = lower
            guess_game.upper_bound = upper

            # สุ่มใหม่
            guess_game.check_number = round(random.randint(guess_game.lower_bound, guess_game.upper_bound))  # Get random number.
            guess_game.rounds_number = round(math.log(guess_game.upper_bound - guess_game.lower_bound + 1,2))  # Get random number of rounds.

            await ctx.send(f'เลขต่ำสุดและสูงสุด: {guess_game.lower_bound} , {guess_game.upper_bound}\n เริ่มเกมได้เลยย', delete_after=40)

        elif lower > upper:
            await ctx.send(f'การ set bound ผิดผลาด', delete_after=30)

    # เริ่มเกม
    @commands.command()
    async def start(self, ctx):
        await ctx.send(f'ลองทายเลขระหว่าง {guess_game.lower_bound}-{guess_game.upper_bound}.\nพิม ".guess" เพื่อทายนะ \n โชคดี!', delete_after=30)


    @commands.command()
    async def guess(self, ctx, guess_number: int):
        await ctx.send(f'Bounds: {guess_game.lower_bound}, {guess_game.upper_bound}', delete_after=30) 

        check_number = guess_game.check_number
        rounds_number = guess_game.rounds_number

        guess_game.count += 1

        if check_number == guess_number:
            await ctx.send(f'ยินดีด้วยยย พวกคุณทายไป {guess_game.count} ครั้ง!!  นายทายเลข {guess_number}.\n')
            guess_game.count -= rounds_number 
        elif check_number > guess_number:
            await ctx.send(f'พวกนายทายต่ำไปนะ  ลองทายใหม่ เหลือ {rounds_number - guess_game.count} ครั้ง ', delete_after=30)
        elif check_number < guess_number:
            await ctx.send(f'พวกนายทายสูงไปนะ  ลองทายใหม่ เหลือ {rounds_number - guess_game.count} ครั้ง', delete_after=30)
        if guess_game.count >= rounds_number:
            await ctx.send(f'ว้าาาา แย่จัง คำตอบคือเลข {check_number}. ไว้เรามาเล่นกันใหม่นะ')


    # รี bot 
    @commands.command()
    async def reset(self, ctx):
        guess_game.lower_bound = 1
        guess_game.upper_bound = 10

        guess_game.check_number = round(random.randint(guess_game.lower_bound, guess_game.upper_bound)) 
        guess_game.rounds_number = round(math.log(guess_game.upper_bound - guess_game.lower_bound + 1,
                                       2)) 

        guess_game.count = 0

        await ctx.send(f'reset เลขเสร็จแล้วว เล่นได้เลยย (.start เพื่อเริ่มน้าา)')

def setup(client):
    client.add_cog(guess_game(client))
    

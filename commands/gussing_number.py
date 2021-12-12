from discord.ext import commands
import random
import math

class guess_game(commands.Cog):
    """Commands for Guessing Right Number"""

    def __init__(self, client):
        self.client = client

    lower_bound = 1# กำหนดขอบล่างเท่ากับ 1
    upper_bound = 10# กำหนดขอบบนเท่ากับ 10

    check_number = round(random.randint(lower_bound, upper_bound))  # สุ่มเลขที่เป็นคำตอบ
    rounds_number = round(math.log(upper_bound - lower_bound + 1, 2))  # กำหนดรอบในการทาย

    
    count = 0

    @commands.command()
    async def bound(self, ctx, lower: int,upper: int): # ตั้งค่าเลขต้น และ เลขท้าย
        # ถ้าไม่ตั้ง เลขจะเป็นแบบ 1-10
        # lower_bound = 1
        # upper_bound = 10

        if lower < upper:
            # เปลี่ยนค่าขอบล่าง และขอบบน
            guess_game.lower_bound = lower
            guess_game.upper_bound = upper

            # สุ่มใหม่
            guess_game.check_number = round(random.randint(guess_game.lower_bound, guess_game.upper_bound))# สุ่มเลขที่เป็นคำตอบ
            guess_game.rounds_number = round(math.log(guess_game.upper_bound - guess_game.lower_bound + 1, 2))# กำหนดจำนวนรอบที่ให้ทาย

            await ctx.send(f'เลขต่ำสุดและสูงสุด: {guess_game.lower_bound} , {guess_game.upper_bound}\n เริ่มเกมได้เลยย', delete_after=40)# ส่งข้อความ และลบตัวเองใน 40วินาที

        elif lower > upper:# ถ้าขอบล่างมีค่ามากกว่าขอบบน
            await ctx.send(f'การ set bound ผิดผลาด', delete_after=30)# ส่งข้อความ และลบตัวเองใน 30วินาที

    # เริ่มเกม
    @commands.command()
    async def start(self, ctx):
        await ctx.send(f'ลองทายเลขระหว่าง {guess_game.lower_bound}-{guess_game.upper_bound}.\nพิม ".guess" เพื่อทายนะ \n โชคดี!', delete_after=30)# ส่งข้อความ และลบตัวเองใน 30วินาที


    @commands.command()
    async def guess(self, ctx, guess_number: int):
        await ctx.send(f'Bounds: {guess_game.lower_bound}, {guess_game.upper_bound}', delete_after=30)# ส่งข้อความ และลบตัวเองใน 30วินาที

        check_number = guess_game.check_number# กำหนดเลขที่เป็นคำตอบ
        rounds_number = guess_game.rounds_number# กำหนดรอบในการทาย

        guess_game.count += 1# เพิ่มจำนวนรอบที่ทายไปแล้ว 1

        if check_number == guess_number:# ถ้าเลขที่ทายเท่ากับเลขที่เป็นคำตอบ
            await ctx.send(f'ยินดีด้วยยย พวกคุณทายไป {guess_game.count} ครั้ง!!  นายทายเลข {guess_number}.\n')# ส่งข้อความ
            guess_game.count -= rounds_number# ปรับค่าของจำนวนรอบที่ทายแล้ว โดยการลบด้วยจำนวนรอบที่ให้ทาย
        elif check_number > guess_number:# ถ้าเลขที่ทายมากกว่าเลขที่เป็นคำตอบ
            await ctx.send(f'พวกนายทายต่ำไปนะ  ลองทายใหม่ เหลือ {rounds_number - guess_game.count} ครั้ง ', delete_after=30)# ส่งข้อความ
        elif check_number < guess_number:# ถ้าเลขที่ทายน้อยกว่าเลขที่เป็นคำตอบ
            await ctx.send(f'พวกนายทายสูงไปนะ  ลองทายใหม่ เหลือ {rounds_number - guess_game.count} ครั้ง', delete_after=30)# ส่งข้อความ
        if guess_game.count >= rounds_number:# ถ้าจำนวนรอบที่ทายไปแล้วมากกว่าเท่ากับจำนวนรอบที่ให้ทาย
            await ctx.send(f'ว้าาาา แย่จัง คำตอบคือเลข {check_number}. ไว้เรามาเล่นกันใหม่นะ')# ส่งข้อความ


    # รี bot 
    @commands.command()
    async def reset(self, ctx):
        guess_game.lower_bound = 1# กำหนดขอบล่างเท่ากับ 1
        guess_game.upper_bound = 10# กำหนดขอบล่างเท่ากับ 10

        guess_game.check_number = round(random.randint(guess_game.lower_bound, guess_game.upper_bound))# สุ่มเลขที่เป็นคำตอบ
        guess_game.rounds_number = round(math.log(guess_game.upper_bound - guess_game.lower_bound + 1, 2))# กำหนดจำนวนรอบที่ให้ทาย

        guess_game.count = 0# กำหนดจำนวนรอบที่ทายไปแล้วให้เท่ากับ 0

        await ctx.send(f'reset เลขเสร็จแล้วว เล่นได้เลยย (.start เพื่อเริ่มน้าา)')# ส่งข้อความ

def setup(client):
    client.add_cog(guess_game(client))
    

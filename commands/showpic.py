import discord
from discord.ext import commands
from googleapiclient.discovery import build
import random

api_key = "AIzaSyBZo45hMPWVPH0dvQ8ph73kRrxtS0E8MvQ"

class showpic_command(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["show"])
    async def showpic(self, ctx, *, search):
        ran = random.randint(0,9)
        resource = build("customsearch","v1",developerKey=api_key).cse()
        result = resource.list(q=f"{search}", cx="a3f26f1f654bd09c3", searchType="image").execute()
        url = result["items"][ran]["link"]
        embed1 = discord.Embed(title=f"Here Your Image ({search.title()})")
        embed1.set_image(url=url)
        await ctx.send(embed=embed1)

def setup(client):
    client.add_cog(showpic_command(client))

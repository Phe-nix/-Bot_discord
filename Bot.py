import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')

# คำหน้าเพื่อเรียก bot
client = commands.Bot(command_prefix='.')


class main(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Greetings
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.client.user} ({self.client.user.id})')
        
    # Reconnect
    @commands.Cog.listener()
    async def on_resumed(self):
        print('Bot has reconnected!')

    # Error Handlers
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Uncomment line 26 for printing debug
        # await ctx.send(error)

        # Unknown command
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Invalid Command!')

        # Bot does not have permission
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('Bot Permission Missing!')
    #ลบข้อความ nข้อความ
    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        await ctx.channel.send("ข้อความถูกลบเรียบร้อยแล้ว", delete_after=5)

if __name__ == '__main__':
    # Load extension
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            client.load_extension(f'commands.{filename[: -3]}')

    client.add_cog(main(client))
    client.run(token) # TOKEN ของ Bot
    

import discord
import random
import functools
import json
import os
from discord.ext import commands
from discord.ext import tasks

# class Utility(commands.Cog, name="Utility"):
#     def __init__(self, bot):
#         self.bot = bot
#         self.prevTrog = None
#         self.path = os.path.dirname(__file__) + '/../roles.json'
#         self.roleFile = open(self.path, 'r')
#         self.roleDict  = json.loads(self.roleFile.read())
#         self.roleFile.close()
#         self.trogOTD.start()

#     @commands.command(name='roll', help='A command for rolling a specified number of dices with a specified number of sides', brief='A command for rolling dice', usage='{number of dices} {number of sides of each dice}')
#     async def rollDice(self, ctx, diceNum : int, sidesNum : int):
#         if(diceNum > 30):
#             await ctx.send('Sorry, max value for the number of dice is 30!')
#             return
#         if(sidesNum > 30):
#             await ctx.send('Sorry max value for the number of dice is 30!')
#             return
#         if(ctx.channel.name=="command-spam"):
#             result = [str(random.choice(range(1, sidesNum + 1))) for _ in range(diceNum)]
#             msgDices = 'Individual dices: ' + ', '.join(result)
#             msgTotal = 'Total roll value: ' + str(functools.reduce(lambda a, b: int(a) + int(b), result))
#             await ctx.send(msgDices+"\n\n"+msgTotal)

#     @tasks.loop(hours=24.0)
#     async def trogOTD(self):
#         await self.bot.wait_until_ready()
#         guild = discord.utils.get(self.bot.guilds, name='Dankinton')
#         member = random.choice(guild.members)
#         while(discord.utils.get(member.roles, id=self.roleDict['Lvl 10 Boss']) == None and discord.utils.get(member.roles, id=self.roleDict['Lvl 100 Mafia Warlord']) == None):
#             member = random.choice(guild.members)
#         print(f'{member.name} has been chosen to be today\'s trog!')
#         await member.add_roles(guild.get_role(self.roleDict['Trog']))
#         ctx = discord.utils.get(guild.channels, name='command-spam')
#         await ctx.send(content=f'{member.name}({member.mention}) is today\'s trog!')
#         if(self.prevTrog != None):
#             await self.prevTrog.remove_roles(guild.get_role(self.roleDict['Trog']))
#         self.prevTrog = member

class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.prevTrog = None
        self.path = os.path.dirname(__file__) + '/../roles_test.json'
        self.roleFile = open(self.path, 'r')
        self.roleDict  = json.loads(self.roleFile.read())
        self.roleFile.close()
        self.trogOTD.start()

    @app_commands.command(name="roll")
    async def rollDice(self, interaction: discord.Interaction, diceNum : int, sidesNum : int):
        if(diceNum > 30):
            await interaction.response.send_message('Sorry, max value for the number of dice is 30!')
            return
        if(sidesNum > 30):
            await interaction.response.send_message('Sorry max value for the number of dice is 30!')
            return
        if(interaction.channel.name=="command-spam"):
            result = [str(random.choice(range(1, sidesNum + 1))) for _ in range(diceNum)]
            msgDices = 'Individual dices: ' + ', '.join(result)
            msgTotal = 'Total roll value: ' + str(functools.reduce(lambda a, b: int(a) + int(b), result))
            await interaction.response.send_message(msgDices+"\n\n"+msgTotal)

    @app_commands.command(name="close")
    @app_commands.default_permissions(administrator=True)
    async def close(self):
        await self.bot.close()


    @tasks.loop(hours=24.0)
    async def trogOTD(self):
        await self.bot.wait_until_ready()
        guild = discord.utils.get(self.bot.guilds, name='Dankinton')
        member = random.choice(guild.members)
        while(discord.utils.get(member.roles, id=self.roleDict['Lvl 10 Boss']) == None and discord.utils.get(member.roles, id=self.roleDict['Lvl 100 Mafia Warlord']) == None):
            member = random.choice(guild.members)
        print(f'{member.name} has been chosen to be today\'s trog!')
        await member.add_roles(guild.get_role(self.roleDict['Trog']))
        ctx = discord.utils.get(guild.channels, name='command-spam')
        await ctx.send(content=f'{member.name}({member.mention}) is today\'s trog!')
        if(self.prevTrog != None):
            await self.prevTrog.remove_roles(guild.get_role(self.roleDict['Trog']))
        self.prevTrog = member
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))

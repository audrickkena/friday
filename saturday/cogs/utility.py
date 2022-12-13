import discord
import random
import functools
import json
import os
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands
from discord.ui import Select, UserSelect, View


class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # self.prevTrog = None
        # self.path = os.path.dirname(__file__) + '/../roles_test.json'
        # self.roleFile = open(self.path, 'r')
        # self.roleDict  = json.loads(self.roleFile.read())
        # self.roleFile.close()
        # self.trogOTD.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Utility cog loaded.')

    @commands.hybrid_command(name='ping', with_app_command=True)
    async def ping(self, ctx):
        print('Pong')
        await ctx.send('Pong')

    @app_commands.command(name='hi')
    async def hi(self, interaction: discord.Interaction):
        print('here')
        await interaction.response.send_message('hello')

    @commands.command()
    async def sync(self, ctx):
        fmt = await self.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f'Synced {len(fmt)} commands.')

    @app_commands.command(name="roll")
    async def rollDice(self, interaction: discord.Interaction, dice_num : int, sides_num : int):
        if(dice_num > 30):
            await interaction.response.send_message('Sorry, max value for the number of dice is 30!')
            return
        if(sides_num > 30):
            await interaction.response.send_message('Sorry max value for the number of dice is 30!')
            return
        if(interaction.channel.name=="command-spam"):
            result = [str(random.choice(range(1, sides_num + 1))) for _ in range(dice_num)]
            msgDices = 'Individual dices: ' + ', '.join(result)
            msgTotal = 'Total roll value: ' + str(functools.reduce(lambda a, b: int(a) + int(b), result))
            msgMax = str(dice_num * sides_num)
            await interaction.response.send_message(f'{msgDices}\n\n{msgTotal}\nMax roll: {msgMax}')

    @app_commands.command(name="maketeams")
    async def makeTeams(self, interaction: discord.Interaction):
        select = UserSelect(
            placeholder="Select members:",
            min_values=2,
            max_values=interaction.guild.max_members)
        async def selCallback(interaction: discord.Interaction):
            numOfSelected = len(select.values)
            await interaction.response.send_message(f'{numOfSelected} is the number of members you have selected')
        #     teamSelect = Select(
        #         placeholder="Select number of teams:",
        #         max_values=1
        #     )
        #     for i in range(2, numOfSelected):
        #         if(numOfSelected // i > 0):
        #             teamSelect.add_option(
        #                 label=f'{i} teams', 
        #                 value=f'{i}'
        #             )
        #     async def teamCallback(interaction: discord.Interaction):
        #         teamsList = [[]] * teamSelect.values[0]
        #         for i in range(numOfSelected):
        #             teamsList[i % teamSelect.values[0]].append(select[i])
        #         for i in range(teamsList):
        #             members = ', '.join(teamsList[i])
        #             await interaction.response.send_message(f'Team {i}: {members}')
                
        #     teamSelect.callback = teamCallback
        #     view.add_item(teamSelect)

        select.callback = selCallback
        view = View()
        view.add_item(select)
        await interaction.response.send_message(f'Choose members for making teams:', view=view)

    @commands.command(name="maketeams")
    async def makeTeams(self, ctx):
        select = Select(options=[
            discord.SelectOption(label="test1", description="1"),
            discord.SelectOption(label="test2", description="2"),
            discord.SelectOption(label="test3", description="3")
        ])
        # select = UserSelect(
        #     placeholder="Select members:",
        #     min_values=1,
        #     max_values=ctx.guild.max_members)
        # async def selCallback(interaction: discord.Interaction):
        #     numOfSelected = len(select.values)
        #     await interaction.response.send_message(f'{numOfSelected} is the number of members you have selected')
        # select.callback = selCallback
        view = View()
        view.add_item(select)
        await ctx.send('Make Teams:', view=view)

    # @app_commands.command(name="close")
    # @app_commands.default_permissions(administrator=True)
    # async def close(self):
    #     await self.bot.close(self)

    # @tasks.loop(hours=24.0)
    # async def trogOTD(self):
    #     await self.bot.wait_until_ready()
    #     guild = discord.utils.get(self.bot.guilds, name='Dankinton')
    #     member = random.choice(guild.members)
    #     while(discord.utils.get(member.roles, id=self.roleDict['Lvl 10 Boss']) == None and discord.utils.get(member.roles, id=self.roleDict['Lvl 100 Mafia Warlord']) == None):
    #         member = random.choice(guild.members)
    #     print(f'{member.name} has been chosen to be today\'s trog!')
    #     await member.add_roles(guild.get_role(self.roleDict['Trog']))
    #     ctx = discord.utils.get(guild.channels, name='command-spam')
    #     await ctx.send(content=f'{member.name}({member.mention}) is today\'s trog!')
    #     if(self.prevTrog != None):
    #         await self.prevTrog.remove_roles(guild.get_role(self.roleDict['Trog']))
    #     self.prevTrog = member

# class MakeTeams(UserSelect):


async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))

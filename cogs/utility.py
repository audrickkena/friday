import discord
import random
import datetime
import functools
import json
import os
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands
from discord.ui import Select, UserSelect, View
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', '.env'))
GUILD = os.getenv('DISCORD_GUILD')

class SelectUsers(UserSelect):
    def __init__(self, ctx):
        super().__init__(
            placeholder='Select users:',
            min_values=3,
            max_values=25
        )
        self.ctx = ctx
        self.users = []
        self.numUsers = 0
        self.options = []
    
    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        self.users = self.values
        self.numUsers = len(self.users)
        await interaction.response.send_message(f'{self.numUsers} is the number of members you have selected')
        for i in range(2, self.numUsers):
            if((self.numUsers) / i > 1):
                temp = discord.SelectOption(
                    label=f'{i} teams',
                    value=f'{i}'
                )
                self.options.append(temp)
        select = UsersIntoTeams(self.users, self.numUsers, self.options)
        view = View()
        view.add_item(select)
        await self.ctx.send(view=view)
    
    def getUsers(self):
        return self.users
    def getNumUsers(self):
        return self.numUsers
    def getOptions(self):
        return self.options

class UsersIntoTeams(Select):
    def __init__(self, users: list, numUsers: int, options: list):
        super().__init__(
            placeholder='Number of teams:',
            options=options
        )
        self.users = users
        self.numUsers = numUsers

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        teams = [[] for i in range(int(self.values[0]))]
        for i in range(self.numUsers):
            tempInt = random.randint(0, len(self.users) - 1)
            teams[i % int(self.values[0])].append(self.users[tempInt].display_name)
            self.users.pop(tempInt)
        teamString = ''
        for i in range(len(teams)):
            teamString += f'Team {i+1}: {", ".join(teams[i])}\n'
        await interaction.response.send_message(content=teamString)

# Server dictionary entry has 3 things: word/phrase, meaning, usage
class addDictModal(discord.ui.Modal, title='Add a word/phrase'):
    word = discord.ui.TextInput(label='Word/phrase to add into dictionary', placeholder='smegwash', required=True, max_length=100, style=discord.TextStyle.short)
    meaning = discord.ui.TextInput(label='Meaning of word/phrase', placeholder='What could it mean?', required=True, max_length=4000, style=discord.TextStyle.long)
    usage = discord.ui.TextInput(label='Usage of word/phrase', placeholder='How is it used?', required=True, max_length=4000, style=discord.TextStyle.long)

    def entryExists(self):
        with open('dict.json', 'r') as f:
            temp = json.loads(f.read())
            if self.word.value.lower() in temp.keys():
                return True
            else:
                return False

    async def on_submit(self, interaction: discord.Interaction):
        if os.path.exists('dict.json'):
            if self.entryExists():
                await interaction.response.send_message(f'{self.word.value} is already in the dictionary! LMAO can\'t read moment', ephemeral=True)
                return
        with open('dict.json', 'w+') as f:
            currDateTime = datetime.datetime.now() + datetime.timedelta(hours=8)
            date = currDateTime.strftime('%x')
            time = currDateTime.strftime('%X')
            print(len(f.readlines))
            if len(f.readlines()) > 0:
                f.seek(0)
                prevDict = json.loads(f.read())
                print(f'prevDict = {prevDict}')
                prevDict[self.word.value.lower()] = f'{self.meaning.value},{self.usage.value},{date},{time}'
                temp = prevDict
            else:
                temp = {self.word.value.lower(): f'{self.meaning.value},{self.usage.value},{date},{time}'}
            f.seek(0)
            f.write(json.dumps(temp, indent=4))
            await interaction.response.send_message(f'{self.word.value} has been added succesfully!', ephemeral=True)
            

    

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
    
    dictGrp = app_commands.Group(name='dict', description='For commands related to the server\'s dictionary')

    @app_commands.command(name='hi', description="For lonely people")
    async def hi(self, interaction: discord.Interaction):
        await interaction.response.send_message('hello', ephemeral=True)

    @app_commands.command(name="roll", description="For rolling a number of dices with a number of sides")
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
    
    @app_commands.command(name="teams", description='For making teams based on the selected users')
    async def teams(self, interaction: discord.Interaction):
        selectUsers = SelectUsers(interaction.channel)
        view = View()
        view.add_item(selectUsers)
        await interaction.response.send_message("Choose users:", view=view)
    
    @app_commands.command(name='help', description='For getting information on usable commands')
    async def help(self, interaction: discord.Interaction):
        cogs = self.bot.cogs
        embedList = []
        for cogName, cog in cogs.items():
            if(cogName == 'Admin' and interaction.guild.owner_id != interaction.user.id):
                continue
            message = discord.Embed(
                title=cogName,
                description=f'{cogName} cog commands:\n',
                color=discord.Colour.blue()
            )
            if(len(cog.get_app_commands()) > 0):
                message.add_field(name='\n\u200b', value='**Slash commands**', inline=False)
                self.getAppCommands(cog, message)
            if(len(cog.get_commands()) > 0):
                message.add_field(name='\n\u200b', value='**Prefix commands**', inline=False)
                self.getCommands(cog, message)
            embedList.append(message)
        await interaction.response.send_message(embeds=embedList, ephemeral=True)

    @app_commands.command(name='ping', description="For really bored people")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message('Pong', ephemeral=True)

    ########## DICTIONARY GROUP FUNCTIONS ##########

    # TODO: commands for server dictionary: /dict list, /dict add, /dict remove(admin only) /dict find {word}
    @dictGrp.command(name='list', description='For listing contents of server dictionary')
    async def listDict(self, interaction: discord.Interaction):
        message = discord.Embed(
            title='Dictionary of Server Slang',
            description='Listing all words added to the server\'s dictionary',
            color=discord.Colour.red()
        )
        with open('dict.json', 'r') as f:
            entries = json.loads(f.read())
            words = entries.keys()
            for e in words:
                entryDate = entries[e].split(',')[-2]
                entryTime = entries[e].split(',')[-1]
                message.add_field(name=f'{e}', value=f'Created: {entryDate} {entryTime}', inline=True)
        await interaction.response.send_message(embed=message, ephemeral=True)

    @dictGrp.command(name='add', description='For adding a word or phrase into the server dictionary')
    async def addDict(self, interaction: discord.Interaction):
        await interaction.response.send_modal(addDictModal())

    ########## END OF DICTIONARY GROUP FUNCTIONS ##########
        
    def getAppCommands(self, cog, embed):
        commands = cog.get_app_commands()
        for command in commands:
            if isinstance(command, discord.app_commands.Group):
                temp = command.commands
                message = ''
                for e in temp:
                    message += f'- name: *{e.name}*\n  - description: {e.description}\n  - usage: `/{command.name} {e.name}'
                    for parameter in e.parameters:
                        message += f' {{{parameter.name}}}'
                    message += '`\n'
                embed.add_field(name=f'{command.name} group commands', value=message, inline=False)
            else:
                message = f'- description: {command.description}\n- usage: `/{command.name}'
                for parameter in command.parameters:
                    message += f' {{{parameter.name}}}'
                message += '`'
                embed.add_field(name=command.name, value=message, inline=False)

    def getCommands(self, cog, embed):
        commands = cog.get_commands()
        for command in commands:
            message = f'- description: {command.description}\n- usage: `{command.usage}`'
            embed.add_field(name=command.name, value=message, inline=False)

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
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))

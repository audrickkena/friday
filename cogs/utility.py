import discord
import random
import datetime
import functools
import json
import os

import danki_checks
import danki_exceptions
import danki_enums

from discord.ext import commands
from discord.ext import tasks
from discord import app_commands
from discord.ui import Select, UserSelect, View

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
            if len(f.readlines()) > 0:
                f.seek(0)
                temp = json.loads(f.read())
                if self.word.value.lower() in temp.keys():
                    return True 
            return False

    async def on_submit(self, interaction: discord.Interaction):
        if self.entryExists():
            await interaction.response.send_message(f'{self.word.value} is already in the dictionary! LMAO can\'t read moment', ephemeral=True)
            return
        with open('dict.json', 'r+') as f:
            currDateTime = datetime.datetime.now() + datetime.timedelta(hours=8)
            date = currDateTime.strftime('%d/%m/%y')
            time = currDateTime.strftime('%X')
            if len(f.readlines()) > 0:
                f.seek(0)
                prevDict = json.loads(f.read())
                prevDict[self.word.value.lower()] = f'{self.meaning.value},,,{self.usage.value},,,{date},,,{time}'
                temp = prevDict
            else:
                temp = {self.word.value.lower(): f'{self.meaning.value},,,{self.usage.value},,,{date},,,{time}'}
            f.seek(0)
            f.write(json.dumps(temp, indent=4))
            await interaction.response.send_message(f'{self.word.value} has been added succesfully!', ephemeral=True)

class editDictModal(discord.ui.Modal):
    def __init__(self, entry: str):
        super().__init__(title='Edit Dictionary Entry')
        self.entry = entry
        with open('dict.json', 'r') as f:
            data = json.loads(f.read())[entry]
            t = data.split(',,,')
            meaning = t[0]
            usage = t[1]
            date = t[2]
            time = t[3]
        self.date = date
        self.time = time
        self.word = discord.ui.TextInput(label='Word/phrase to edit from dictionary', default=entry, required=True, max_length=100, style=discord.TextStyle.short)
        self.meaning = discord.ui.TextInput(label='Meaning of word/phrase', default=meaning, required=True, max_length=4000, style=discord.TextStyle.long)
        self.usage = discord.ui.TextInput(label='Usage of word/phrase', default=usage, required=True, max_length=4000, style=discord.TextStyle.long)
        self.add_item(self.word)
        self.add_item(self.meaning)
        self.add_item(self.usage)

    async def on_submit(self, interaction: discord.Interaction):
        with open('dict.json', 'r+') as f:
            prevDict = json.loads(f.read())
            newDict = {}
            for entry in prevDict.keys():
                if entry != self.entry.lower():
                    newDict[entry] = prevDict[entry]
                else:
                    newDict[self.word.value.lower()] = f'{self.meaning.value},,,{self.usage.value},,,{self.date},,,{self.time}'
            f.seek(0)
            f.write(json.dumps(newDict, indent=4))
            await interaction.response.send_message(f'{self.word.value} has been added succesfully!', ephemeral=True)
    
# TODO: Implement new checks and exceptions for UTILITY
class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.setup = self.bot.getUtilitySetup()
        # self.prevTrog = None
        # self.path = os.path.dirname(__file__) + '/../roles_test.json'
        # self.roleFile = open(self.path, 'r')
        # self.roleDict  = json.loads(self.roleFile.read())
        # self.roleFile.close()
        # self.trogOTD.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{danki_enums.Console.getPrefix()} Utility cog loaded.')
    
    # TODO: /remindme command for reminding user of something

    @app_commands.command(name="teams", description='For making teams based on the selected users')
    async def teams(self, interaction: discord.Interaction):
        try:
            if await danki_checks.checkCommandNeedRoles(interaction.user, 'teams', self.setup['optional']) == True:
                selectUsers = SelectUsers(interaction.channel)
                view = View()
                view.add_item(selectUsers)
                await interaction.response.send_message("Choose users:", view=view)
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await interaction.response.send_message(f'You lack the necessary roles to use this command! {danki_enums.DiscordOut.ISSUE_GITHUB}', ephemeral=True)
        except Exception as err:
            await interaction.response.send_message(f'{danki_enums.DiscordOut.ERROR}', ephemeral=True)
            raise err
            
    


    ####################################
    ########## HELP FUNCTIONS ##########

    @app_commands.command(name='help', description='For getting information on usable commands')
    async def help(self, interaction: discord.Interaction):
        try:
            if await danki_checks.checkCommandNeedRoles(interaction.user, 'help', self.setup['optional']) == True:
                cogs = self.bot.cogs
                embedList = []
                for cogName, cog in cogs.items():
                    if(cogName == 'Admin' and interaction.guild.owner_id != interaction.user.id):
                        continue
                    message = discord.Embed(
                        title=f'{cogName} commands:\n',
                        color=discord.Colour.blue()
                    )
                    if(len(cog.get_app_commands()) > 0):
                        self.getAppCommands(cog, message)
                    if(len(cog.get_commands()) > 0):
                        message.add_field(name='\n\u200b', value='\n', inline=False)
                        self.getCommands(cog, message)
                    embedList.append(message)
                await interaction.response.send_message(embeds=embedList, ephemeral=True)
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await interaction.response.send_message(f'You lack the necessary roles to use this command! {danki_enums.DiscordOut.ISSUE_GITHUB}', ephemeral=True)
        except Exception as err:
            await interaction.response.send_message(f'{danki_enums.DiscordOut.ERROR}', ephemeral=True)
            raise err
    
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

    ########## END OF HELP FUNCTIONS ##########
    ###########################################



    ################################################
    ########## DICTIONARY GROUP FUNCTIONS ##########
    
    # TODO: commands for server dictionary: /dict remove(admin only?)
    dictGrp = app_commands.Group(name='dict', description='For commands related to the server\'s dictionary')

    @dictGrp.command(name='list', description='For listing contents of server dictionary')
    async def listDict(self, interaction: discord.Interaction):
        try:
            if await danki_checks.checkCommandNeedRoles(interaction.user, 'listDict', self.setup['optional']) == True:
                if not self.dictFileExists():
                    await interaction.response.send_message('No entries in dictionary!', ephemeral=True)
                else:
                    message = discord.Embed(
                        title='Dictionary of Server Slang',
                        description='Listing all words added to the server\'s dictionary',
                        color=discord.Colour.red()
                    )
                    with open('dict.json', 'r') as f:
                        entries = json.loads(f.read())
                        words = entries.keys()
                        for e in words:
                            entryDate = entries[e].split(',,,')[-2]
                            entryTime = entries[e].split(',,,')[-1]
                            message.add_field(name=f'{e}', value=f'Created: {entryDate} {entryTime}', inline=False)
                    await interaction.response.send_message(embed=message, ephemeral=True)
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await interaction.response.send_message(f'You lack the necessary roles to use this command! {danki_enums.DiscordOut.ISSUE_GITHUB}', ephemeral=True)
        except Exception as err:
            await interaction.response.send_message(f'{danki_enums.DiscordOut.ERROR}', ephemeral=True)
            raise err

    @dictGrp.command(name='add', description='For adding a word or phrase into the server dictionary')
    async def addDict(self, interaction: discord.Interaction):
        try:
            if await danki_checks.checkCommandNeedRoles(interaction.user, 'addDict', self.setup['optional']) == True:
                if not self.dictFileExists():
                    f = open('dict.json', 'x')
                    f.close()
                await interaction.response.send_modal(addDictModal())
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await interaction.response.send_message(f'You lack the necessary roles to use this command! {danki_enums.DiscordOut.ISSUE_GITHUB}', ephemeral=True)
        except Exception as err:
            await interaction.response.send_message(f'{danki_enums.DiscordOut.ERROR}', ephemeral=True)
            raise err

    @dictGrp.command(name='get', description='For getting the meaning and usage of a word or phrase in the server dictionary')
    async def getDict(self, interaction: discord.Interaction, entry: str):
        try:
            if await danki_checks.checkCommandNeedRoles(interaction.user, 'getDict', self.setup['optional']) == True:
                if not self.dictFileExists():
                    await interaction.response.send_message('No entries in dictionary!', ephemeral=True)
                else:
                    with open('dict.json', 'r') as f:
                        entries = json.loads(f.read())
                        words = entries.keys()
                        if entry.lower() in words:
                            val = entries[entry]
                            valList = val.split(',,,')
                            meaning = valList[0]
                            usage = valList[1]
                            message = discord.Embed(
                                title=f'{entry.lower()}',
                                description=f'Here is the definition and usage of the entry {entry.lower()} entered on {valList[2]} at {valList[3]}',
                                color=discord.Colour.red()
                            )
                            message.add_field(name='\n\u200b', value=f'Definition: {meaning}\nUsage: {usage}')
                            await interaction.response.send_message(embed=message, ephemeral=True)
                        else:
                            await interaction.response.send_message(f'{entry} is not in the dictionary! Use /dict list to find out the words available', ephemeral=True)
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await interaction.response.send_message(f'You lack the necessary roles to use this command! {danki_enums.DiscordOut.ISSUE_GITHUB}', ephemeral=True)
        except Exception as err:
            await interaction.response.send_message(f'{danki_enums.DiscordOut.ERROR}', ephemeral=True)
            raise err
        
    @getDict.autocomplete('entry')
    async def dictAuto(self, interaction: discord.Interaction, current: str):
        data = []
        with open('dict.json', 'r') as f:
            entries = json.loads(f.read())
            for entry in entries.keys():
                if current.lower() in entry.lower():
                    data.append(app_commands.Choice(name=entry, value=entry))
        return data

    @dictGrp.command(name='edit', description='For editing an existing entry in the dictionary')
    async def editDict(self, interaction: discord.Interaction, entry: str):
        try:
            if await danki_checks.checkCommandNeedRoles(interaction.user, 'editDict', self.setup['optional']) == True:
                if not self.dictFileExists():
                    await interaction.response.send_message('No entries in dictionary!', ephemeral=True)
                else:
                    with open('dict.json', 'r') as f:
                        entries = json.loads(f.read())
                        words = entries.keys()
                        if entry.lower() in words:
                            edit = editDictModal(entry.lower())
                            await interaction.response.send_modal(edit)
                        else:
                            await interaction.response.send_message(f'{entry} is not in the dictionary! Use /dict list to find out the words available', ephemeral=True)
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await interaction.response.send_message(f'You lack the necessary roles to use this command! {danki_enums.DiscordOut.ISSUE_GITHUB}', ephemeral=True)
        except Exception as err:
            await interaction.response.send_message(f'{danki_enums.DiscordOut.ERROR}', ephemeral=True)
            raise err
    
    def dictFileExists(self):
        try:
            with open('dict.json', 'r') as f:
                return True
        except FileNotFoundError:
            return False

    ########## END OF DICTIONARY GROUP FUNCTIONS ##########
    #######################################################



    ###################################################
    ########## START OF POLL GROUP FUNCTIONS ##########

    # TODO: Implement a poll commands such as /poll create /poll start /poll end /poll results /poll del /poll edit(can only edit when poll is not started)
    ######## check sequence diagram for poll command possible flow

    ########## END OF POLL GROUP FUNCTIONS ##########
    #################################################



    ###################################
    ########### DANKI BUCKS ###########
    ###################################

    # dbucks = app_commands.Group(name='dbucks', description='For commands related to the server\'s virtual currency')

    # @dbucks.command(name='mybalance', description='for getting your balance amount')
    # async def balance(self, interaction: discord.Interaction):
    #     with open(f'utility/passport/{UID}')


    ##########################################
    ########### END OF DANKI BUCKS ###########
    ##########################################


    ################################
    ########### PASSPORT ###########
    ################################
    '''
    Passport current structure:
    [VIEWABLE Information] - Everyone can view but no one can edit (including passport owner) except mods
    Server Nickname:
    Discord Username:
    Birthday Month:
    Server Join Date:
    Biggest Loser Count:
    DBUCKS Amount:

    [EDITABLE information] -  Passport owner and mods can edit
    STEAM FRIEND CODE:
    EPIC FRIEND CODE:
    (etc...)

    directory path: utility/passports/{userid}.json

    JSON SAMPLE:
    {
        "View": {
            "Username": (username),
            "Nickname": (displayname),
            "Birthday Month": (month in numerical [1-12] i.e: 1 = Jan, 12 = Dec),
            "Join Date": (YYYY-MM-DD),
            "Biggest Loser Record":{
                (YYYY-MM-DD)
            },
            "DBUCKS Amount: D$(dbux amt)
        },
        "Edit": {
            "STEAMID": (id),
            "EPICID": (id),
            "ORIGINID": (id)
        }
    }
    '''

    # passport = app_commands.Group(name='passport', description='For commands related to your identity in the server')
    # @passport.command(name='show', description='for showing the passport of a user (run without mentioning a user to show your own passport)')
    # async def showPass(self, interaction: discord.Interaction, user_mention=None):
    #     try:
    #         member = None
    #         memberID = None
    #         if user_mention == None:
    #             memberID = interaction.user.id
    #         else:
    #             if user_mention[1] != '@' or user_mention[2] == '&':
    #                 await interaction.response.send_message(f'{user_mention} is not a mention of a user in the server! Type @{{username}} to ensure that user is mentioned properly!', ephemeral=True)
    #             else:
    #                 memberID = user_mention[2:-1]
    #         member = discord.utils.get(interaction.guild.members, id=memberID)
    #         if member == None:
    #             # raise user not found err
    #             print('User not foundddddd, oi make the error handler lah sheesh')
    #             return
    #         if danki_checks.checkDirectoriesExist(['utility/passports']) == True:
    #             if danki_checks.checkFileExists(f'utility/passports/{memberID}.json') == True:

    #     except:
    #         pass

    #######################################
    ########### END OF PASSPORT ###########
    #######################################


async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))
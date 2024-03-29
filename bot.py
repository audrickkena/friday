import os
import json
import discord
import sys
import random

import danki_checks
import danki_exceptions
import danki_enums
import tm_color

from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get

## INITIALISING INTENTS
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
intents.voice_states = True
intents.presences = True

## LOADING ENVIRONMENT
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
APPID = os.getenv('DISCORD_APP_ID')

## FRIDAY CLASS DEFINITION
# TODO: Add logging of errors and warnings that happen in runtime
# TODO: Consider logging of other things
class Friday(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents = intents,
            application_id = APPID
        )
        self.currGuild = None
        self.initial_extensions = [
            "cogs.admin",
            "cogs.utility",
            'cogs.misc'
        ]
        # Setup options initialised for bot and the cogs
        self.botSetup = None
        self.adminSetup = None
        self.utilitySetup = None
        self.miscSetup = None
    async def setup_hook(self):
        """!
        A coroutine to be called to setup the bot, by default this is blank.
        This performs an asynchronous setup after the bot is logged in,
        but before it has connected to the Websocket (quoted from d.py docs)
        """
        try:
            await self.getSetup()
            self.remove_command('help')
            
            for ext in self.initial_extensions:
                await self.load_extension(ext)

        except Exception as e:
            raise e
    
    async def on_ready(self):
        try:
            for guild in self.guilds:
                if guild.id == int(GUILD): 
                    self.currGuild = guild
                    break
            if await danki_checks.checkServerHasRoles(self.currGuild) == True:
                print(f'{danki_enums.Console.getPrefix()} Discord version: {discord.__version__}\n{danki_enums.Console.getPrefix()} Python version: {sys.version}\n')
                print(
                    f'{danki_enums.Console.getPrefix()} {self.user} has connected to Discord!\n'
                    f'{danki_enums.Console.getPrefix()} {self.user} is connected to {self.currGuild.name}(id: {self.currGuild.id})\n'
                )
                await self.initialiseDirectories()
                updateRoles(self, self.currGuild.roles)
        except danki_exceptions.RoleDoesNotExist as err:
            print(f'\n{err}\n')
            print(f'{danki_enums.Console.getPrefix()} Due to setup failure, Danki will be closing...\n')
            await self.close()

        except Exception as e:
            raise e
        
    async def initialiseDirectories(self):
        try:
            # TODO: consider moving paths to it's own json file
            paths = ['misc', 'misc/selamat', 'backups', 'utility', 'utility/passports']
            if await danki_checks.checkDirectoriesExist(paths) == True:
                print(f'{danki_enums.Console.getPrefix()} All directories present')
        except danki_exceptions.DirectoryMissing as err:
            path = err.getPath()
            print(f'{danki_enums.Console.getPrefix()} {danki_enums.Console.WARNING} {{{path}}} directory is not initialised yet!\n{danki_enums.Console.getPrefix()} {tm_color.colors.fg.green}Adding directory now...{tm_color.colors.reset}', end='')
            os.mkdir(path)
            print(f'{tm_color.colors.fg.blue}{{{path}}} directory initialised!{tm_color.colors.reset}\n')
            await self.initialiseDirectories()
        except Exception as err:
            raise err

    async def on_guild_role_create(self, role):
        if(role.guild == self.currGuild):
            updateRoles(self, self.currGuild.roles)
            print(f'{danki_enums.Console.getPrefix()} Roles file has been updated! Added role {role.name}({role.id})')

    async def on_guild_role_delete(self, role):
        if(role.guild == self.currGuild):
            updateRoles(self, self.currGuild.roles)
            print(f'{danki_enums.Console.getPrefix()} Roles file has been updated! Removed role {role.name}({role.id})')

    async def on_guild_role_update(self, before, after):
        if(before.guild == self.currGuild):
            updateRoles(self, self.currGuild.roles)
            print(f'{danki_enums.Console.getPrefix()} Roles file has been updated! Updated role from {before.name}({before.id}) to {after.name}({after.id})')
    
    async def on_member_join(self, member):
        try:
            namesFile = open('backups/memberNamesBackup.json', 'r')
            namesDict = json.loads(namesFile.read())
            if str(member.id) in namesDict.keys():
                roleFile = open('backups/memberRolesBackup.json', 'r')
                roleDict = json.loads(roleFile.read())
                prevRoles = roleDict[str(member.id)].split(',')
                for e in prevRoles:
                    await member.add_roles(self.currGuild.get_role(int(e)))
                print(f'{danki_enums.Console.getPrefix()} {member.name} has recovered their previous roles!')
                roleFile.close()
            elif(member.guild == self.currGuild):
                print(f'{danki_enums.Console.getPrefix()} {member.name} has joined the server!')
                for role in self.botSetup['required']['default_roles']:
                    await member.add_roles(discord.utils.get(self.currGuild.roles, name=role))
                    print(f'{danki_enums.Console.getPrefix()} {member.name} has been given role "{role}"')
                # separators should store the id of the role, not the name as role separators have funky names
                if len(self.botSetup['optional']['separators']) >= 1 and '---NONE---' not in self.botSetup['optional']['separators']:
                    for role in self.botSetup['optional']['separators']:
                        await member.add_roles(discord.utils.get(self.currGuild.roles, id=int(role)))   
            namesFile.close()
        except Exception as e:
            raise e

    
    async def on_member_remove(self, member):
        print(f'{danki_enums.Console.getPrefix()} {member.name} has left the server!')

    
    async def on_voice_state_update(self, member, before, after):
        if(member.guild != self.currGuild):
            return
        if(member == self.user):
            return
        if(before.channel == None):
            if after.channel.name in self.botSetup['optional']['silent_channels']:
                return
            msg = f'{member.display_name} just joined {after.channel}'
            channel = get(self.currGuild.channels, name=self.botSetup['required']['tts_channel'], type=discord.ChannelType.text)
            await channel.send(content=msg, tts=False, delete_after=10)
        if(after.channel == None):
            if(before.channel.name in self.botSetup['optional']['silent_channels']):
                return
            msg = f'{member.display_name} just left {before.channel}'
            channel = get(self.currGuild.channels, name=self.botSetup['required']['tts_channel'], type=discord.ChannelType.text)
            await channel.send(content=msg, tts=False, delete_after=10)

    # async def on_message(self, message):
    #     pass
    
    async def getSetup(self):
        try:
            setup = await danki_checks.checkSetup()
            self.botSetup = setup['bot']
            self.adminSetup = setup['admin']
            self.utilitySetup = setup['utility']
            self.miscSetup = setup['misc']
        except danki_exceptions.MissingValueInSetup as err:
            print(f'\n{err}\n')
            print(f'{danki_enums.Console.getPrefix()} Due to setup failure, Danki will be closing...\n')
            await self.close()
        except danki_exceptions.DefaultValueNotRemoved as err:
            print(f'\n{err}\n')
            print(f'{danki_enums.Console.getPrefix()} The default value will now be removed from {{{err.getKey()}}}.\nIf this action is not working as intended, please contact the developer on github\n')
            with open('SETUP.json', 'r+') as f:
                f.seek(0)
                setup = json.loads(f.read())
                print(f'{danki_enums.Console.getPrefix()} {{{err.getKey()}}} before: {setup[err.getModule()][err.getSetting()][err.getKey()]}')
                temp = [x for x in setup[err.getModule()][err.getSetting()][err.getKey()] if x != '---NONE---']
                setup[err.getModule()][err.getSetting()][err.getKey()] = temp
                f.seek(0)
                f.write(json.dumps(setup, indent=4))
                # to remove lingering contents after f.write() truncate method used
                f.truncate()
                print(f'{danki_enums.Console.getPrefix()} {{{err.getKey()}}} after: {setup[err.getModule()][err.getSetting()][err.getKey()]}\n')
            await self.getSetup()
        except Exception as err:
            print(f'\n{danki_enums.Console.getPrefix()} I don\'t know how you got here but you did')
            print(f'{danki_enums.Console.getPrefix()} Closing bot due to this unexpected error')
            raise err
    
    def getGuild(self):
        return self.currGuild
    
    def getGuildRoles(self):
        return self.currGuild.roles

    def getCogs(self):
        return self.initial_extensions
    
    def getBotSetup(self):
        return self.botSetup
    
    def getAdminSetup(self):
        return self.adminSetup
    
    def getUtilitySetup(self):
        return self.utilitySetup
    
    def getMiscSetup(self):
        return self.miscSetup

## HELPER FUNCTIONS
def updateRoles(self, guildRoles):
    roleDict = {}
    roleFile = open('roles.json', 'w')
    for i in range(len(guildRoles)):
        roleDict[guildRoles[i].name] = guildRoles[i].id
    roleFile.write(json.dumps(roleDict, indent=4))
    roleFile.close()



bot = Friday()
bot.run(TOKEN)

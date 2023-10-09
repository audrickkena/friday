import os
import json
import discord
import random

import danki_checks
import danki_exceptions
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
# TODO: UPDATE HARDCODED VARIABLES TO BE FETCHED FROM SETUP.TXT INSTEAD
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
        self.setupVariables = None
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
            if danki_checks.checkServerHasRequiredRoles(self.currGuild) == True:
                print(discord.__version__)
                print(
                    f'{self.user} has connected to Discord!\n'
                    f'{self.user} is connected to {self.currGuild.name}(id: {self.currGuild.id})\n\n'
                )
                await self.initialiseDirectories()
                updateRoles(self, self.currGuild.roles)
        except danki_exceptions.RoleDoesNotExist as err:
            print(f'\n{err}\n')
            print('Due to setup failure, Danki will be closing...\n')
            await self.close()

        except Exception as e:
            raise e
        
    async def initialiseDirectories(self):
        paths = ['misc', 'misc/selamat', 'backups']
        for path in paths:
            if os.path.exists(path) == False:
                print(f'{tm_color.colors.fg.yellow}[WARNING]: {{{path}}} directory is not initialised yet!{tm_color.colors.reset}\n{tm_color.colors.fg.green}Adding directory now...{tm_color.colors.reset}', end='')
                os.mkdir(path)
                print(f'{tm_color.colors.fg.blue}{{{path}}} directory initialised!{tm_color.colors.reset}\n\n')

    async def on_guild_role_create(self, role):
        if(role.guild == self.currGuild):
            updateRoles(self, self.currGuild.roles)
            print(f'Roles file has been updated! Added role {role.name}({role.id})')

    async def on_guild_role_delete(self, role):
        if(role.guild == self.currGuild):
            updateRoles(self, self.currGuild.roles)
            print(f'Roles file has been updated! Removed role {role.name}({role.id})')

    async def on_guild_role_update(self, before, after):
        if(before.guild == self.currGuild):
            updateRoles(self, self.currGuild.roles)
            print(f'Roles file has been updated! Updated role from {before.name}({before.id}) to {after.name}({after.id})')
    
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
                print(f'{member.name} has recovered their previous roles!')
                roleFile.close()
            elif(member.guild == self.currGuild):
                print(f'{member.name} has joined the server!')
                for role in self.setupVariables['required']['default_roles']:
                    await member.add_roles(discord.utils.get(self.currGuild.roles, name=role))
                    print(f'{member.name} has been given role "{role}"')
                # separators should store the id of the role, not the name as role separators have funky names
                if len(self.setupVariables['optional']['separators']) >= 1 and '---NONE---' not in self.setupVariables['optional']['separators']:
                    for role in self.setupVariables['optional']['separators']:
                        await member.add_roles(discord.utils.get(self.currGuild.roles, id=int(role)))   
            namesFile.close()
        except Exception as e:
            raise e

    
    async def on_member_remove(self, member):
        print(f'{member.name} has left the server!')

    
    async def on_voice_state_update(self, member, before, after):
        if(member.guild != self.currGuild):
            return
        if(member == self.user):
            return
        if(before.channel == None):
            if after.channel.name in self.setupVariables['optional']['silent_channels']:
                return
            msg = f'{member.display_name} just joined {after.channel}'
            channel = get(self.currGuild.channels, name=self.setupVariables['required']['voice_state_channel'], type=discord.ChannelType.text)
            await channel.send(content=msg, tts=True, delete_after=10)
        if(after.channel == None):
            if(before.channel.name in self.setupVariables['optional']['silent_channels']):
                return
            msg = f'{member.display_name} just left {before.channel}'
            channel = get(self.currGuild.channels, name=self.setupVariables['required']['voice_state_channel'], type=discord.ChannelType.text)
            await channel.send(content=msg, tts=True, delete_after=10)

    # async def on_message(self, message):
    #     pass
    
    def getGuild(self):
        return self.currGuild

    def getCogs(self):
        return self.initial_extensions
    
    async def getSetup(self):
        try:
            bot_setup = danki_checks.checkRequired()
            self.setupVariables = bot_setup
        except danki_exceptions.MissingValueInSetup as err:
            print(f'\n{err}\n')
            print('Due to setup failure, Danki will be closing...\n')
            await self.close()
        except danki_exceptions.DefaultValueNotRemoved as err:
            print(f'\n{err}\n')
            print(f'The default value will now be removed from {{{err.getKey()}}}.\nIf this action is not working as intended, please contact the developer on github\n')
            with open('SETUP.json', 'r+') as f:
                setup = json.loads(f.read())
                f.seek(0)
                print(f'{{{err.getKey()}}} before: {setup["bot"][err.getKey()]}')
                temp = [x for x in setup['bot'][err.getKey()] if x != '---NONE---']
                setup['bot'][err.getKey()] = temp
                f.write(json.dumps(setup, indent=4))
                print(f'{{{err.getKey()}}} after: {temp}')
                self.setupVariables = setup['bot']
        except Exception as err:
            print('I don\'t know how you got here but you did')
            print(err)
            print('Closing bot due to this unexpected error')
            await self.close()

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

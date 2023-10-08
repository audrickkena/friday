import os
import json
import discord
import random
import danki_exceptions
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
        self.remove_command('help')
        await self.getSetup()
        for ext in self.initial_extensions:
            await self.load_extension(ext)
    
    async def on_ready(self):
        for guild in self.guilds:
            if guild.id == int(GUILD): 
                self.currGuild = guild
                break
        print(discord.__version__)
        print(
            f'{self.user} has connected to Discord!\n'
            f'{self.user} is connected to {self.currGuild.name}(id: {self.currGuild.id})\n\n'
        )
        updateRoles(self, self.currGuild.roles)

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
            roleFile = open('roles.json', 'r')
            roleDict = json.loads(roleFile.read())
            print(f'{member.name} has joined the server!')
            await member.add_roles(self.currGuild.get_role(roleDict['Lvl 0 Thief']))
            # Role separator IDS below
            # TODO: GET ROLE SEPARATOR IDS FROM EXTERNAL FILE INSTEAD
            await member.add_roles(self.currGuild.get_role(1059332235028856893))
            await member.add_roles(self.currGuild.get_role(1059324888906743878))
            await member.add_roles(self.currGuild.get_role(1059331288533843989))
            print(f'{member.name} has been given role "Lvl 0 Thief"')
            roleFile.close()
        namesFile.close()

    
    async def on_member_remove(self, member):
        print(f'{member.name} has left the server!')

    
    async def on_voice_state_update(self, member, before, after):
        if(member.guild != self.currGuild):
            return
        if(member == self.user):
            return
        if(before.channel == None):
            if(after.channel.name == 'all hail the thocc'):
                return
            msg = f'{member.display_name} just joined {after.channel}'
            channel = get(self.currGuild.channels, name='voiceless-spam-lvl10', type=discord.ChannelType.text)
            await channel.send(content=msg, tts=True, delete_after=10)
        if(after.channel == None):
            if(before.channel.name == 'all hail the thocc'):
                return
            msg = f'{member.display_name} just left {before.channel}'
            channel = get(self.currGuild.channels, name='voiceless-spam-lvl10', type=discord.ChannelType.text)
            await channel.send(content=msg, tts=True, delete_after=10)

    # async def on_message(self, message):
    #     pass
    
    def getGuild(self):
        return self.currGuild

    def getCogs(self):
        return self.initial_extensions
    
    async def getSetup(self):
        try:
            with open('SETUP.json', 'r') as f:
                bot_setup = json.loads(f.read())['bot']
                for e in bot_setup.keys():
                    if bot_setup[e] == '---NONE---':
                        print(e)
                        if e == 'default_roles' or e == 'voice_state_channel':
                            raise danki_exceptions.MissingValueInSetup(e, f'{e} has not been initialised although it is required! Please initialise this value before starting Danki!')
                self.setupVariables = bot_setup
        except danki_exceptions.MissingValueInSetup as err:
            print(err)
            print('Due to setup failure, Danki will be closing...')
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

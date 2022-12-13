import os
import json
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord import app_commands

## INITIALISING INTENTS
intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.voice_states = True

## LOADING ENVIRONMENT
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
APPID = os.getenv('DISCORD_APP_ID')

## Saturday class definition
class Saturday(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents = intents,
            application_id = APPID
        )
        self.currGuild = None
        self.initial_extensions = [
            "cogs.utility",
            "cogs.admin"
        ]
    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)
        for guild in self.guilds:
            if guild.name == GUILD: 
                self.currGuild = guild
                break
        await bot.tree.sync(guild = self.currGuild)
    
    async def on_ready(self):
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
        if(member.guild == self.currGuild):
            roleFile = open('roles_test.json', 'r')
            roleDict = json.loads(roleFile.read())
            print(f'{member.name} has joined the server!')
            await member.add_roles(self.currGuild.get_role(roleDict['Lvl 0 Thief']))
            print(f'{member.name} has been given role "Lvl 0 Thief"')
            roleFile.close()

    
    async def on_member_remove(self, member):
        print(f'{member.name} has left the server!')

    
    async def on_voice_state_update(self, member, before, after):
        if(member.guild != self.currGuild):
            return
        if(member == self.user):
            return
        if(before.channel == None):
            if(member.nick == None):
                msg = f'{member.name} just joined {after.channel}'
            else:
                msg = f'{member.nick} just joined {after.channel}'
            channel = get(self.currGuild.channels, name='voiceless-spam', type=discord.ChannelType.text)
            await channel.send(content=msg, tts=True, delete_after=10)
        if(after.channel == None):
            if(member.nick == None):
                msg = f'{member.name} just left {before.channel}'
            else:
                msg = f'{member.nick} just left {before.channel}'
            channel = get(self.currGuild.channels, name='voiceless-spam', type=discord.ChannelType.text)
            await channel.send(content=msg, tts=True, delete_after=10)

    async def on_command_error(self, ctx, error):
        if(isinstance(error, commands.BadArgument)):
            if(ctx.command.name == 'roll'):
                await ctx.send('Roll was given unsuitable arguments! Please retry with valid integer inputs.')

## HELPER FUNCTIONS
def updateRoles(self, guildRoles):
    roleDict = {}
    roleFile = open('roles_test.json', 'w')
    for i in range(len(guildRoles)):
        roleDict[guildRoles[i].name] = guildRoles[i].id
    roleFile.write(json.dumps(roleDict, indent=4))
    roleFile.close()

bot = Saturday()
bot.run(TOKEN)
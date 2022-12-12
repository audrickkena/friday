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

## INITIALISING VARIABLES
# bot = commands.Bot(command_prefix='!', intents=intents)
# currGuild = None

# ## BOT EVENT LISTENERS
# @bot.event
# async def on_ready():
#     print(discord.__version__)
#     for guild in bot.guilds:
#         if guild.name == GUILD:
#             global currGuild 
#             currGuild = guild
#             break
#     print(
#         f'{bot.user} has connected to Discord!\n'
#         f'{bot.user} is connected to {currGuild.name}(id: {currGuild.id})\n\n'
#     )
#     updateRoles(currGuild.roles)
#     try:
#         synced = await bot.tree.sync()
#         print(f'Synced {len(synced)} commands(s)')
#     except Exception as e:
#         print(e)
# ##    bot.load_extension("cogs.utility")

# @bot.event
# async def on_guild_role_create(role):
#     updateRoles(currGuild.roles)
#     print(f'Roles file has been updated! Added role {role.name}({role.id})')

# @bot.event
# async def on_guild_role_delete(role):
#     updateRoles(currGuild.roles)
#     print(f'Roles file has been updated! Removed role {role.name}({role.id})')

# @bot.event
# async def on_guild_role_update(before, after):
#     updateRoles(currGuild.roles)
#     print(f'Roles file has been updated! Updated role from {before.name}({before.id}) to {after.name}({after.id})')

# @bot.event
# async def on_member_join(member):
#     roleFile = open('roles_test.json', 'r')
#     roleDict = json.loads(roleFile.read())
#     print(f'{member.name} has joined the server!')
#     await member.add_roles(currGuild.get_role(roleDict['Lvl 0 Thief']))
#     print(f'{member.name} has been given role "Lvl 0 Thief"')
#     roleFile.close()

# @bot.event
# async def on_member_remove(member):
#     print(f'{member.name} has left the server!')

# @bot.event
# async def on_voice_state_update(member, before, after):
#     if(member == bot.user):
#         return
#     if(before.channel == None):
#         if(member.nick == None):
#             msg = f'{member.name} just joined {after.channel}'
#         else:
#             msg = f'{member.nick} just joined {after.channel}'
#         channel = get(currGuild.channels, name='voiceless-spam', type=discord.ChannelType.text)
#         await channel.send(content=msg, tts=True, delete_after=10)
#     if(after.channel == None):
#         if(member.nick == None):
#             msg = f'{member.name} just left {before.channel}'
#         else:
#             msg = f'{member.nick} just left {before.channel}'
#         channel = get(currGuild.channels, name='voiceless-spam', type=discord.ChannelType.text)
#         await channel.send(content=msg, tts=True, delete_after=10)

# @bot.event
# async def on_command_error(ctx, error):
#     if(isinstance(error, commands.BadArgument)):
#         if(ctx.command.name == 'roll'):
#             await ctx.send('Roll was given unsuitable arguments! Please retry with valid integer inputs.')

## Friday class definition
class Friday(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents = intents,
            application_id = APPID
        )
        self.currGuild = None
        for guild in self.guilds:
            if guild.name == GUILD: 
                self.currGuild = guild
                break
        self.initial_extensions = [
            "cogs.utility"
        ]
    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)
        await bot.tree.sync(guild = self.currGuild)
    
    async def on_ready(self):
        print(discord.__version__)
        print(
            f'{self.user} has connected to Discord!\n'
            f'{self.user} is connected to {self.currGuild.name}(id: {self.currGuild.id})\n\n'
        )
        updateRoles(self.currGuild.roles)

    async def on_guild_role_create(self, role):
        if(role.guild == self.currGuild):
            updateRoles(self.currGuild.roles)
            print(f'Roles file has been updated! Added role {role.name}({role.id})')

    async def on_guild_role_delete(self, role):
        if(role.guild == self.currGuild):
            updateRoles(self.currGuild.roles)
            print(f'Roles file has been updated! Removed role {role.name}({role.id})')

    async def on_guild_role_update(self, before, after):
        if(before.guild == self.currGuild):
            updateRoles(self.currGuild.roles)
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

    @commands.command(name="reload")
    async def reload(self, ctx, extension):
        bot.reload_extension(extension)

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

bot = Friday()
bot.run(TOKEN)
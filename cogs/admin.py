import discord
import random
import functools
import json
import os
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', '.env'))
GUILD = os.getenv('DISCORD_GUILD')

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Admin cog loaded.')
    
    def is_guild_owner_intr():
        def predicate(interaction: discord.Interaction):
            return interaction.guild is not None and interaction.guild.owner_id == interaction.user.id
        return app_commands.check(predicate)

    def is_guild_owner_ctx():
        def predicate(ctx):
            return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
        return commands.check(predicate)

    @commands.command(name="reloadAll", description="For reloading all cogs", usage="!reloadAll")
    @is_guild_owner_ctx()
    async def reloadAll(self, ctx):
        try:
            for ext in self.bot.getCogs():
                await self.bot.reload_extension(ext)
            print("All cogs reloaded successfully")
        except commands.ExtensionError as e:
            print(e)
    @reloadAll.error
    async def reloadAll_error(self, ctx, error):
        print(f'{ctx.author.display_name} does not have the necessary permissions to access !{ctx.command.name}.')
    
    @commands.command(name="clear", description="For clearing app commands", usage="!clear")
    @is_guild_owner_ctx()
    async def clear(self, ctx):
        self.bot.tree.clear_commands(guild=None)
        print("Commands cleared.")
    @clear.error
    async def clear_error(self, ctx, error):
        print(error)
        print(f'{ctx.author.display_name} does not have the necessary permissions to access !{ctx.command.name}.')

    @commands.command(name="sync", description="For syncing app commands", usage="!sync")
    @is_guild_owner_ctx()
    async def sync(self, ctx):
        
        fmt = await self.bot.tree.sync()
        print(f'Synced {len(fmt)} commands.')
    @sync.error
    async def sync_error(self, ctx, error):
        print(error)
        print(f'{ctx.author.display_name} does not have the necessary permissions to access !{ctx.command.name}.')
    
    @commands.command(name="backupRoles", description="For backing up roles of users in server", usage="!backupRoles")
    @is_guild_owner_ctx()
    async def backupRoles(self, ctx):
        members = ctx.guild.members
        backup = {}
        for i in range(len(members)):
            roleList = []
            currRoles = members[i].roles
            for e in currRoles:
                roleList.append(str(e.id))
            roleList = ','.join(roleList)
            backup[members[i].id] = roleList
            print(f'Backed up {members[i].name}\'s roles sucessfully')
        roleFile = open('backups/memberRolesBackup.json', 'w')
        roleFile.write(json.dumps(backup, indent=4))
        roleFile.close()
    @backupRoles.error
    async def backupRoles_error(self, ctx, error):
        print(error)
        print(f'{ctx.author.display_name} does not have the necessary permissions to access !{ctx.command.name}.')

    @commands.command(name="backupNames", description="For backing up usernames of users in server", usage="!backupNames")
    @is_guild_owner_ctx()
    async def backupNames(self, ctx):
        members = ctx.guild.members
        backup = {}
        for i in range(len(members)):
            backup[members[i].id] = members[i].name
            print(f'Backed up {members[i].name}\'s id sucessfully')
        roleFile = open('backups/memberNamesBackup.json', 'w')
        roleFile.write(json.dumps(backup, indent=4))
        roleFile.close()
    @backupNames.error
    async def backupNames_error(self, ctx, error):
        print(error)
        print(f'{ctx.author.display_name} does not have the necessary permissions to access !{ctx.command.name}.')

    @commands.command(name="removeBackup", description="For permanently removing backup of a user", usage="!removeBackup {username}")
    @is_guild_owner_ctx()
    async def removeBackup(self, ctx, user:str):
        namesFile = open('backups/memberNamesBackup.json', 'r+')
        # rolesFile = open('backups/memberRolesBackup.json', 'r+')
        namesDict = json.loads(namesFile.read())
        # rolesDict = json.loads(rolesFile.read())
        print(namesDict)
        if user in namesDict.values():
            for uID in namesDict:
                if namesDict[uID] == user:
                    namesDict.pop(uID)
            # for uID in rolesDict:
            #     if rolesDict[uID] == user:
            #         rolesDict.pop(uID)
        print(namesDict)
        namesFile.write(json.dumps(namesDict, indent=4))
        # rolesFile.write(json.dumps(rolesDict, indent=4))
        namesFile.close()
        # rolesFile.close()
    @removeBackup
    async def removeBackup_error(self, ctx, error):
        print(error)

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
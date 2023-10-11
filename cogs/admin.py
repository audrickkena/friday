import discord
import random
import functools
import json
import os

import danki_checks
import danki_exceptions
import danki_enums

from discord.ext import commands
from discord.ext import tasks
from discord import app_commands

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.setup = self.bot.getAdminSetup()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{danki_enums.Console.getPrefix()} Admin cog loaded.')
    
    def is_guild_owner_intr():
        def predicate(interaction: discord.Interaction):
            return interaction.guild is not None and interaction.guild.owner_id == interaction.user.id
        return app_commands.check(predicate)

    def is_guild_owner_ctx():
        def predicate(ctx):
            return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
        return commands.check(predicate)

    @commands.command(name="reloadAll", description="For reloading all cogs", usage="!reloadAll")
    async def reloadAll(self, ctx):
        try:
            if await danki_checks.checkHasRoles(ctx.author, 'reloadAll', self.setup['required']) == True:
                for ext in self.bot.getCogs():
                    await self.bot.reload_extension(ext)
                await ctx.send("All cogs reloaded successfully", ephemeral=True)
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await ctx.send(f'You do not have the necessary roles required to use this command!\nIf this is a mistake, please contact the admin or raise an issue in github')
        except Exception as err:
            print(f'{err}')
            await ctx.send(f'{danki_enums.DiscordOut.ERROR}')
            raise err
    
    @commands.command(name="clear", description="For clearing app commands", usage="!clear")
    async def clear(self, ctx):
        try:
            if await danki_checks.checkHasRoles(ctx.author, 'clear', self.setup['required']) == True:
                self.bot.tree.clear_commands(guild=None)
                await ctx.send("Commands cleared.", ephemeral=True)
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await ctx.send(f'You do not have the necessary roles required to use this command!\nIf this is a mistake, please contact the admin or raise an issue in github')
        except Exception as err:
            print(f'{err}')
            await ctx.send(f'{danki_enums.DiscordOut.ERROR}')
            raise err


    @commands.command(name="sync", description="For syncing app commands", usage="!sync")
    async def sync(self, ctx):
        try:
            if await danki_checks.checkHasRoles(ctx.author, 'sync', self.setup['required']) == True:
                fmt = await self.bot.tree.sync()
                await ctx.send(f'Synced {len(fmt)} commands.', ephemeral=True)
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await ctx.send(f'You do not have the necessary roles required to use this command!\nIf this is a mistake, please contact the admin or raise an issue in github')
        except Exception as err:
            print(f'{err}')
            await ctx.send(f'{danki_enums.DiscordOut.ERROR}')
            raise err
    
    @commands.command(name="backupRoles", description="For backing up roles of users in server", usage="!backupRoles")
    async def backupRoles(self, ctx):
        try:
            if await danki_checks.checkHasRoles(ctx.author, 'backupRoles', self.setup['required']) == True:
                members = ctx.guild.members
                backup = {}
                for i in range(len(members)):
                    roleList = []
                    currRoles = members[i].roles
                    for e in currRoles:
                        if e.id == 866927479419830282:
                            continue
                        roleList.append(str(e.id))
                    roleList = ','.join(roleList)
                    backup[members[i].id] = roleList
                    print(f'Backed up {members[i].name}\'s roles sucessfully')
                roleFile = open('backups/memberRolesBackup.json', 'w')
                roleFile.write(json.dumps(backup, indent=4))
                roleFile.close()
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await ctx.send(f'You do not have the necessary roles required to use this command!\nIf this is a mistake, please contact the admin or raise an issue in github')
        except Exception as err:
            print(f'{err}')
            await ctx.send(f'{danki_enums.DiscordOut.ERROR}')
            raise err

    @commands.command(name="backupNames", description="For backing up usernames of users in server", usage="!backupNames")
    async def backupNames(self, ctx):
        try:
            if await danki_checks.checkHasRoles(ctx.author, 'backupNames', self.setup['required']) == True:    
                members = ctx.guild.members
                backup = {}
                for i in range(len(members)):
                    backup[members[i].id] = members[i].name
                    print(f'Backed up {members[i].name}\'s id sucessfully')
                roleFile = open('backups/memberNamesBackup.json', 'w')
                roleFile.write(json.dumps(backup, indent=4))
                roleFile.close()
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await ctx.send(f'You do not have the necessary roles required to use this command!\nIf this is a mistake, please contact the admin or raise an issue in github')
        except Exception as err:
            print(f'{err}')
            await ctx.send(f'{danki_enums.DiscordOut.ERROR}')
            raise err

    @commands.command(name="removeBackup", description="For permanently removing backup of a user", usage="!removeBackup {username}")
    async def removeBackup(self, ctx, user:str):
        try:
            if await danki_checks.checkHasRoles(ctx.author, 'removeBackup', self.setup['required']) == True:
                namesFile = open('backups/memberNamesBackup.json', 'r+')
                rolesFile = open('backups/memberRolesBackup.json', 'r+')
                namesDict = json.loads(namesFile.read())
                rolesDict = json.loads(rolesFile.read())
                delete = ''
                if user in namesDict.values():
                    for uID in namesDict:
                        if namesDict[uID] == user:
                            print(f'{namesDict[uID]} still backed up -> Deleting Backup')
                            delete = uID
                            break
                if delete != '':
                    namesDict.pop(delete)
                    rolesDict.pop(delete)
                    namesFile.seek(0)
                    rolesFile.seek(0)
                    namesFile.write(json.dumps(namesDict, indent=4))
                    rolesFile.write(json.dumps(rolesDict, indent=4))
                else:
                    print(f'{user} is already not backed up!')
                namesFile.close()
                rolesFile.close()
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await ctx.send(f'You do not have the necessary roles required to use this command!\nIf this is a mistake, please contact the admin or raise an issue in github')
        except Exception as err:
            print(f'{err}')
            await ctx.send(f'{danki_enums.DiscordOut.ERROR}')
            raise err

    @commands.command(name='close', description='For closing the bot', usage = '!close')
    async def close(self, ctx):
        try:
            if await danki_checks.checkHasRoles(ctx.author, 'close', self.setup['required']) == True:
                await ctx.send('Shutting down bot')
                await ctx.bot.close()
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await ctx.send(f'You do not have the necessary roles required to use this command!\nIf this is a mistake, please contact the admin or raise an issue in github')
        except Exception as err:
            print(f'{err}')
            await ctx.send(f'{danki_enums.DiscordOut.ERROR}')
            raise err

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
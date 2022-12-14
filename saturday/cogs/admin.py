import discord
import random
import functools
import json
import os
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def is_guild_owner():
        def predicate(interaction: discord.Interaction):
            return interaction.guild is not None and interaction.guild.owner_id == interaction.user.id
        return app_commands.check(predicate)

    @app_commands.command(name="reload", description="For reloading cogs")
    @is_guild_owner()
    async def reload(self, interaction: discord.Interaction, module: str):
        try:
            await self.bot.reload_extension(module)
            await interaction.response.send_message(f'{module} reloaded successfully', ephemeral=True)
        except commands.ExtensionError as e:
            print(e)
            await interaction.response.send_message(f'{module} reloaded unsuccessfully. Please check server for more info', ephemeral=True)
    @reload.error
    async def reload_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(f'You do not have the necessary permissions to access /{interaction.command.name}. If this is not the intended effect, please contact the server admin.', ephemeral=True)

    @commands.command(name="clear", description="For clearing app commands", usage="!clear")
    async def clear(self, ctx):
        fmt = await ctx.bot.tree.clear_commands(guild=ctx.guild)
        await ctx.send(f'Cleared {len(fmt)} commands.')
        
    @commands.command(name="sync", description="For syncing app commands", usage="!sync")
    async def sync(self, ctx):
        
        fmt = await self.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f'Synced {len(fmt)} commands.')
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot), guilds=[discord.Object(id=1051422874143035412)])
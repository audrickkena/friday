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
        def predicate(ctx):
            return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
        return commands.check(predicate)
    @app_commands.command(name="reload")
    @is_guild_owner()
    async def reload(self, interaction: discord.Interaction, module: str):
        try:
            await self.bot.reload_extension(module)
            await interaction.response.send_message(f'{module} reloaded successfully', ephemeral=True)
        except commands.ExtensionError as e:
            print(e)
            await interaction.response.send_message(f'{module} reloaded unsuccessfully. Please check server for more info', ephemeral=True)
        except commands.CheckFailure as e:
            print(e)
            await interaction.response.send_message(f'You do not have permission to use this command! Contact the admin if this is not the intended effect')
        

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
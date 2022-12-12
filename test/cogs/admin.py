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

    @app_commands.command(name="reload")
    @commands.has_permissions(administrator=True)
    async def reload(self, interaction: discord.Interaction, module: str):
        try:
            await self.bot.reload_extension(module)
            await interaction.response.send_message(f'{module} reloaded successfully')
        except commands.ExtensionError as e:
            print(e)
            await interaction.response.send_message(f'{module} reloaded unsuccessfully. Please check server for more info')

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
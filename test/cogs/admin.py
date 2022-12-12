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
    async def reload(self, ctx, module):
        try:
            await self.bot.reload_extension(module)
        except commands.ExtensionError as e:
            print(e)

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
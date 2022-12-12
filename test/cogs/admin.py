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

    @app_commands.command(name="reload")
    @is_guild_owner()
    async def reload(self, interaction: discord.Interaction, module: str):
        try:
            await self.bot.reload_extension(module)
            await interaction.response.send_message(f'{module} reloaded successfully', ephemeral=True)
        except commands.ExtensionError as e:
            print(e)
            await interaction.response.send_message(f'{module} reloaded unsuccessfully. Please check server for more info', ephemeral=True)

    async def on_command_error(interaction: discord.Interaction, error):
        if(isinstance(error, commands.CheckFailure)):
            await interaction.response.send_message(f'You do not have the necessary permissions to access {interaction.command}. If this is not the intended effect, please contact the server admin.')
        

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
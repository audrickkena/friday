import discord

from discord.ext import commands
from discord import app_commands

class dict(app_commands.Group):
    @app_commands.command(name='list', description='For listing contents of server dictionary')
    async def listDict(self, interaction: discord.Interaction):
        await interaction.response.send_message('Hi', ephemeral=True)

async def setup(bot):
    bot.tree.add_command(dict(name='dict', description='For commands related to the server\'s dictionary'))
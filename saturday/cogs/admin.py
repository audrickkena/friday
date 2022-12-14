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
    @reload.error
    async def reload_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(f'You do not have the necessary permissions to access /{interaction.command.name}. If this is not the intended effect, please contact the server admin.', ephemeral=True)
    
    @commands.command(name='help')
    async def help(self, ctx):
        cogs = self.bot.cogs
        message = ''
        for cogName, cog in cogs.items():
            message += f'{cogName} cog slash-commands:\n'
            message += self.getAppCommands(cog)
            message += f'{cogName} cog prefix-commands:\n'
            message += self.getCommands(cog)
            message += '\n'
        await ctx.send(content=message)
        
    def getAppCommands(self, cog):
        message = ''
        commands = cog.get_app_commands()
        for command in commands:
            message += f'  - /{command.name}: {command.description}\n'
            message += f'      - usage: /{command.name}'
            for parameter in command.parameters:
                message += f' {{{parameter.name}}}'
            message += '\n'
        return message

    def getCommands(self, cog):
        message = ''
        commands = cog.get_commands()
        for command in commands:
            message += f'  - !{command.name}: {command.description}\n'
            message += f'      - usage: {command.usage}\n'
        return message
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
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
    
    @commands.command(name='help', description='For getting information on usable commands', usage='!help')
    async def help(self, ctx):
        cogs = self.bot.cogs
        embedList = []
        for cogName, cog in cogs.items():
            message = discord.Embed(
                title=cogName,
                description=f'{cogName} cog commands:\n',
                color=discord.Colour.blue()
            )
            message.add_field(name='\n\u200b', value='**Slash commands**', inline=False)
            self.getAppCommands(cog, message)
            message.add_field(name='\n\u200b', value='**Prefix commands**', inline=False)
            self.getCommands(cog, message)
            embedList.append(message)
        await ctx.send(embeds=embedList)
        
    def getAppCommands(self, cog, embed):
        commands = cog.get_app_commands()
        for command in commands:
            message = f'- description: {command.description}\n- usage: /{command.name}'
            for parameter in command.parameters:
                message += f' {{{parameter.name}}}'
            embed.add_field(name=command.name, value=message, inline=False)

    def getCommands(self, cog, embed):
        commands = cog.get_commands()
        for command in commands:
            message = f'- description: {command.description}\n- usage: {command.usage}'
            embed.add_field(name=command.name, value=message, inline=False)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
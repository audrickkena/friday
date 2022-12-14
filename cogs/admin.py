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

    @commands.command(name="reloadAll", description="For reloading all cogs")
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
        await ctx.bot.tree.clear_commands()
        print("Commands cleared.")
    @clear.error
    async def clear_error(self, ctx, error):
        print(f'{ctx.author.display_name} does not have the necessary permissions to access !{ctx.command.name}.')

    @commands.command(name="sync", description="For syncing app commands", usage="!sync")
    @is_guild_owner_ctx()
    async def sync(self, ctx):
        
        fmt = await self.bot.tree.sync()
        print(f'Synced {len(fmt)} commands.')
    @sync.error
    async def sync_error(self, ctx, error):
        print(f'{ctx.author.display_name} does not have the necessary permissions to access !{ctx.command.name}.')

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
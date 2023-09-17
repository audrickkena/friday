import discord
import functools
import random
import datetime
import json
from discord.ext import commands
from discord import app_commands

class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Miscellaneous cog loaded.')

    @app_commands.command(name='hi', description="For lonely people")
    async def hi(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'hello {interaction.user.display_name}', ephemeral=True)

    @app_commands.command(name='ping', description="For really bored people")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message('Pong', ephemeral=True)

    @app_commands.command(name="roll", description="For rolling a number of dices with a number of sides")
    async def rollDice(self, interaction: discord.Interaction, dice_num : int, sides_num : int):
        if(dice_num > 30):
            await interaction.response.send_message('Sorry, max value for the number of dice is 30!')
            return
        if(sides_num > 30):
            await interaction.response.send_message('Sorry max value for the number of dice is 30!')
            return
        if(interaction.channel.name=="command-spam"):
            result = [str(random.choice(range(1, sides_num + 1))) for _ in range(dice_num)]
            msgDices = 'Individual dices: ' + ', '.join(result)
            msgTotal = 'Total roll value: ' + str(functools.reduce(lambda a, b: int(a) + int(b), result))
            msgMax = str(dice_num * sides_num)
            await interaction.response.send_message(f'{msgDices}\n\n{msgTotal}\nMax roll: {msgMax}')


    # TODO: /popoff command
    @app_commands.command(name='popoff', description='For when a user is popping off')
    async def popoff(self, interaction: discord.Interaction, user_mention: str):
        if user_mention[1] != '@' or user_mention[2] == '&':
            await interaction.response.send_message(f'{user_mention} is not a mention of a user in the server! Type @{{username}} to ensure that user is mentioned properly!', ephemeral=True)
        else:
            id = user_mention[2:-1]
            if not self.fileExists('misc/popoff.json'):
                with open('misc/popoff.json', 'w') as f:
                    f.write(json.dumps({id : '1'}, indent=4))
                    await interaction.response.send_message(f'{user_mention} has popped off 1 times')
            else:
                with open('misc/popoff.json', 'r+') as f:
                    old = json.loads(f.read())
                    if id in old.keys():
                        old[id] = str(int(old[id]) + 1)
                    else:
                        old[id] = '1'
                    f.seek(0)
                    f.write(json.dumps(old, indent=4))
                    await interaction.response.send_message(f'{user_mention} has popped off {old[id]} times')
    
    def fileExists(self, filename):
        try:
            with open(filename, 'r') as f:
                return True
        except FileNotFoundError:
            return False
        


    #######################################
    ########## SELAMAT FUNCTIONS ##########
    selamatGrp = app_commands.Group(name='selamat', description='For commands related to greeting others in the server')

    @selamatGrp.command(name='pagi', description="For greeting a fellow member in the morning")
    async def pagi(self, interaction: discord.Interaction, user_mention: str):
        if user_mention[1] != '@' or user_mention[2] == '&':
            await interaction.response.send_message(f'{user_mention} is not a mention of a user in the server! Type @{{username}} to ensure that user is mention properly!', ephemeral=True)
        else:
            if self.checkTime() == 1:
                await interaction.response.send_message('It is currently afternoon! Try /selamat petang {username}!', ephemeral=True)
            elif self.checkTime() == 2:
                await interaction.response.send_message('It is currently evening! Try /selamat malam {username}!', ephemeral=True)
            else:
                member = discord.utils.get(interaction.client.get_all_members(), id=int(user_mention[2:-1]))
                sender = interaction.guild.get_member(interaction.user.id)
                if member.status == discord.Status.offline or member.status == discord.Status.dnd:
                    await interaction.response.send_message(f'{member.display_name} is not available! Wait till they\'re free and online to greet them!', ephemeral=True)
                    return
                if sender.status == discord.Status.offline or sender.status == discord.Status.dnd:
                    await interaction.response.send_message(f'You are appearing busy or offline! Go online for you to greet your friends!', ephemeral=True)
                    return 
                if self.checkCooldown(str(sender.id), str(member.id)) == False:
                    await interaction.response.send_message(f'You have already greeted {member.display_name} today! Try again later!', ephemeral=True)
                    return 
                if discord.utils.get(interaction.guild.roles, name=f'rude to {sender.display_name}') == None:
                    role = await interaction.guild.create_role(name=f'rude to {sender.display_name}')
                else:
                    role = discord.utils.get(interaction.guild.roles, name=f'rude to {sender.display_name}')
                rudeRole = discord.utils.get(interaction.guild.roles, name=f'rude to {member.display_name}')
                if rudeRole != None:
                    if sender.get_role(rudeRole.id) != None:
                        await sender.remove_roles(rudeRole)
                        await interaction.response.send_message(f'{user_mention} you have been greeted back by <@{sender.id}>')
                        return
                await member.add_roles(role)
                await interaction.response.send_message(f'{user_mention} you have been greeted by <@{sender.id}>')

    @selamatGrp.command(name='petang', description="For greeting a fellow member in the afternoon")
    async def petang(self, interaction: discord.Interaction, user_mention: str):
        if user_mention[1] != '@' or user_mention[2] == '&':
            await interaction.response.send_message(f'{user_mention} is not a mention of a user in the server! Type @{{username}} to ensure that user is mentioned properly!', ephemeral=True)
        else:
            if self.checkTime() == 0:
                await interaction.response.send_message('It is currently morning! Try /selamat pagi {username}!', ephemeral=True)
            elif self.checkTime() == 2:
                await interaction.response.send_message('It is currently evening! Try /selamat malam {username}!', ephemeral=True)
            else:
                member = discord.utils.get(interaction.client.get_all_members(), id=int(user_mention[2:-1]))
                sender = interaction.guild.get_member(interaction.user.id)
                if member.status == discord.Status.offline or member.status == discord.Status.dnd:
                    await interaction.response.send_message(f'{member.display_name} is not available! Wait till they\'re free and online to greet them!', ephemeral=True)
                    return
                if sender.status == discord.Status.offline or sender.status == discord.Status.dnd:
                    await interaction.response.send_message(f'You are appearing busy or offline! Go online for you to greet your friends!', ephemeral=True)
                    return 
                if self.checkCooldown(str(sender.id), str(member.id)) == False:
                    await interaction.response.send_message(f'You have already greeted {member.display_name} today! Try again later!', ephemeral=True)
                    return 
                if discord.utils.get(interaction.guild.roles, name=f'rude to {sender.display_name}') == None:
                    role = await interaction.guild.create_role(name=f'rude to {sender.display_name}')
                else:
                    role = discord.utils.get(interaction.guild.roles, name=f'rude to {sender.display_name}')
                rudeRole = discord.utils.get(interaction.guild.roles, name=f'rude to {member.display_name}')
                if rudeRole != None:
                    if sender.get_role(rudeRole.id) != None:
                        await sender.remove_roles(rudeRole)
                        await interaction.response.send_message(f'{user_mention} you have been greeted back by <@{sender.id}>')
                        return
                await member.add_roles(role)
                await interaction.response.send_message(f'{user_mention} you have been greeted by <@{sender.id}>')

    @selamatGrp.command(name='malam', description="For greeting a fellow member in the evening")
    async def malam(self, interaction: discord.Interaction, user_mention: str):
        if user_mention[1] != '@' or user_mention[2] == '&':
            await interaction.response.send_message(f'{user_mention} is not a mention of a user in the server! Type @{{username}} to ensure that user is mention properly!', ephemeral=True)
        else:
            if self.checkTime() == 1:
                await interaction.response.send_message('It is currently afternoon! Try /selamat petang {username}!', ephemeral=True)
            elif self.checkTime() == 0:
                await interaction.response.send_message('It is currently morning! Try /selamat pagi {username}!', ephemeral=True)
            else:
                member = discord.utils.get(interaction.client.get_all_members(), id=int(user_mention[2:-1]))
                sender = interaction.guild.get_member(interaction.user.id)
                if member.status == discord.Status.offline or member.status == discord.Status.dnd:
                    await interaction.response.send_message(f'{member.display_name} is not available! Wait till they\'re free and online to greet them!', ephemeral=True)
                    return
                if sender.status == discord.Status.offline or sender.status == discord.Status.dnd:
                    await interaction.response.send_message(f'You are appearing busy or offline! Go online for you to greet your friends!', ephemeral=True)
                    return 
                if self.checkCooldown(str(sender.id), str(member.id)) == False:
                    await interaction.response.send_message(f'You have already greeted {member.display_name} today! Try again later!', ephemeral=True)
                    return 
                if discord.utils.get(interaction.guild.roles, name=f'rude to {sender.display_name}') == None:
                    role = await interaction.guild.create_role(name=f'rude to {sender.display_name}')
                else:
                    role = discord.utils.get(interaction.guild.roles, name=f'rude to {sender.display_name}')
                rudeRole = discord.utils.get(interaction.guild.roles, name=f'rude to {member.display_name}')
                if rudeRole != None:
                    if sender.get_role(rudeRole.id) != None:
                        await sender.remove_roles(rudeRole)
                        await interaction.response.send_message(f'{user_mention} you have been greeted back by <@{sender.id}>')
                        return
                await member.add_roles(role)
                await interaction.response.send_message(f'{user_mention} you have been greeted by <@{sender.id}>')

    def checkTime(self):
        currDateTime = datetime.datetime.now() + datetime.timedelta(hours=8)
        if currDateTime.hour < 12:
            return 0
        elif currDateTime.hour > 18:
            return 2
        return 1
    
    # check misc/selamat/senderID.json 
    def checkCooldown(self, senderID : str, receiverID : str):
        currDate = datetime.datetime.now() + datetime.timedelta(hours=8)
        entries = {}
        if self.fileExists(f'{senderID}.json'):
            with open(f'{senderID}.json', 'r+') as f:
                entries = json.loads(f.read())
                if receiverID in entries.keys():
                    # dates saved in YYYY-MM-DD-HH-MIN format
                    pastDate = datetime.datetime(int(entries[receiverID].split('-')[0]), int(entries[receiverID].split('-')[1]), int(entries[receiverID].split('-')[2]), int(entries[receiverID].split('-')[3]), int(entries[receiverID].split('-')[4]))
                    if pastDate + datetime.timedelta(days=1) > currDate: # if it's been 1 day since the previous selamat
                        print((datetime.timedelta(days=1) - (currDate - pastDate)).strfrtime('%H-%M'))
                        return False
                entries[receiverID] = currDate.strftime('%Y-%m-%d-%H-%M')
                f.seek(0)
                f.write(json.dumps(entries, indent=4))
        else:
            with open(f'{senderID}.json', 'w') as f:
                entries[receiverID] = currDate.strftime('%Y-%m-%d-%H-%M')
                f.write(json.dumps(entries, indent=4))
        return True


    
    ########## SELAMAT FUNCTIONS ##########
    #######################################



async def setup(bot: commands.Bot):
    await bot.add_cog(Misc(bot))
import discord
import functools
import random
import datetime
import json
import os
from discord.ext import commands
from discord import app_commands
# import asyncio
# import pytube




class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # self.vc = None
        # self.stop_audio_task = None

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


    @app_commands.command(name='popoff', description='For when a user is popping off')
    # TODO: limit amount of times popoff is said per hour
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
            if int(id) == self.bot.application_id:
                sender = interaction.guild.get_member(interaction.user.id)
                channel = self.bot.get_channel(interaction.channel_id)
                await channel.send(f'Danki thanks {sender.display_name} for the popoff!')
    
    def fileExists(self, filename):
        try:
            with open(filename, 'r') as f:
                return True
        except FileNotFoundError:
            return False
        
    @app_commands.command(name='banter', description='For reminding everyone that what you said was just a joke')
    async def banter(self, interaction: discord.Interaction):
        tts_channel = discord.utils.get(interaction.guild.text_channels, name='voiceless-spam-lvl10')
        await tts_channel.send(f'{interaction.guild.get_member(interaction.user.id).display_name} was merely joking and is not liable for any hurt feelings that what they said may have caused. Thank you for your understanding', tts=True, delete_after=20)
        await interaction.response.send_message(f'Disclaimer sent to voiceless-spam-lvl10', ephemeral=True)

    @app_commands.command(name='notbanter', description='For reminding everyone that what you said was NOT a joke')
    async def notbanter(self, interaction: discord.Interaction, user_mention: str):
        tts_channel = discord.utils.get(interaction.guild.text_channels, name='voiceless-spam-lvl10')
        messages = [
        f'{interaction.guild.get_member(interaction.user.id).display_name} meant what they said to {user_mention} from the bottom of their heart',
        f'Did {interaction.guild.get_member(interaction.user.id).display_name} fucking stutter',
        ]
        chosen_message = random.choice(messages)
        await tts_channel.send(chosen_message, tts=True, delete_after=60)        
        await interaction.response.send_message(f'Disclaimer sent to voiceless-spam-lvl10', ephemeral=True)


    # @commands.Cog.listener()
    # async def on_voice_state_update(self, member, before, after):
    #     role_name = "This"  # Replace with the actual role name

    #     # Check if the member has the specified role
    #     role = discord.utils.get(member.roles, name=role_name)
    #     if role and not before.channel and after.channel:
    #         if member.id == self.bot.user.id:
    #             return
    #         # Connect to the user's voice channel
    #         self.vc = await after.channel.connect()
    #         specific_url = 'https://www.youtube.com/watch?v=2BCgSYNteVo&ab_channel=CHORUSLOOPS'
    #         # Get the audio stream URL from the YouTube video (you'll need to define 'specific_url' here)
    #         video = pytube.YouTube(specific_url)
    #         audio_stream = video.streams.filter(only_audio=True).first()
    #         url2 = audio_stream.url
    #         # Play the audio stream
    #         self.vc.play(discord.FFmpegPCMAudio(url2, executable='ffmpeg.exe'))
    #         self.stop_audio_task = asyncio.create_task(self.stop_audio_after_duration(5))


    # async def stop_audio_after_duration(self, duration):
    #     await asyncio.sleep(duration)
    #     if self.vc and self.vc.is_playing():
    #         self.vc.stop()
    #         await self.vc.disconnect()

   

    #######################################
    ########## SELAMAT FUNCTIONS ##########
    #######################################

    selamatGrp = app_commands.Group(name='selamat', description='For commands related to greeting others in the server')

    #####################################################################
    ###################### DEFINING DEFAULT CHECKS ######################
    #####################################################################
    
    
    # async def selamatErrors(interaction: discord.Interaction, error):
    #     if isinstance(error, app_commands.CheckFailure):
    #         print(f'{interaction.command} has failed!')
    #         print(str(error))
    #     await interaction.response.send_message(f'{interaction.command} is broken! Please contact the admin about this issue!')
    # @selamatGrp.error(selamatErrors)
    #####################################################################
    ###################### END OF DEFAULT CHECKS ########################
    #####################################################################

    @selamatGrp.command(name='pagi', description="For greeting a fellow member in the morning")
    @app_commands.checks.has_any_role('Lvl 100 Mafia Warlord', 'Lvl 10 Boss')
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
                greeting = 'Selamat pagi'
                await self.greet(interaction, sender, member, user_mention, greeting)

    @selamatGrp.command(name='petang', description="For greeting a fellow member in the afternoon")
    @app_commands.checks.has_any_role('Lvl 100 Mafia Warlord', 'Lvl 10 Boss')
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
                greeting = 'Selamat petang'
                await self.greet(interaction, sender, member, user_mention, greeting)

    @selamatGrp.command(name='malam', description="For greeting a fellow member in the evening")
    @app_commands.checks.has_any_role('Lvl 100 Mafia Warlord', 'Lvl 10 Boss')
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
                greeting = 'Selamat malam'
                await self.greet(interaction, sender, member, user_mention, greeting)
                

    async def greet(self, interaction: discord.Interaction, sender, member, user_mention, greeting):
        if member.status == discord.Status.offline or member.status == discord.Status.dnd:
            await interaction.response.send_message(f'{member.display_name} is not available! Wait till they\'re free and online to greet them!', ephemeral=True)
            return
        if sender.status == discord.Status.offline or sender.status == discord.Status.dnd:
            await interaction.response.send_message(f'You are appearing busy or offline! Go online for you to greet your friends!', ephemeral=True)
            return 
        if self.checkCooldown(str(sender.id), str(member.id))[0] == False:
            countdown = self.checkCooldown(str(sender.id), str(member.id))[1]
            await interaction.response.send_message(f'You have already greeted {member.display_name} today! Try again in {countdown[0]} hours {countdown[1]} mins {countdown[2]} secs', ephemeral=True)
            return 
        if int(user_mention[2:-1]) == self.bot.application_id:
            await interaction.response.send_message(f'Thank you {sender.display_name} for your greeting! {greeting} to you too!')
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
    # TODO: check if checks.cooldown can be used here instead
    def checkCooldown(self, senderID : str, receiverID : str):
        currDate = datetime.datetime.now() + datetime.timedelta(hours=8)
        entries = {}
        if self.fileExists(f'misc/selamat/{senderID}.json'):
            with open(f'misc/selamat/{senderID}.json', 'r+') as f:
                entries = json.loads(f.read())
                if receiverID in entries.keys():
                    # dates saved in YYYY-MM-DD-HH-MIN format
                    pastDate = datetime.datetime(int(entries[receiverID].split('-')[0]), int(entries[receiverID].split('-')[1]), int(entries[receiverID].split('-')[2]), int(entries[receiverID].split('-')[3]), int(entries[receiverID].split('-')[4]))
                    if pastDate + datetime.timedelta(days=1) > currDate: # if it's been 1 day since the previous selamat
                        countdown = str(datetime.timedelta(days=1) - (currDate - pastDate)).split('.')[0].split(':')
                        return [False, countdown]
                entries[receiverID] = currDate.strftime('%Y-%m-%d-%H-%M')
                f.seek(0)
                f.write(json.dumps(entries, indent=4))
        else:
            with open(f'misc/selamat/{senderID}.json', 'w') as f:
                entries[receiverID] = currDate.strftime('%Y-%m-%d-%H-%M')
                f.write(json.dumps(entries, indent=4))
        return [True, None]




    ##############################################
    ########## END OF SELAMAT FUNCTIONS ##########
    ##############################################

    ########################################################################
    ########## QUOTE COMMANDS ##############################################
    ########################################################################
    quoteGrp = app_commands.Group(name='quote', description='For commands related to quoting in the server')

    @quoteGrp.command(name='get', description="For getting a random quote from the server's database")
    @app_commands.checks.has_any_role('Coders')
    async def quote(self, interaction:discord.Interaction):
        chosen_quote = "@@@@@"
        
        if os.path.exists("quote_file.json") and os.path.getsize("quote_file.json") > 0:
            ## Open .json file
            with open("quote_file.json") as read_file:
                quote_data = json.load(read_file)
                rand_index = str(random.randint(1, len(quote_data)))

            ## Retrieve random .json entry
            print(quote_data[str(rand_index)])
            chosen_quote = quote_data[rand_index]["quote"]
            quoted_by = quote_data[rand_index]["addedBy"]
            quoted_on = quote_data[rand_index]["addedOn"]


            # ## Send random quote to user
            await interaction.response.send_message(f"### Your Quote: `{chosen_quote}`\n### - {quoted_by} {quoted_on}")

        else:
            return await interaction.response.send_message(":x: **No quotes exist yet!** :x:", ephemeral=True)

    @quoteGrp.command(name='make', description="For making a new quote for the server")
    @app_commands.checks.has_any_role('Coders')
    @app_commands.describe(added_quote = "What quote are you adding?")
    async def makequote(self, interaction:discord.Interaction, added_quote:str):

        try:
            added_by = interaction.user.name
            added_on = "{:%B %d, %Y}".format(datetime.datetime.now())

            if os.path.exists("quote_file.json") and os.path.getsize("quote_file.json") > 0:
                # Load existing quote from the JSON file
                with open("quote_file.json", "r") as file:
                    quote_data = json.load(file)
                for quote in quote_data:
                    if quote_data[quote]["quote"].lower() ==  added_quote.lower():
                        return await interaction.response.send_message(":x: **That quote already exists!** :x:", ephemeral=True)
            else:
                quote_data = {}
            
            # Add new quote
            new_quote = {
                "addedBy": added_by,
                "addedOn": added_on,
                "quote" : added_quote
            }

            quote_data[len(quote_data)+1] = new_quote

            with open("quote_file.json", "w") as file:
                json.dump(quote_data, file)
            
            await interaction.response.send_message(f"You added: \"{added_quote}\"")

        except json.JSONDecodeError as e:
            print(f"Error loading JSON: {e}")

    ########################################################################
    ########## QUOTE END ###################################################
    ########################################################################









    ##################################
    ########## Error Handling ########
    ##################################
    async def cog_app_command_error(self, interaction: discord.Interaction, error):
        print(str(error))
        if isinstance(error, app_commands.MissingAnyRole):
            missing = []
            user = interaction.guild.get_member(interaction.user.id)
            for role in error.missing_roles:
                print(role)
                if discord.utils.get(user.roles, name=role) == None:
                    missing.append(role)
            await interaction.response.send_message(f'You do not have the necessary roles to use /{interaction.command.qualified_name}! Here is the list of required roles:\n{missing}')
        else:
            await interaction.response.send_message(f'/{interaction.command.qualified_name} is broken! Please contact the admin about this issue!', ephemeral=True)









async def setup(bot: commands.Bot):
    
    await bot.add_cog(Misc(bot))
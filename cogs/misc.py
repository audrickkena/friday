import discord
import functools
import random
import datetime
import json
import os

import danki_enums
import danki_checks
import danki_exceptions

from discord.ext import commands
from discord import app_commands
import asyncio
import pytube




class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.setup = self.bot.getMiscSetup()
        self.botSetup = self.bot.getBotSetup()
        self.vc = None
        self.stop_audio_task = None
        self.musicQueue = []
        self.currSong = None
        self.message_music_curr = None
        self.message_music_queue = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{danki_enums.Console.getPrefix()} Miscellaneous cog loaded.')

    @app_commands.command(name='hi', description="For lonely people")
    async def hi(self, interaction: discord.Interaction):
        try:
            if await danki_checks.checkCommandNeedRoles(interaction.user, 'hi', self.setup['optional']) == True:
                await interaction.response.send_message(f'hello {interaction.user.display_name}', ephemeral=True)
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await interaction.response.send_message(f'You lack the necessary roles to use this command! {danki_enums.DiscordOut.ISSUE_GITHUB}', ephemeral=True)
        except Exception as err:
            await interaction.response.send_message(f'{danki_enums.DiscordOut.ERROR}', ephemeral=True)
            raise err
        

    @app_commands.command(name='ping', description="For really bored people")
    async def ping(self, interaction: discord.Interaction):
        try:
            if await danki_checks.checkCommandNeedRoles(interaction.user, 'ping', self.setup['optional']) == True:
                await interaction.response.send_message('Pong', ephemeral=True)
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await interaction.response.send_message(f'You lack the necessary roles to use this command! {danki_enums.DiscordOut.ISSUE_GITHUB}', ephemeral=True)
        except Exception as err:
            await interaction.response.send_message(f'{danki_enums.DiscordOut.ERROR}', ephemeral=True)
            raise err
        

    @app_commands.command(name="roll", description="For rolling a number of dices with a number of sides")
    async def rollDice(self, interaction: discord.Interaction, dice_num : int, sides_num : int):
        try:
            if await danki_checks.checkCommandNeedRoles(interaction.user, 'rollDice', self.setup['optional']) == True:
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
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await interaction.response.send_message(f'You lack the necessary roles to use this command! {danki_enums.DiscordOut.ISSUE_GITHUB}', ephemeral=True)
        except Exception as err:
            await interaction.response.send_message(f'{danki_enums.DiscordOut.ERROR}', ephemeral=True)
            raise err
        

    @app_commands.command(name='popoff', description='For when a user is popping off')
    # TODO: limit amount of times popoff is said per hour
    async def popoff(self, interaction: discord.Interaction, user_mention: str):
        try:
            if await danki_checks.checkCommandNeedRoles(interaction.user, 'popoff', self.setup['optional']) == True:
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
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await interaction.response.send_message(f'You lack the necessary roles to use this command! {danki_enums.DiscordOut.ISSUE_GITHUB}', ephemeral=True)
        except Exception as err:
            await interaction.response.send_message(f'{danki_enums.DiscordOut.ERROR}', ephemeral=True)
            raise err
        
    
    def fileExists(self, filename):
        try:
            with open(filename, 'r') as f:
                return True
        except FileNotFoundError:
            return False
        
    @app_commands.command(name='banter', description='For reminding everyone that what you said was just a joke')
    async def banter(self, interaction: discord.Interaction):
        try:
            if await danki_checks.checkCommandNeedRoles(interaction.user, 'banter', self.setup['optional']) == True:
                tts_channel = discord.utils.get(interaction.guild.text_channels, name=f'{self.botSetup["required"]["tts_channel"]}')
                await tts_channel.send(f'{interaction.guild.get_member(interaction.user.id).display_name} was merely joking and is not liable for any hurt feelings that what they said may have caused. Thank you for your understanding', tts=True, delete_after=20)
                await interaction.response.send_message(f'Disclaimer sent to {self.botSetup["required"]["tts_channel"]}', ephemeral=True)
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await interaction.response.send_message(f'You lack the necessary roles to use this command! {danki_enums.DiscordOut.ISSUE_GITHUB}', ephemeral=True)
        except Exception as err:
            await interaction.response.send_message(f'{danki_enums.DiscordOut.ERROR}', ephemeral=True)
            raise err
        

    @app_commands.command(name='notbanter', description='For reminding everyone that what you said was NOT a joke')
    async def notbanter(self, interaction: discord.Interaction, user_mention: str):
        try:
            if await danki_checks.checkCommandNeedRoles(interaction.user, 'notbanter', self.setup['optional']) == True:
                tts_channel = discord.utils.get(interaction.guild.text_channels, name=f'{self.botSetup["required"]["tts_channel"]}')
                messages = [
                f'{interaction.guild.get_member(interaction.user.id).display_name} meant what they said to {user_mention} from the bottom of their heart',
                f'Did {interaction.guild.get_member(interaction.user.id).display_name} fucking stutter',
                ]
                chosen_message = random.choice(messages)
                await tts_channel.send(chosen_message, tts=True, delete_after=60)        
                await interaction.response.send_message(f'Disclaimer sent to {self.botSetup["required"]["tts_channel"]}', ephemeral=True)
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await interaction.response.send_message(f'You lack the necessary roles to use this command! {danki_enums.DiscordOut.ISSUE_GITHUB}', ephemeral=True)
        except Exception as err:
            await interaction.response.send_message(f'{danki_enums.DiscordOut.ERROR}', ephemeral=True)
            raise err
        




















    #####################################    
    ########## MUSIC FUNCTIONS ##########
    #####################################



    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        ### Continue Playing Check
        # Check if danki in VC
        if discord.utils.get(after.channel.members, name='Danki#2189') != None:
            # Check if danki is alone in VC
            if len(after.channel.members) == 1:
                self.vc.disconnect()
                # reset variables used for music to None since disconnected
                self.vc = None
                self.currSong = None
                self.musicQueue = None
                self.message_music_curr = None
                self.message_music_queue = None
        else:
            ### Horny Check
            role_name = "Horny"
            # Check if the member has the specified role
            role = discord.utils.get(member.roles, name=role_name)
            if role and not before.channel and after.channel:
                if member.id == self.bot.user.id:
                    return
                # Connect to the user's voice channel
                self.vc = await after.channel.connect()
                specific_url = 'https://www.youtube.com/watch?v=2BCgSYNteVo&ab_channel=CHORUSLOOPS'
                # Get the audio stream URL from the YouTube video (you'll need to define 'specific_url' here)
                video = pytube.YouTube(specific_url)
                audio_stream = video.streams.filter(only_audio=True).first()
                url2 = audio_stream.url
                # Play the audio stream
                self.vc.play(discord.FFmpegPCMAudio(url2, executable='ffmpeg',before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",options="-vn"))
                self.stop_audio_task = asyncio.create_task(self.stop_audio_after_duration(5))


    async def stop_audio_after_duration(self, duration):
        await asyncio.sleep(duration)
        if self.vc and self.vc.is_playing():
            self.vc.stop()
            await self.vc.disconnect()

            # reset self.vc to None since disconnected
            self.vc = None

    music = app_commands.Group(name='music', description='For music related commands')
    @music.command(name='play', description='For playing music (type without adding url to resume paused music)')
    async def music_play(self, interaction: discord.Interaction, url: str=None):
        try:
            member = discord.utils.get(interaction.guild.members, id=interaction.user.id)
            # Check if user is in a voice channel
            if await danki_checks.checkUserInVoice(member, '/music play') == True:
                # Check if user didn't specify a url
                if url == None:
                    # Check if danki is in vc
                    if self.vc != None:
                        # Check if a song is paused
                        if self.vc.is_paused():
                            self.vc.resume()
                            await interaction.response.send_message('Music resumed!', ephemeral=True)
                            return
                        else:
                            await interaction.response.send_message('No music paused!', ephemeral=True)
                            return
                    else:
                        await interaction.response.send_message('I\'m not even in vc though, what song do you want me to pause...?', ephemeral=True)
                else:
                    # Check if danki not in vc
                    if self.vc == None:

                        # Connecting Danki to user's voice channel
                        voice_channel = member.voice.channel
                        self.vc = await voice_channel.connect()

                        # TODO: Check if music info channel exists in the server

                        # Send an initial message to music info channel (specified in SETUP.json) regarding the current song playing and queue
                        self.message_music_curr = discord.utils.get(interaction.guild.text_channels, self.setup['required']['music_info_channel']).send(f'#Current Song:')
                        self.message_music_queue = discord.utils.get(interaction.guild.text_channels, self.setup['required']['music_info_channel']).send(f'Queue:')
                    
                    else:
                        # Check if Danki not in the same vc as command user
                        if self.vc.channel.id != interaction.user.voice.channel.id:
                            await interaction.response.send_message('Join the same voice channel as me first!')
                            return

                    # Check if a song is currently playing
                    if self.vc.is_playing():
                        self.musicQueue.append(url)
                        await interaction.response.send_message('Music already playing! Adding your song to the queue', ephemeral=True)
                        await self.music_update_queue()
                        return

                    # Check if no queue
                    if len(self.musicQueue) == 0:
                        # Get audio stream URL from youtube vid
                        video = pytube.YouTube(url)
                        audio_stream = video.streams.filter(only_audio=True).first()
                        audio_url = audio_stream.url

                        # Play audio stream
                        self.vc.play(discord.FFmpegPCMAudio(audio_url, executable='ffmpeg', before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", options="-vn"), after=self.afterSong)

                        # Set curr song var
                        self.message_music_curr = url

                        # Output for playing song
                        await interaction.response.send_message('Music playing now, enjoy!', ephemeral=True)

                    # # if there is a queue
                    # else:
                    #     await interaction.response.send_message(f'There\'s currently [{len(self.musicQueue)}] songs in queue! Your song has been added to the queue!')
                    #     self.musicQueue.append(url)
        except Exception as err:
            raise err

    # function for updating current song message
    async def music_update_curr(self):
        msg = f'#Current Song: {self.currSong}'
        self.message_music_curr.edit(msg)

    # function for updating queue message
    async def music_update_queue(self):
        msg = 'Queue:\n'
        for i in range(len(self.musicQueue)):
            msg += f'{i + 1}. {self.musicQueue}\n'
        self.message_music_queue.edit(msg)

    # Recursive function for going through queue
    def afterSong(self, error):
        try:    
            if len(self.musicQueue) > 0:
                url = self.musicQueue[0]

                # update current music
                self.message_music_curr = url
                self.music_update_curr()

                # play new song
                video = pytube.YouTube(url)
                audio_stream = video.streams.filter(only_audio=True).first()
                audio_url = audio_stream.url
                self.vc.play(discord.FFmpegPCMAudio(audio_url, executable='ffmpeg', before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", options="-vn"), after=self.afterSong)

                # update queue
                self.musicQueue.pop(0)
                self.music_update_queue()
            else:
                print('Queue Finished!')
            print(error)
        except Exception as err:
            raise err
        
    @music.command(name='pause', description='For pausing the currently playing song')
    async def music_pause(self, interaction: discord.Interaction):
        # Check if Danki is connected to a vc
        if self.vc != None:
            # Check if Danki is already playing a song
            if self.vc.is_playing():
                self.vc.pause()
                await interaction.response.send_message('Music has been paused!', ephemeral=True)
                return
            # Check if there is already a paused song
            if self.vc.is_paused():
                await interaction.response.send_message('Music already paused! Type /music play instead!', ephemeral=True)
                return
        await interaction.response.send_message('There is no music playing!', ephemeral=True)

    @music.command(name='disconnect', description='For disconnecting Danki from the voice channel')
    async def music_disc(self, interaction: discord.Interaction):
        # Check if Danki is connected to a vc
        if self.vc != None:
            self.vc.stop()
            await self.vc.disconnect()
            await interaction.response.send_message('Thank you for listening!', ephemeral=True)
            # Reset music variables as disconnected
            self.vc = None
            self.currSong = None
            self.musicQueue = None
            self.message_music_curr = None
            self.message_music_queue = None
            return
        else:
            await interaction.response.send_message('I\'m not even there lmao bruh', ephemeral=True)

    @music.command(name='queue', description='For getting the current queue')
    async def music_queue(self, interaction: discord.Interaction):
        # Check if Danki is connected to a vc
        if self.vc != None:
            # Check if queue is empty
            if len(self.musicQueue) == 0:
                await interaction.response.send_message('Queue is empty!', ephemeral=True)
            else:
                queueMsg = 'Current Queue\n'
                for i in range(len(self.musicQueue)):
                    queueMsg += f'{i + 1}. {self.musicQueue[i]}\n'
                await interaction.response.send_message(queueMsg, ephemeral=True)
        else:
            await interaction.response.send_message('I\'m not even there? What queue are you talking about?', ephemeral=True)

    @music.command(name='skip', description='For skipping songs')
    async def music_skip(self, interaction: discord.Interaction):
        # Check if Danki is connected to a vc
        if self.vc != None:
            # Check if music playing
            if self.vc.is_playing():
                # Check if queue is empty
                if len(self.musicQueue) == 0:
                    self.vc.stop()
                    await interaction.response.send_message('No more songs in queue! Stopping instead...', ephemeral=True)
                else:
                    self.vc.stop()
                    url = self.musicQueue[0]
                    video = pytube.YouTube(url)
                    audio_stream = video.streams.filter(only_audio=True).first()
                    audio_url = audio_stream.url
                    self.vc.play(discord.FFmpegPCMAudio(audio_url, executable='ffmpeg', before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", options="-vn"), after=self.afterSong)
                    self.musicQueue.pop(0)
                    await interaction.response.send_message('Song skipped! Sorry whoever added it!')
        else:
            await interaction.response.send_message('bruh.', ephemeral=True)

    
    # @commands.command(name="play", description="For playing music", usage="!play [Youtube URL]")
    # async def play(self, ctx, url):
    #     # Check if the user is in a voice channel
    #     if ctx.author.voice is None:
    #         await ctx.send("You're not in a voice channel.")
    #         return

    #     # Check if the bot is already in a voice channel
    #     if ctx.voice_client is not None:
    #         await ctx.send("I'm already in a voice channel. Use !disconnect or !stop to stop the current audio.")
    #         return

        # # Connect to the user's voice channel
        # voice_channel = ctx.author.voice.channel
        # vc = await voice_channel.connect()

        # # Get the audio stream URL from the YouTube video
        # video = pytube.YouTube(url)
        # audio_stream = video.streams.filter(only_audio=True).first()
        # audio_url = audio_stream.url

        # # Play the audio stream
        # vc.play(discord.FFmpegPCMAudio(audio_url, executable='ffmpeg',before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",options="-vn"))

        # # Wait for the audio to finish playing
        # while vc.is_playing():
        #     await asyncio.sleep(1)

        # # Disconnect after the audio is finished
        # await vc.disconnect()

    # @commands.command(name="stop", description="For playing music", usage="!stop")
    # async def stop(self, ctx):
    #     # Check if the bot is in a voice channel and is currently playing audio
    #     if ctx.voice_client is not None and ctx.voice_client.is_playing():
    #         ctx.voice_client.stop()

    # @commands.command(name="disconnect", description="For playing music", usage="!disconnect")
    # async def disconnect(self, ctx):
    #     # Check if the bot is in a voice channel
    #     if ctx.voice_client is not None:
    #         await ctx.voice_client.disconnect()
    #     else:
    #         await ctx.send("I'm not in a voice channel.")

    
    
    ############################################
    ########## END OF MUSIC FUNCTIONS ##########
    ############################################
    
    
    
    











    
    
    
    
    
    #######################################
    ########## SELAMAT FUNCTIONS ##########
    #######################################

    selamatGrp = app_commands.Group(name='selamat', description='For commands related to greeting others in the server')

    @selamatGrp.command(name='pagi', description="For greeting a fellow member in the morning")
    @app_commands.checks.has_any_role('Lvl 100 Mafia Warlord', 'Lvl 10 Boss')
    async def pagi(self, interaction: discord.Interaction, user_mention: str):
        try:
            if await danki_checks.checkCommandNeedRoles(interaction.user, 'pagi', self.setup['optional']) == True:
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
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await interaction.response.send_message(f'You lack the necessary roles to use this command! {danki_enums.DiscordOut.ISSUE_GITHUB}', ephemeral=True)
        except Exception as err:
            await interaction.response.send_message(f'{danki_enums.DiscordOut.ERROR}', ephemeral=True)
            raise err
        

    @selamatGrp.command(name='petang', description="For greeting a fellow member in the afternoon")
    @app_commands.checks.has_any_role('Lvl 100 Mafia Warlord', 'Lvl 10 Boss')
    async def petang(self, interaction: discord.Interaction, user_mention: str):
        try:
            if await danki_checks.checkCommandNeedRoles(interaction.user, 'petang', self.setup['optional']) == True:
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
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await interaction.response.send_message(f'You lack the necessary roles to use this command! {danki_enums.DiscordOut.ISSUE_GITHUB}', ephemeral=True)
        except Exception as err:
            await interaction.response.send_message(f'{danki_enums.DiscordOut.ERROR}', ephemeral=True)
            raise err
        

    @selamatGrp.command(name='malam', description="For greeting a fellow member in the evening")
    @app_commands.checks.has_any_role('Lvl 100 Mafia Warlord', 'Lvl 10 Boss')
    async def malam(self, interaction: discord.Interaction, user_mention: str):
        try:
            if await danki_checks.checkCommandNeedRoles(interaction.user, 'malam', self.setup['optional']) == True:
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
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await interaction.response.send_message(f'You lack the necessary roles to use this command! {danki_enums.DiscordOut.ISSUE_GITHUB}', ephemeral=True)
        except Exception as err:
            await interaction.response.send_message(f'{danki_enums.DiscordOut.ERROR}', ephemeral=True)
            raise err
        
                

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
        try:
            if await danki_checks.checkCommandNeedRoles(interaction.user, 'quote', self.setup['optional']) == True:
                chosen_quote = "@@@@@"
                
                if os.path.exists("quote_file.json") and os.path.getsize("quote_file.json") > 0:
                    ## Open .json file
                    with open("quote_file.json") as read_file:
                        quote_data = json.load(read_file)
                        rand_index = str(random.randint(1, len(quote_data)))

                    ## Retrieve random .json entry
                    chosen_quote = quote_data[rand_index]["quote"]
                    quoted_by = quote_data[rand_index]["addedBy"]
                    quoted_on = quote_data[rand_index]["addedOn"]


                    # ## Send random quote to user
                    await interaction.response.send_message(f"### Your Quote: `{chosen_quote}`\n### - {quoted_by} {quoted_on}")

                else:
                    return await interaction.response.send_message(":x: **No quotes exist yet!** :x:", ephemeral=True)
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await interaction.response.send_message(f'You lack the necessary roles to use this command! {danki_enums.DiscordOut.ISSUE_GITHUB}', ephemeral=True)
        except Exception as err:
            await interaction.response.send_message(f'{danki_enums.DiscordOut.ERROR}', ephemeral=True)
            raise err
        

    @quoteGrp.command(name='make', description="For making a new quote for the server")
    @app_commands.checks.has_any_role('Coders')
    @app_commands.describe(added_quote = "What quote are you adding?")
    async def makequote(self, interaction:discord.Interaction, added_quote:str):

        try:
            if await danki_checks.checkCommandNeedRoles(interaction.user, 'makequote', self.setup['optional']) == True:
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
        except danki_exceptions.MemberMissingRole as err:
            print(f'\n{err}\n')
            await interaction.response.send_message(f'You lack the necessary roles to use this command! {danki_enums.DiscordOut.ISSUE_GITHUB}', ephemeral=True)
        except Exception as err:
            await interaction.response.send_message(f'{danki_enums.DiscordOut.ERROR}', ephemeral=True)
            raise err

    ########################################################################
    ########## QUOTE END ###################################################
    ########################################################################



















    ##################################
    ########## Error Handling ########
    ##################################
    # async def cog_app_command_error(self, interaction: discord.Interaction, error):
    #     print(str(error))
    #     if isinstance(error, app_commands.MissingAnyRole):
    #         missing = []
    #         user = interaction.guild.get_member(interaction.user.id)
    #         for role in error.missing_roles:
    #             print(role)
    #             if discord.utils.get(user.roles, name=role) == None:
    #                 missing.append(role)
    #         await interaction.response.send_message(f'You do not have the necessary roles to use /{interaction.command.qualified_name}! Here is the list of required roles:\n{missing}')
    #     else:
    #         await interaction.response.send_message(f'/{interaction.command.qualified_name} is broken! Please contact the admin about this issue!', ephemeral=True)


    # TODO: /bet function for placing{all}, making{all}, removing{owner of bet/restricted}, unbetting{all} and changing bet{all} could be used in conjunction with poll commands; bets are monetised polls
    # TODO: /dbucks function for getting amount{all} giving{restricted} and using{all} of dbucks






async def setup(bot: commands.Bot):
    
    await bot.add_cog(Misc(bot))
import json
import os
import discord

import danki_exceptions
import danki_enums


'''
for SETUP.json,
str are used to hold channel names
list are used to hold roles

'''

async def checkHasRoles(member: discord.Member, command: str, optionList: dict):
    memberRoles = member.roles
    serverRolesList = member.guild.roles
    for role in optionList[command+'_required_roles']:
        role = discord.utils.get(serverRolesList, name=role)
        if role not in memberRoles:
            raise danki_exceptions.MemberMissingRole(member, command, role)
    return True

async def checkRequired():
    with open('SETUP.json', 'r') as f:
        setup = json.loads(f.read())
        for module in setup.keys():
            moduleSetup = setup[module]
            for e in moduleSetup['required'].keys():
                if type(moduleSetup['required'][e]) == str:
                    if moduleSetup['required'][e] == '---NONE---':
                        raise danki_exceptions.MissingValueInSetup(module, e)
                elif type(moduleSetup['required'][e]) == list:
                    if len(moduleSetup['required'][e]) == 1:
                        if moduleSetup['required'][e][0] == '---NONE---':
                            raise danki_exceptions.MissingValueInSetup(module, e)
                    if '---NONE---' in moduleSetup['required'][e]:
                        raise danki_exceptions.DefaultValueNotRemoved(module, 'required', e)
    return True

async def checkOptional():
    with open('SETUP.json', 'r') as f:
        setup = json.loads(f.read())
        for module in setup.keys():
            moduleSetup = setup[module]
            for e in moduleSetup['optional'].keys():
                if type(moduleSetup['optional'][e]) == list and len(moduleSetup['optional'][e]) > 1:
                    if '---NONE---' in moduleSetup['optional'][e]:
                        raise danki_exceptions.DefaultValueNotRemoved(module, 'optional', e)
    return True

async def checkSetup():
    if await checkRequired() and await checkOptional():
        with open('SETUP.json', 'r') as f:
            setup = json.loads(f.read())
            return setup
    
async def checkServerHasRequiredRoles(guild):
    with open('SETUP.json', 'r') as f:
        setup = json.loads(f.read())
        for module in setup.keys():
            if len(setup[module]['required']) > 0:
                req = setup[module]['required']
                for option in req.keys():
                    if type(req[option]) == str:
                        if discord.utils.get(guild.text_channels, name=req[option]) == None:
                            raise danki_exceptions.ChannelDoesNotExist(option, req[option])
                    elif type(req[option]) == list:
                        for role in req[option]:
                            if discord.utils.get(guild.roles, name=role) == None:
                                raise danki_exceptions.RoleDoesNotExist(option, role)
    return True

async def checkServerHasOptionalRoles(guild):
    with open('SETUP.json', 'r') as f:
        setup = json.loads(f.read())
        for module in setup.keys():
            if len(setup[module]['optional']) > 0:
                opt = setup[module]['optional']
                for option in opt.keys():
                    if type[opt[option]] == str:
                        if opt[option] != '---NONE---' and discord.utils.get(guild.text_channels, name=opt[option]) == None:
                            raise danki_exceptions.ChannelDoesNotExist(option, opt[option])
                    elif type[opt[option]] == list:
                        if len(opt[option]) >= 1 and '---NONE--' not in opt[option]:
                            for role in opt[option]:
                                if discord.utils.get(guild.roles, name=role) == None:
                                    raise danki_exceptions.RoleDoesNotExist(option, role)
    return True

async def checkServerHasRoles(guild):
    if await checkServerHasRequiredRoles(guild) and await checkServerHasRequiredRoles(guild):
        return True
    
async def checkCommandNeedRoles(member: discord.Member, command: str, optionList: dict):
    if len(optionList[command+danki_enums.Setup.ROLES_END]) == 1 and '---NONE---' in optionList[command+danki_enums.Setup.ROLES_END]:
        return True
    else:
        await checkHasRoles(member, command, optionList)

async def checkDirectoriesExist(pathList: list[str]):
    for path in pathList:
        if os.path.exists(path) == False:
            raise danki_exceptions.DirectoryMissing(path)
    return True

async def checkFileExists(filepath):
    try:
        with open(filepath, 'r') as f:
            return True
    except FileNotFoundError:
        raise danki_exceptions.FileMissing(filepath)
    
async def checkUserInVoice(member: discord.Member, command: str):
    if member.voice.channel == None:
        raise danki_exceptions.UserNotInVoiceChannel(member, command)
    return True
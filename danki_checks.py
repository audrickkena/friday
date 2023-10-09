import json
import danki_exceptions
import discord

def check_has_role():
    pass

def checkRequired(moduleName):
    with open('SETUP.json', 'r') as f:
        moduleSetup = json.loads(f.read())[moduleName]
        for e in moduleSetup['required'].keys():
            if type(moduleSetup['required'][e]) == str:
                if moduleSetup['required'][e] == '---NONE---':
                    raise danki_exceptions.MissingValueInSetup(e)
            elif type(moduleSetup['required'][e]) == list:
                if len(moduleSetup['required'][e]) == 1:
                    if moduleSetup['required'][e][0] == '---NONE---':
                        raise danki_exceptions.MissingValueInSetup(e)
                if '---NONE---' in moduleSetup['required'][e]:
                    raise danki_exceptions.DefaultValueNotRemoved(e)
        return moduleSetup
    
def checkServerHasRequiredRoles(guild):
    with open('SETUP.json', 'r') as f:
        setup = json.loads(f.read())
        for module in setup.keys():
            req = setup[module]['required']
            for option in req.keys():
                if type(req[option]) == str:
                    if discord.utils.get(guild.roles, name=req[option]) == None:
                        raise danki_exceptions.RoleDoesNotExist(option, req[option])
                elif type(req[option]) == list:
                    for role in req[option]:
                        if discord.utils.get(guild.roles, name=role) == None:
                            raise danki_exceptions.RoleDoesNotExist(option, role)
        return True    
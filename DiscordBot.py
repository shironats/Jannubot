import discord
from discord.ext import commands, tasks
import io
import aiohttp
import datetime
import random

bot = commands.Bot(command_prefix='}')
bot.remove_command('help')
imageCounter = 5
#target_channel = ID here #botfest
#target_channel = ID here #general
#target_channel = ID here #bot_test
#raid_channel = ID here #raids
#danchou = '<@&ID here>'
#officers = '<@&ID here>'
#haipa = '<@!ID here>'
#victim = :kmr:

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name='}help'))

@bot.command(pass_context = True)
async def help(ctx):
    embed = discord.Embed(colour = discord.Colour.orange())
    embed.set_author(name='Help')
    embed.add_field(name='}down', value='Sends a random "Buff is down" image', inline=False)
    embed.add_field(name='}up', value='Sets timer for next buff reactivation', inline=False)
    embed.add_field(name='}checkImages', value='Check }down images', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def down(ctx):
    """Sends a random 'Buff is down' image"""
    downReminder.cancel()
    ITSDOWN.cancel()
    link = mySwitch(random.randint(0,imageCounter-1))
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            if link[27:] == ".jpg":
                await ctx.send(file=discord.File(data, 'BUFFDOWN.jpg'))
            elif link[27:] == ".png":
                await ctx.send(file=discord.File(data, 'BUFFDOWN.png'))
            elif link[27:] == ".gif":
                await ctx.send(file=discord.File(data, 'BUFFDOWN.gif'))
            else:
                await ctx.send("ERROR")

@bot.command()
async def up(ctx):
    """Sets timer for next buff reactivation"""
    await ctx.send('Buff has been reactivated on {0}'.format(datetime.datetime.now()))
    downReminder.start()

@bot.command()
async def checkImages(ctx):
    """Check }down images"""
    for iCounter in range(imageCounter):
        link = mySwitch(iCounter)
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                if link[27:] == ".jpg":
                    await ctx.send(file=discord.File(data, 'BUFFDOWN.jpg'))
                elif link[27:] == ".png":
                    await ctx.send(file=discord.File(data, 'BUFFDOWN.png'))
                elif link[27:] == ".gif":
                    await ctx.send(file=discord.File(data, 'BUFFDOWN.gif'))
                else:
                    await ctx.send("ERROR")

#@tasks.loop(minutes=58, hours=71)
@tasks.loop(seconds=2)
async def downReminder():
    message_channel = bot.get_channel(target_channel)
    if downReminder.current_loop == 0:
        await message_channel.send('Reminder has been set for {0}'.format(datetime.datetime.now()+datetime.timedelta(hours = 71, minutes = 58)))
    elif downReminder.current_loop == 1:
        await message_channel.send('Buffs will go down in 2 minutes.')
        ITSDOWN.start()
    else:
        await message_channel.send('ERROR!! downReminder not yet terminated!!')

#@tasks.loop(minutes=2)
@tasks.loop(seconds=2)
async def ITSDOWN():
    message_channel = bot.get_channel(target_channel)
    if ITSDOWN.current_loop == 0:
        downReminder.cancel()
    else:
        link = mySwitch(random.randint(0,imageCounter-1))
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                if resp.status != 200:
                    return await ctx.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                if link[27:] == ".jpg":
                    await message_channel.send('%s, Please type in (or maybe spam) "}up" to continue...' %victim, file=discord.File(data, 'BUFFDOWN.jpg'))
                elif link[27:] == ".png":
                    await message_channel.send('%s, Please type in (or maybe spam) "}up" to continue...' %victim, file=discord.File(data, 'BUFFDOWN.png'))
                elif link[27:] == ".gif":
                    await message_channel.send('%s, Please type in (or maybe spam) "}up" to continue...' %victim, file=discord.File(data, 'BUFFDOWN.gif'))
                else:
                    await ctx.send("ERROR")
        
def mySwitch(argument):
    switcher = {
        0: 'https://i.imgur.com/Ns9DV9R.jpg',
        1: 'https://i.imgur.com/EGDsKdv.png',
        2: 'https://i.imgur.com/SDRmkhD.jpg',
        3: 'https://i.imgur.com/uJp4D7C.jpg',
        4: 'https://i.imgur.com/agYqbci.jpg'
        }
    return switcher.get(argument, "Invalid pick")

def stopAllTimers():
    downReminder.cancel()
    ITSDOWN.cancel()

bot.run('token here')

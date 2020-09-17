import discord
from discord.ext import commands, tasks
import io
import aiohttp
import random

bot = commands.Bot(command_prefix='}')
bot.remove_command('help')
downImageCounter = 6
upImageCounter = 2
botfest = ID Here #botfest
general = ID Here #general
botTest = ID Here #bot_test
vc_channel = ID Here #vc-for-mutes
raid_channel = ID Here #raids
danchou = '<@&ID Here>'
officers = '<@&ID Here>'
haipa = '<@!ID Here>'
self = '<@!ID Here>'
nadekoBOT = ID Here

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name='}help'))

@bot.event
async def on_message(message):
    nadeko = bot.get_user(nadekoBOT)
    if message.author == bot.user:
        return
    elif message.author == nadeko:
        if message.content.startswith('}down'):
            if message.content.endswith('mutes'):
                downSpamBot.start(vc_channel)
            elif message.content.endswith('general'):
                downSpamBot.start(general)
            else:
                downSpamBot.start(botfest)
        else:
            await bot.process_commands(message)

    await bot.process_commands(message)

@bot.command(pass_context = True)
async def help(ctx):
    embed = discord.Embed(colour = discord.Colour.orange())
    embed.set_author(name='Help')
    embed.add_field(name='}down', value='Spams random "Buff is down" images', inline=False)
    embed.add_field(name='}up', value='Sends a random "Buff is up" image', inline=False)
    embed.add_field(name='}checkImages', value='Check all images', inline=False)
    embed.add_field(name='Source Code', value='https://github.com/shironats/Buffbot/blob/Update-14/07/DiscordBot.py', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def down(ctx):
    """Sends a random 'Buff is down' image"""
    downSpam.start(ctx)

@bot.command()
async def downTest(ctx, imgID: int):
    """Function for testing"""
    link = downSwitch(imgID)
    await sendPics(ctx, link, False)

@bot.command()
async def up(ctx):
    """Sets timer for next buff reactivation"""
    downSpam.cancel()
    downSpamBot.cancel()
    link = upSwitch(random.randint(0,upImageCounter-1))
    await sendPics(ctx, link, False)

@bot.command()
async def checkImages(ctx):
    """Check }down images"""
    for iCounter in range(downImageCounter):
        link = downSwitch(iCounter)
        await sendPics(ctx, link, False)
    for iCounter in range(upImageCounter):
        link = upSwitch(iCounter)
        await sendPics(ctx, link, False)

@tasks.loop(seconds=2)
async def downSpam(ctx):
    link = downSwitch(random.randint(0,downImageCounter-1))
    await sendPics(ctx, link, True, downSpam.current_loop)

@tasks.loop(seconds=2)
async def downSpamBot(target_channel):
    link = downSwitch(random.randint(0,downImageCounter-1))
    msgChannel = bot.get_channel(target_channel)
    await sendPics(msgChannel, link, True, downSpamBot.current_loop)

def downSwitch(argument):
    switcher = {
        0: 'https://i.imgur.com/Ns9DV9R.jpg',
        1: 'https://i.imgur.com/EGDsKdv.png',
        2: 'https://i.imgur.com/SDRmkhD.jpg',
        3: 'https://i.imgur.com/uJp4D7C.jpg',
        4: 'https://i.imgur.com/agYqbci.jpg',
        5: 'https://i.imgur.com/H7bos6u.gif'
        }
    return switcher.get(argument, "Invalid pick")

def upSwitch(argument):
    switcher = {
        0: 'https://i.imgur.com/1FaipNk.png',
        1: 'https://i.imgur.com/kEOah4r.jpg'
        }
    return switcher.get(argument, "Invalid pick")

async def sendPics(ctx, imglink, withText, loopNum = 0):
    async with aiohttp.ClientSession() as session:
        async with session.get(imglink) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            if imglink.endswith(".jpg"):
                if withText == True:
                    await ctx.send('%s or %s, Please reactivate crew buffs, this is reminder number %i' %(danchou,officers,loopNum), file=discord.File(data, 'img.jpg'))
                else:
                    await ctx.send(file=discord.File(data, 'img.jpg'))
            elif imglink.endswith(".png"):
                if withText == True:
                    await ctx.send('%s or %s, Please reactivate crew buffs, this is reminder number %i' %(danchou,officers,loopNum), file=discord.File(data, 'img.png'))
                else:
                    await ctx.send(file=discord.File(data, 'img.png'))
            elif imglink.endswith(".gif"):
                if withText == True:
                    await ctx.send('%s or %s, Please reactivate crew buffs, this is reminder number %i' %(danchou,officers,loopNum), file=discord.File(data, 'img.gif'))
                else:
                    await ctx.send(file=discord.File(data, 'img.gif'))
            else:
                await ctx.send("ERROR")

bot.run('ID Here')

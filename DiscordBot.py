import discord
from discord.ext import commands, tasks
import io
import aiohttp
import random

bot = commands.Bot(command_prefix='}')
bot.remove_command('help')
botfest = ID Here #botfest
general = ID Here #general
botTest = ID Here #bot_test
vc_channel = ID Here #vc-for-mutes
raid_channel = ID Here #raids
danchou = '<@&ID Here>'
officers = '<@&ID Here>'
haipa = '<@!ID Here>'
self = '<@!ID Here>'
sol = '<@!ID Here>'
nadekoBOT = ID Here

#============== BOT EVENTS ================================
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

#send screaming cat image
    if message.content.lower().endswith('aaaaa'):
        await sendSinglePic(message.channel, 'https://i.imgur.com/8n1zvzR.jpg')

    await bot.process_commands(message)

#============== BOT COMMANDS ==============================
@bot.command(pass_context = True)
async def help(ctx):
    embed = discord.Embed(colour = discord.Colour.orange())
    embed.set_author(name='Help')
    embed.add_field(name='}down', value='Spams random "Buff is down" images', inline=False)
    embed.add_field(name='}up', value='Sends a random "Buff is up" image', inline=False)
    embed.add_field(name='}checkImages', value='Check all images', inline=False)
    embed.add_field(name='}truck [@ someone]', value='Sends a truck after that person', inline=False)
    embed.add_field(name='Other Features', value='Send 5 "a"s', inline=False)
    embed.add_field(name='Source Code', value='https://github.com/shironats/Buffbot/blob/Update-16/07/DiscordBot.py', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def down(ctx):
    """Sends a random 'Buff is down' image"""
    downSpam.start(ctx)

@bot.command()
async def downTest(ctx, imgID: int):
    """Function for testing"""
    link = downImages[imgID]
    await sendSinglePic(ctx, link)

@bot.command()
async def up(ctx):
    """Sets timer for next buff reactivation"""
    downSpam.cancel()
    downSpamBot.cancel()
    link = upImages[random.randint(0,len(upImages)-1)]
    await sendPics(ctx, link, False)

@bot.command()
async def checkImages(ctx):
    """Check }down images"""
    for iCounter in range(len(downImages)):
        link = downImages[iCounter]
        await sendSinglePic(ctx, link)
    for iCounter in range(len(upImages)):
        link = upImages[iCounter]
        await sendSinglePic(ctx, link)
    for iCounter in range(len(truckImages)):
        link = truckImages[iCounter]
        await sendSinglePic(ctx, link)
    for iCounter in range(len(bonkImages)):
        link = bonkImages[iCounter]
        await sendSinglePic(ctx, link)

@bot.command()
async def truck(ctx, member: discord.Member):
    """Sends a truck over"""
    link = truckImages[random.randint(0,len(truckImages)-1)]
    embed = discord.Embed(colour = discord.Colour.red())
    embed.set_footer(text='{0.nick}, {1.nick} sends their regards.'.format(member, ctx.message.author))
    embed.set_image(url='attachment://img%s' %(link[27:]))
    await sendSinglePic(ctx, link, embed)

@bot.command()
async def bonk(ctx, member: discord.Member):
    """Bonks a member"""
    link = bonkImages[random.randint(0,len(bonkImages))]
    embed = discord.Embed(colour = discord.Colour.blurple())
    embed.set_footer(text='{0.nick} has been BONKED by {1.nick} for being bad.'.format(member, ctx.message.author))
    embed.set_image(url='attachment://img%s' %(link[27:]))
    await sendSinglePic(ctx, link, embed)

#============== BOT LOOPS =============================
@tasks.loop(seconds=2)
async def downSpam(ctx):
    link = downSwitch(random.randint(0,downImageCounter-1))
    await sendPics(ctx, link, True, downSpam.current_loop)

@tasks.loop(seconds=2)
async def downSpamBot(target_channel):
    link = downSwitch(random.randint(0,downImageCounter-1))
    msgChannel = bot.get_channel(target_channel)
    await sendPics(msgChannel, link, True, downSpamBot.current_loop)

#============== IMAGES ============================
downImages = ['https://i.imgur.com/Ns9DV9R.jpg',
              'https://i.imgur.com/EGDsKdv.png',
              'https://i.imgur.com/SDRmkhD.jpg',
              'https://i.imgur.com/uJp4D7C.jpg',
              'https://i.imgur.com/agYqbci.jpg',
              'https://i.imgur.com/H7bos6u.gif']

upImages = ['https://i.imgur.com/1FaipNk.png',
            'https://i.imgur.com/kEOah4r.jpg']

truckImages = ['https://i.imgur.com/qYhwU3x.gif',
               'https://i.imgur.com/PWEibqW.gif']

bonkImages = ['https://i.imgur.com/3e1P8oW.gif',
              'https://i.imgur.com/fIWm3Hh.gif',
              'https://i.imgur.com/fmZY9dV.gif']

#============== ASYNC FUNCTIONS =======================
async def sendPics(ctx, imglink, withText, loopNum = 0):
    async with aiohttp.ClientSession() as session:
        async with session.get(imglink) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            if withText == True:
                await ctx.send('%s or %s, Please reactivate crew buffs, this is reminder number %i' %(danchou,officers,loopNum), file=discord.File(data, 'img%s'%(imglink[27:])))
            else:
                await ctx.send(file=discord.File(data, 'img%s'%(imglink[27:])))

async def sendSinglePic(ctx, imglink, embed = None):
    async with aiohttp.ClientSession() as session:
        async with session.get(imglink) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, 'img%s'%(imglink[27:])), embed = embed)

bot.run('ID Here')

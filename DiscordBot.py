import discord
from discord.ext import commands, tasks
import os
import io
import aiohttp
import random

bot = commands.Bot(command_prefix='}')
bot.remove_command('help')
botfest = blahblahblah #botfest
general = blahblahblah #general
danchou = '<@&blahblahblah>'
officers = '<@&blahblahblah>'
haipa = blahblahblah
self = blahblahblah
sol = blahblahblah
nadekoBOT = blahblahblah
jannuBOT = blahblahblah

#============== BOT EVENTS ================================
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name='}help'))
    getBirthdays()

@bot.event
async def on_message(message):
    nadeko = bot.get_user(nadekoBOT)
    if message.author == bot.user:
        return
    elif message.author == nadeko:
        if message.content.startswith('}down'):
            if message.content.endswith('general'):
                downSpamBot.start(general)
            else:
                downSpamBot.start(botfest)

#send Screaming cat image
    if message.content.lower().endswith('aaaaa'):
        await sendSinglePic(message.channel, 'https://i.imgur.com/8n1zvzR.jpg')

#send Jangkrik
    if message.content.lower().find('cricket cricket') != -1:
        await sendSinglePic(message.channel, 'https://i.imgur.com/ors2jnC.gif')

#send RAID: SHADOW LEGENDS
    if message.content.lower().find('ra') != -1:
        if message.content.lower().find('aai') > message.content.lower().find('ra'):
            if message.content.lower().find('id') > message.content.lower().find('aai'):
                await sendSinglePic(message.channel, 'https://i.imgur.com/eywxw5g.gif')

#send Solaire
    if message.content.lower().find('praise the sun') != -1:
        await sendSinglePic(message.channel, 'https://i.imgur.com/MYhwSHm.gif')
    
    await bot.process_commands(message)

#============== BOT COMMANDS ==============================
@bot.command(pass_context = True)
async def help(ctx):
    embed = discord.Embed(colour = discord.Colour.teal())
    embed.set_author(name='Help')
    embed.add_field(name='}down', value='Spams random "Buff is down" images', inline=False)
    embed.add_field(name='}up', value='Sends a random "Buff is up" image', inline=False)
    embed.add_field(name='}checkImages', value='Check all images', inline=False)
    embed.add_field(name='}truck [@ someone]', value='Sends a truck after that person', inline=False)
    embed.add_field(name='}bonk [@ someone]', value='Bonks that person', inline=False)
    embed.add_field(name='}riot', value='Time to RIOT!!', inline=False)
    embed.add_field(name='Other Features', value='Send 5 "a"s\nSend "cricket cricket"\nSend "raaid"', inline=False)
    embed.add_field(name='Source Code', value='https://github.com/shironats/Buffbot/blob/Update-26/08/DiscordBot.py', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def down(ctx):
    """Sends a random 'Buff is down' image"""
    downSpam.start(ctx)

@bot.command()
async def test(ctx, func: str, imgID: int):
    """Function for testing"""
    if (func == 'down'):
        link = downImages[imgID]
    elif (func == 'up'):
        link = upImages[imgID]
    elif (func == 'truck'):
        link = truckImages[imgID]
    else:
        link = bonkImages[imgID]
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
async def isekai(ctx, member: discord.Member):
    """Same as }truck"""
    await truck(ctx, member)
 
@bot.command()
async def truck(ctx, member: discord.Member):
    """Sends a truck over"""
    link = truckImages[random.randint(0,len(truckImages)-1)]
    embed = discord.Embed(colour = discord.Colour.teal())
    embed.set_footer(text='{0.display_name}, {1.display_name} sends their regards.'.format(member, ctx.message.author))
    embed.set_image(url='attachment://img%s' %(link[27:]))
    await sendSinglePic(ctx, link, embed)

@bot.command()
async def bonk(ctx, member: discord.Member):
    """Bonks a member"""
    link = bonkImages[random.randint(0,len(bonkImages)-1)]
    embed = discord.Embed(colour = discord.Colour.teal())
    if (member == bot.get_user(self)):
        embed.set_footer(text='{0.display_name} has been BONKED by {1.display_name} for being bad.'.format(ctx.message.author, member))
    else:
        embed.set_footer(text='{0.display_name} has been BONKED by {1.display_name} for being bad.'.format(member, ctx.message.author))
    embed.set_image(url='attachment://img%s' %(link[27:]))
    await sendSinglePic(ctx, link, embed)

@bot.command()
async def riot(ctx):
    """Time to RIOT!!"""
    await sendSinglePic(ctx, 'https://i.imgur.com/fyG8NZk.png')

@bot.command()
async def bday(ctx):
    """Birthdays"""
    embed = discord.Embed(colour = discord.Colour.teal())
    embed.set_author(name='BIRTHDAYS, PEOPLE, BIRTHDAYS')
    for iCounter in range(len(months)):
        embed.add_field(name=months[iCounter], value=birthdays[months[iCounter]])
    await ctx.send(embed=embed)

#============== BOT LOOPS =============================
@tasks.loop(seconds=2)
async def downSpam(ctx):
    link = downImages[random.randint(0,len(downImages)-1)]
    await sendPics(ctx, link, True, downSpam.current_loop)

@tasks.loop(seconds=2)
async def downSpamBot(target_channel):
    link = downImages[random.randint(0,len(downImages)-1)]
    msgChannel = bot.get_channel(target_channel)
    await sendPics(msgChannel, link, True, downSpamBot.current_loop)

#============== IMAGES ============================
downImages = ['https://i.imgur.com/q4H83FZ.jpg',
              'https://i.imgur.com/h2V3SaO.jpg',
              'https://i.imgur.com/SDRmkhD.jpg',
              'https://i.imgur.com/uJp4D7C.jpg',
              'https://i.imgur.com/agYqbci.jpg',
              'https://i.imgur.com/g5WXEY7.gif',
              'https://i.imgur.com/Jo6Rvsi.jpg']

upImages = ['https://i.imgur.com/ueO6Lrn.jpg',
            'https://i.imgur.com/mVF83k7.jpg']

truckImages = ['https://i.imgur.com/XMG3BXZ.gif',
               'https://i.imgur.com/xYM56uZ.gif',
               'https://i.imgur.com/oRMKp3k.gif']

bonkImages = ['https://i.imgur.com/h2di9EZ.gif',
              'https://i.imgur.com/yXhqh1d.gif',
              'https://i.imgur.com/fmZY9dV.gif',
              'https://i.imgur.com/VkYz0vr.gif',
              'https://i.imgur.com/ngj9zmN.jpg',
              'https://i.imgur.com/EZ56Cbz.jpg',
              'https://i.imgur.com/HQFCiLI.jpg']

months = ['January','February','March','April','May','June',
          'July','August','September','October','November','December']

birthdays = {months[0]:'None (yet)',
             months[1]:'None (yet)',
             months[2]:'None (yet)',
             months[3]:'None (yet)',
             months[4]:'None (yet)',
             months[5]:'None (yet)',
             months[6]:'None (yet)',
             months[7]:'None (yet)',
             months[8]:'None (yet)',
             months[9]:'None (yet)',
             months[10]:'None (yet)',
             months[11]:'None (yet)'}

#============== FUNCTIONS==============================
def getBirthdays():
    newLine = "\n"
    currentMonth = ""
    textfile = open(os.getcwd()+"/DiscordBot_source/JannupalsBirthdays.txt")
    for line in textfile:
        line = line.rstrip(newLine)
        if line in months:
            currentMonth = line
        else:
            if birthdays[currentMonth] == 'None (yet)':
                birthdays[currentMonth] = line
            else:
                myString = birthdays[currentMonth]
                myString = myString+newLine+line
                birthdays[currentMonth] = myString
    textfile.close()

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

bot.run('blahblahblah')

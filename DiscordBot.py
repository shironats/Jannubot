import discord
from discord.ext import commands, tasks
import os
import io
import aiohttp
import random
from pathlib import Path

bot = commands.Bot(command_prefix='}')
bot.remove_command('help')

#============== SENSITIVE NUMBERS ==============
miscID = {"jannupals"   : IDHere, #server
          "botfest"     : IDHere, #channel
          "general"     : IDHere} #channel

roles = {"danchou"      : '<@&IDHere>',
         "officers"     : '<@&IDHere>',
         "twinele"      : '<@&IDHere>',
         "europa"       : '<@&IDHere>'}

userID = {"haipa"       : IDHere,
          "self"        : IDHere,
          "sol"         : IDHere,
          "nadekoBOT"   : IDHere,
          "jannuBOT"    : IDHere,
          "europaBOT"   : IDHere,
          "zeo"         : IDHere,
          "mango"       : IDHere,
          "nana"        : IDHere,
          "bunny"       : IDHere,
          "wayne"       : IDHere,
          "yonji"       : IDHere,
          "joe"         : IDHere,
          "chinpo"      : IDHere}

nukeCode = {"user"      : userID,
            "role"      : roles,
            "misc"      : miscID}

#============== IMAGES & GLOBAL VARIABLE =========
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
               'https://i.imgur.com/oRMKp3k.gif',
               'https://i.imgur.com/9BJEJkS.gif']

bonkImages = ['https://i.imgur.com/h2di9EZ.gif',
              'https://i.imgur.com/yXhqh1d.gif',
              'https://i.imgur.com/fmZY9dV.gif',
              'https://i.imgur.com/VkYz0vr.gif',
              'https://i.imgur.com/ngj9zmN.jpg',
              'https://i.imgur.com/EZ56Cbz.jpg',
              'https://i.imgur.com/HQFCiLI.jpg',
              'https://i.imgur.com/TELpsTl.jpg',
              'https://i.imgur.com/SA4uMHJ.jpg']

months = ['January','February','March','April','May','June','July',
          'August','September','October','November','December']

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

data_folder = Path("DiscordBot_source/")
newLine = "\n"

#============== BOT EVENTS ================================
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name='}help'))
    getBirthdays()

@bot.event
async def on_message(message):
    nadeko = bot.get_user(nukeCode["user"]["nadekoBOT"])

    if message.author == bot.user:
        return
    elif message.author == nadeko:
        if message.content.startswith('}down'):
            if message.content.endswith('general'):
                downSpamBot.start(nukeCode["misc"]["general"])
            else:
                downSpamBot.start(nukeCode["misc"]["botfest"])

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

#counters Uwaaru
    if message.content.find('<:uwaaru:755820728175034489>') != -1:
        await sendSinglePic(message.channel, 'https://i.imgur.com/GWiQcKX.jpg')

    if len(message.mentions) > 0:
        if bot.get_user(nukeCode["user"]["europaBOT"]) in message.mentions:
            raidCode = message.content.split(" ")
            await message.delete()
            await message.channel.send("%s %s"%(nukeCode["role"]["europa"], raidCode[-1]))

    await bot.process_commands(message)

#============== BOT COMMANDS ==============================
@bot.command(pass_context = True)
async def help(ctx, detail = "None"):
    if detail.lower() == "none":
        embed = discord.Embed(colour = discord.Colour.teal(), description = "Type `}help [command]` for more help.\tE.g. `}help down`")
        embed.set_author(name='Help')
        embed.add_field(name='Commands', value="`down` `up` `checkImages` `truck` `bonk` `riot` `birthday` `TE`", inline=False)
        embed.add_field(name='Other Features', value='Send 5 "a"s\nSend "cricket cricket"\nSend "raaid"', inline=False)
        embed.add_field(name='Source Code', value='https://github.com/shironats/Jannubot/blob/V2.20_21/09/DiscordBot.py', inline=False)
    elif detail.lower() == 'down':
        embed = discord.Embed(colour = discord.Colour.teal(), description = 'Spams random "Buff is down" images')
        embed.set_author(name='}down')
    elif detail.lower() == 'up':
        embed = discord.Embed(colour = discord.Colour.teal(), description = 'Spams random "Buff is up" image')
        embed.set_author(name='}up')
    elif detail.lower() == 'checkimages':
        embed = discord.Embed(colour = discord.Colour.teal(), description = 'Check all images')
        embed.set_author(name='}checkImages')
    elif detail.lower() == 'truck':
        embed = discord.Embed(colour = discord.Colour.teal(), description = 'Sends a truck after that person')
        embed.set_author(name='}truck [@ someone]')
    elif detail.lower() == 'bonk':
        embed = discord.Embed(colour = discord.Colour.teal(), description = 'Bonks that person')
        embed.set_author(name='}bonk [@ someone] "reason for bonk (optional)"')
    elif detail.lower() == 'riot':
        embed = discord.Embed(colour = discord.Colour.teal(), description = 'Time to RIOT!!')
        embed.set_author(name='}riot')
    elif detail.lower() == 'birthday':
        embed = discord.Embed(colour = discord.Colour.teal(), description = 'Sends your birthday to my txt file')
        embed.set_author(name='}birthday [date] [month]')
    elif detail.lower() == 'te':
        embed = discord.Embed(colour = discord.Colour.teal(), description = 'Calls people subscribed to DA TE Services')
        embed.set_author(name='}TE [code]')
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
    embed = discord.Embed(colour = discord.Colour.teal(), description = '{0.mention}, {1.mention} sends their regards.'.format(member, ctx.message.author))
    embed.set_image(url='attachment://img%s' %(link[27:]))
    await sendSinglePic(ctx, link, embed)

@bot.command()
async def bonk(ctx, member: discord.Member, reason = "being bad"):
    """Bonks a member"""
    if ((member == bot.get_user(nukeCode["user"]["joe"])) or (member == bot.get_user(nukeCode["user"]["chinpo"]))):
        link = 'https://i.imgur.com/ZvUC0Eq.jpg'
    else:
        link = bonkImages[random.randint(0,len(bonkImages)-1)]
    if (member == bot.get_user(nukeCode["user"]["self"])):
        embed = discord.Embed(colour = discord.Colour.teal(), description = "{0.mention} has been BONKED by {1.mention} for {2}.".format(ctx.message.author, member, reason))
    else:
        embed = discord.Embed(colour = discord.Colour.teal(), description = "{0.mention} has been BONKED by {1.mention} for {2}.".format(member, ctx.message.author, reason))
    embed.set_image(url='attachment://img%s' %(link[27:]))
    await sendSinglePic(ctx, link, embed)

@bot.command()
async def riot(ctx):
    """Time to RIOT!!"""
    await sendSinglePic(ctx, 'https://i.imgur.com/fyG8NZk.png')

@bot.command()
async def bday(ctx):
    """Birthdays"""
    if(ctx.guild.id == nukeCode["misc"]["jannupals"]):
        embed = discord.Embed(colour = discord.Colour.teal())
        embed.set_author(name='BIRTHDAYS, PEOPLE, BIRTHDAYS')
        for iCounter in range(len(months)):
            embed.add_field(name=months[iCounter], value=birthdays[months[iCounter]])
        await ctx.send(embed=embed)
    else:
        await ctx.send("Sorry, permission denied")

@bot.command()
async def birthday(ctx, date: int, month: int):
    """Set Birthday"""
    if(ctx.guild.id == nukeCode["misc"]["jannupals"]):
        addBirthdays(ctx, date, month)
        getBirthdays()
        await ctx.send("Your birthday has been added to DA's database")
    else:
        await ctx.send("Sorry, permission denied")

@bot.command()
async def TE(ctx, raidcode: str):
    """Call TE Peeps"""
    if(ctx.guild.id == nukeCode["misc"]["jannupals"]):
        await ctx.send("%s %s %s %s %s %s %s %s" %(nukeCode["role"]["twinele"],
                                                   raidcode,
                                                   bot.get_user(nukeCode["user"]["zeo"]).mention,
                                                   bot.get_user(nukeCode["user"]["nana"]).mention,
                                                   bot.get_user(nukeCode["user"]["bunny"]).mention,
                                                   bot.get_user(nukeCode["user"]["wayne"]).mention,
                                                   bot.get_user(nukeCode["user"]["yonji"]).mention,
                                                   bot.get_user(nukeCode["user"]["self"]).mention))
    else:
        await ctx.send("Sorry, permission denied")

#@bot.command()
#async def asd(ctx, emot: discord.Emoji):
#    await ctx.send("%i"%(emot.id))

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

#============== FUNCTIONS==============================
def getBirthdays():
    currentMonth = ""
    textfile = data_folder/"JannupalsBirthdays.txt"
    lines = textfile.read_text().split("\n")
    for iCounter in range(len(lines)):
        if lines[iCounter] in months:
            currentMonth = lines[iCounter]
        else:
            if birthdays[currentMonth] == 'None (yet)':
                birthdays[currentMonth] = lines[iCounter]
            else:
                myString = birthdays[currentMonth]
                myString = myString+newLine+lines[iCounter]
                birthdays[currentMonth] = myString

def addBirthdays(ctx, date: int, month: int):
    textfile = data_folder/"JannupalsBirthdays.txt"
    lines = textfile.read_text().split("\n")
    fullText = ""
    strMonth = months[month-1]
    myFlag = False
    for iCounter in range(len(lines)):
        if myFlag == False:
            if lines[iCounter] == strMonth:
                myFlag = True
        else:
            if lines[iCounter][0].isalpha():
                lines.insert(iCounter, "{0} - {1}".format(date, ctx.message.author.name))
                myFlag = False
            elif lines[iCounter][0].isdigit():
                if int(lines[iCounter][:2]) >= date:
                    lines.insert(iCounter, "{0} - {1}".format(date, ctx.message.author.name))
                    myFlag = False
    for iCounter in range(len(lines)):
        fullText += lines[iCounter]
        fullText += newLine
    textfile.write_text(fullText)

#============== ASYNC FUNCTIONS =======================
async def sendPics(ctx, imglink, withText, loopNum = 0):
    async with aiohttp.ClientSession() as session:
        async with session.get(imglink) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            if withText == True:
                await ctx.send('%s or %s, Please reactivate crew buffs, this is reminder number %i' %(nukeCode["role"]["danchou"],nukeCode["role"]["officers"],loopNum), file=discord.File(data, 'img%s'%(imglink[27:])))
            else:
                await ctx.send(file=discord.File(data, 'img%s'%(imglink[27:])))

async def sendSinglePic(ctx, imglink, embed = None):
    async with aiohttp.ClientSession() as session:
        async with session.get(imglink) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, 'img%s'%(imglink[27:])), embed = embed)

bot.run('IDHere')

import discord
from discord.ext import commands, tasks
from discord.utils import get
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import io
import aiohttp
import random
import time
import numpy
import pickle

bot = commands.Bot(command_prefix='}', activity=discord.Game(name='}help'))
bot.remove_command('help')

#============== SENSITIVE NUMBERS ==============
TOKEN = 'IDHere'
SPREADSHEET_ID = 'IDHere'

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

evadeImages = ['https://i.imgur.com/ruwTwKI.png',
               'https://i.imgur.com/HW6rPzB.png',
               'https://i.imgur.com/uYd12fT.png',
               'https://i.imgur.com/N8NCQWH.jpg']

allImages = {"down"     : downImages,
             "up"       : upImages,
             "truck"    : truckImages,
             "bonk"     : bonkImages,
             "evade"    : evadeImages}

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

emojis = {"checkmark"   : '✅',
          "crossmark"   : '❌',
          "uwaaru"      : '<:uwaaru:755820728175034489>',
          "F"           : '🇫'}

ejected = """.      　。　　　•　    　ﾟ　　。　ﾟ
　　.　　　.　　　  　　.　　　　　。　　
　.　　      。　        ඞ   。　    .    •
  •              %s was ejected%s 。　.
　 　　。　　 　　　　ﾟ　　　.　    　　　。
,　　　　.　 .　　    .             .                  ."""

raidQueue = []
myCurrentQueue = [0]
data_folder = Path("DiscordBot_source/")
newLine = "\n"

#============== BOT EVENTS ================================
@bot.event
async def on_ready():
    try:
        getBirthdays()
    except:
        print('Birthdays not found, leaving as empty')
    global sparkBGImage
    global respectBGImage
    sparkBGImage = await getBackgroundImage('https://i.imgur.com/dEuGdHI.jpg')
    respectBGImage = await getBackgroundImage('https://i.imgur.com/4LVGMPn.jpg')
    print('We have logged in as {0.user}'.format(bot))

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
        await message.channel.send('https://i.imgur.com/8n1zvzR.jpg')
#send Jangkrik
    if message.content.lower().endswith('cricket cricket') and message.content.lower().startswith('cricket cricket'):
        await message.channel.send('https://tenor.com/wjNW.gif')
#send Riot pic
    if message.content.lower().find('riot') != -1:
        await message.channel.send('https://i.imgur.com/fyG8NZk.png')
#send Mango memorial
    elif message.content.lower().find(' mango ') != -1:
        await message.channel.send('https://i.imgur.com/EmrHMS7.jpg')
#send Solaire
    elif message.content.lower().find('praise the sun') != -1:
        await message.channel.send('https://i.imgur.com/MYhwSHm.gif')
    elif message.content.lower().find('stickbug') != -1:
        await message.channel.send('https://tenor.com/view/stickbug-excited-dance-dancing-lit-gif-11913206')
#send RAID: SHADOW LEGENDS
    elif message.content.lower().find('ra') != -1:
        if message.content.lower().find('aai') > message.content.lower().find('ra'):
            if message.content.lower().find('id') > message.content.lower().find('aai'):
                await message.channel.send('https://i.imgur.com/eywxw5g.gif')

#counters Uwaaru
    if message.content.find('<:uwaaru:755820728175034489>') != -1:
        await message.channel.send('https://i.imgur.com/GWiQcKX.jpg')

#fixes accidental Europa bot mentions
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
        embed.add_field(name='Global Commands', value="`down` `up` `checkImages` `truck` `bonk` `evade` `F` `votestart`", inline=False)
        embed.add_field(name='Jannupals-Exclusive Commands', value="`birthday` `queue` `next` `clearqueue`", inline=False)
        embed.add_field(name='Keywords Bot will React to', value='`aaaaa` `riot` `cricket cricket` `raaid` `Praise the sun` `stickbug`', inline=False)
        embed.add_field(name='Source Code', value='https://github.com/shironats/Jannubot/blob/V2.70_15/10/DiscordBot.py', inline=False)
    else:
        if detail.lower() == 'down':
            embed = discord.Embed(colour = discord.Colour.teal(), description = 'Spams random "Buff is down" images')
            embed.set_author(name='}down')
        elif detail.lower() == 'up':
            embed = discord.Embed(colour = discord.Colour.teal(), description = 'Sends a random "Buff is up" image')
            embed.set_author(name='}up')
        elif detail.lower() == 'checkimages':
            embed = discord.Embed(colour = discord.Colour.teal(), description = 'Check all images')
            embed.set_author(name='}checkImages')
        elif (detail.lower() == 'truck') or (detail.lower() == 'isekai'):
            embed = discord.Embed(colour = discord.Colour.teal(), description = 'Sends a truck after that person')
            embed.set_author(name='}truck [@ someone]')
            embed.add_field(name='Aliases', value='`}isekai`', inline=False)
        elif detail.lower() == 'bonk':
            embed = discord.Embed(colour = discord.Colour.teal(), description = 'Bonks that person')
            embed.set_author(name='}bonk [@ someone] "reason for bonk [optional]"')
        elif detail.lower() == 'evade':
            embed = discord.Embed(colour = discord.Colour.teal(), description = 'Rolls for bonk evasion')
            embed.set_author(name='}evade')
        elif detail.lower() == 'birthday':
            embed = discord.Embed(colour = discord.Colour.teal(), description = 'Sends your birthday to my txt file')
            embed.set_author(name='}birthday [date] [month]')
            embed.add_field(name='Note', value='Only available to Jannupals members.', inline=False)
        elif detail.lower() == 'f':
            embed = discord.Embed(colour = discord.Colour.teal(), description = 'Press F to Pay Respects')
            embed.set_author(name='}F [@ someone]')
        elif (detail.lower() == 'queue') or (detail.lower() == 'q'):
            embed = discord.Embed(colour = discord.Colour.teal(), description = 'Check raid host queue')
            embed.set_author(name='}queue')
            embed.add_field(name='}queue [raid name]', value='Add to raid host queue', inline=False)
            embed.add_field(name='Note', value='Only available to Jannupals members.', inline=False)
            embed.add_field(name='Aliases', value='`}q`')
        elif (detail.lower() == 'next') or (detail.lower() == 'n'):
            embed = discord.Embed(colour = discord.Colour.teal(), description = 'Moves the raid host queue')
            embed.set_author(name='}next')
            embed.add_field(name='Note', value='Only available to Jannupals members.', inline=False)
            embed.add_field(name='Aliases', value='`}n`', inline=False)
        elif (detail.lower() == 'remove') or (detail.lower() == 'r'):
            embed = discord.Embed(colour = discord.Colour.teal(), description = 'Removes selected entry from the raid host queue')
            embed.set_author(name='}remove [entry number]')
            embed.add_field(name='Note', value='Only available to Jannupals members.', inline=False)
            embed.add_field(name='Aliases', value='`}r`', inline=False)
        elif (detail.lower() == 'clearqueue') or (detail.lower() == 'c'):
            embed = discord.Embed(colour = discord.Colour.teal(), description = 'Clears the raid host queue')
            embed.set_author(name='}clearqueue')
            embed.add_field(name='Note', value='Only available to Jannupals members.', inline=False)
            embed.add_field(name='Aliases', value='`}c`', inline=False)
        elif detail.lower() == 'votestart':
            embed = discord.Embed(colour = discord.Colour.teal(), description = 'Vote to YEET that person')
            embed.set_author(name='}votestart [@ someone]')
        else:
            embed = discord.Embed(colour = discord.Colour.teal(), description = 'Please check }help')
            embed.set_author(name='No such command')
    await ctx.send(embed=embed)

@bot.command()
async def down(ctx):
    """Sends a random 'Buff is down' image"""
    downSpam.start(ctx)

@bot.command()
async def test(ctx, func: str, imgID: int):
    """Function for testing"""
    try:
        link = allImages[func][imgID]
    except:
        link = allImages["bonk"][5]
    await sendSinglePic(ctx, link)

@bot.command()
async def up(ctx):
    """Sets timer for next buff reactivation"""
    downSpam.cancel()
    downSpamBot.cancel()
    link = allImages["up"][random.randint(0,len(upImages)-1)]
    await sendSinglePic(ctx, link)

@bot.command()
async def checkImages(ctx):
    """Check }down images"""
    for imgList in allImages:
        for iCounter in range(len(allImages[imgList])):
            link = allImages[imgList][iCounter]
            await sendSinglePic(ctx, link)
 
@bot.command()
async def truck(ctx, member: discord.Member):
    """Sends a truck over"""
    link = allImages["truck"][random.randint(0,len(truckImages)-1)]
    embed = discord.Embed(colour = discord.Colour.teal(), description = '{0.mention}, {1.mention} sends their regards.'.format(member, ctx.message.author))
    embed.set_image(url='attachment://img%s' %(link[27:]))
    await sendSinglePic(ctx, link, embed)

@bot.command()
async def bonk(ctx, member: discord.Member, reason = "being bad"):
    """Bonks a member"""
    if ((member == bot.get_user(nukeCode["user"]["joe"])) or (member == bot.get_user(nukeCode["user"]["chinpo"]))):
        link = 'https://i.imgur.com/ZvUC0Eq.jpg'
    else:
        link = allImages["bonk"][random.randint(0,len(bonkImages)-1)]
    if (member == bot.get_user(nukeCode["user"]["self"])):
        embed = discord.Embed(colour = discord.Colour.teal(), description = "{0.mention} has been BONKED by {1.mention} for {2}.".format(ctx.message.author, member, reason))
    else:
        embed = discord.Embed(colour = discord.Colour.teal(), description = "{0.mention} has been BONKED by {1.mention} for {2}.".format(member, ctx.message.author, reason))
    embed.set_image(url='attachment://img%s' %(link[27:]))
    await sendSinglePic(ctx, link, embed)

@bot.command()
async def evade(ctx):
    """Roll for evasion"""
    if(random.randint(1,20) > 18):
        link = allImages["evade"][random.randint(0,len(evadeImages)-1)]
        embed = discord.Embed(colour = discord.Colour.teal(), description = "{0.mention} evades the bonk.".format(ctx.message.author))
    else:
        link = allImages["bonk"][random.randint(0,len(bonkImages)-1)]
        embed = discord.Embed(colour = discord.Colour.teal(), description = "{0.mention} is BONKED again by {1.mention} for trying to evade the bonk.".format(ctx.message.author, bot.user))
    embed.set_image(url='attachment://img%s' %(link[27:]))
    await sendSinglePic(ctx, link, embed)

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
        await ctx.send("Sorry, permission denied.")

@bot.command()
async def birthday(ctx, date: int, month: int):
    """Set Birthday"""
    if(ctx.guild.id == nukeCode["misc"]["jannupals"]):
        addBirthdays(ctx, date, month)
        getBirthdays()
        await ctx.send("Your birthday has been added to DA's database")
    else:
        await ctx.send("Sorry, permission denied.")

@bot.command()
async def F(ctx, member: discord.Member):
    """Press F to pay respect"""
    avatarSize = 256
    myImage = respectBGImage.copy()
    imgWidth, imgHeight = myImage.size
    topLeft = (978, 354)
    topRight = (1093, 356)
    bottomLeft = (990, 551)
    bottomRight = (1111, 540)

##    for j in range(imgHeight):
##        for i in range(imgWidth):
##            myTuple = myImage.getpixel((i, j))
##            if myTuple[0] == 255 and myTuple[1] == 255 and myTuple[2] == 255:
##                if i > topRight[0] and j <= topRight[1]+1:
##                    topRight[0], topRight[1] = i, j
##                if i > bottomRight[0]:
##                    bottomRight[0], bottomRight[1] = i, j
##                if j > bottomLeft[1]:
##                    bottomLeft[0], bottomLeft[1] = i, j
##    await ctx.send(str(topLeft)+"\t"+str(topRight)+"\n\n"+str(bottomLeft)+"\t"+str(bottomRight))

    avatarAsset = member.avatar_url_as(format='png', size=256)
    bufferAvatar = io.BytesIO(await avatarAsset.read())
    avatarImage = Image.open(bufferAvatar)
    avatarImage = avatarImage.resize((avatarSize,avatarSize))
    avatarLayer = Image.new('RGBA', (imgWidth, imgHeight))
    avatarLayer.paste(avatarImage, topLeft)
    
    coeffs = find_coeffs(
        [topLeft, topRight, bottomRight, bottomLeft],
        [topLeft, (topLeft[0]+avatarSize, topLeft[1]), (topLeft[0]+avatarSize, topLeft[1]+avatarSize), (topLeft[0], topLeft[1]+avatarSize)])
    avatarLayer = avatarLayer.transform((imgWidth, imgHeight), Image.PERSPECTIVE, coeffs)
    
    myImage = Image.alpha_composite(myImage, avatarLayer)
    myImage = myImage.crop((imgWidth/3, topLeft[1]-50, imgWidth, imgHeight))
    myImage = myImage.convert("RGB")

    buffer_output = io.BytesIO()
    myImage.save(buffer_output, format='JPEG')
    buffer_output.seek(0)

    embed = discord.Embed(colour = discord.Colour.teal(), description = "{0.mention} pays their respects.\nRIP {1.mention}.".format(ctx.message.author, member))
    embed.set_image(url='attachment://img.jpeg')
    myMessage = await ctx.send(file=discord.File(buffer_output, "img.jpeg"), embed = embed)
    await myMessage.add_reaction(emojis["F"])

@bot.command()
async def queue(ctx, raidName: str = "None"):
    """Add raid to queue"""
    if(ctx.guild.id == nukeCode["misc"]["jannupals"]):
        if(raidName != "None"):
            raidQueue.append("%s by %s" %(raidName, ctx.message.author.mention))
            embed = discord.Embed(colour = discord.Colour.teal(), description = "Queued %s [%s]" %(raidName, ctx.message.author.mention))
            await ctx.send(embed=embed)
        else:
            if(len(raidQueue) == 0):
                await ctx.send("```The queue is empty y'all```")
            else:
                qString = "```"
                for x in range(len(raidQueue)):
                    if myCurrentQueue[0] == x:
                        qString = qString + "\t⬐ current raid" + newLine
                    if(raidQueue[x].find("<@!") != -1):
                        qMember = await bot.get_guild(nukeCode["misc"]["jannupals"]).fetch_member(int(raidQueue[x][raidQueue[x].find("<@!")+3:raidQueue[x].find(">", raidQueue[x].find("<@!"))]))
                        qUser = qMember.display_name
                        qString = qString + str(x+1) + ") " + raidQueue[x][:raidQueue[x].find("<@!")] + qUser + newLine
                    else:
                        qMember = await bot.get_guild(nukeCode["misc"]["jannupals"]).fetch_member(int(raidQueue[x][raidQueue[x].find("<@")+2:raidQueue[x].find(">", raidQueue[x].find("<@"))]))
                        qUser = qMember.display_name
                        qString = qString + str(x+1) + ") " + raidQueue[x][:raidQueue[x].find("<@")] + qUser + newLine                            
                    if myCurrentQueue[0] == x:
                        qString = qString + "\t⬑ current raid" + newLine
                qString += "```"
                await ctx.send(qString)
    else:
        await ctx.send("Sorry, permission denied.")

@bot.command()
async def next(ctx):
    """Next raid up"""
    if(ctx.guild.id == nukeCode["misc"]["jannupals"]):
        if len(raidQueue) == 0:
            embed = discord.Embed(colour = discord.Colour.teal(), description = "Please fill with `}queue`")
            embed.set_author(name = "Queue is empty")
        elif myCurrentQueue[0] == (len(raidQueue)-1):
            embed = discord.Embed(colour = discord.Colour.teal(), description = "Please add more with `}queue` or clear with `}clearqueue`")
            embed.set_author(name = "You've reached the end of the queue")
        else:
            myCurrentQueue[0] += 1
            embed = discord.Embed(colour = discord.Colour.teal(), description = "%s" %(raidQueue[myCurrentQueue[0]]))
            embed.set_author(name="Next Up")
        await ctx.send(embed=embed)
    else:
        await ctx.send("Sorry, permission denied.")

@bot.command()
async def remove(ctx, entry: int):
    """Remove queue entry"""
    if(ctx.guild.id == nukeCode["misc"]["jannupals"]):
        if len(raidQueue) == 0:
            embed = discord.Embed(colour = discord.Colour.teal(), description = "Please fill with `}queue`")
            embed.set_author(name = "Queue is empty")
        else:
            raidRemoved = raidQueue.pop(entry-1)
            embed = discord.Embed(colour = discord.Colour.teal(), description = "%s has been removed by [%s]" %(raidRemoved[:raidRemoved.find("by")], ctx.message.author.mention))
            embed.add_field(name="This function was brought to you by:",value=bot.get_user(nukeCode["user"]["haipa"]).mention,inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Sorry, permission denied.")

@bot.command()
async def clearqueue(ctx):
    """Clears raid queue"""
    if(ctx.guild.id == nukeCode["misc"]["jannupals"]):
        raidQueue.clear()
        myCurrentQueue[0] = 0
        await ctx.send("```Queue cleared```")
    else:
        await ctx.send("Sorry, permission denied.")

@bot.command()
async def votestart(ctx, member: discord.Member):
    """Vote to kick off"""
    link = "https://i.imgur.com/rkXH0dl.jpg"
    embed = discord.Embed(colour = discord.Colour.teal(), description = "You have 15 seconds to vote.")
    embed.set_author(name = "Emergency meeting called to eject %s." %(member.display_name))
    embed.set_image(url='attachment://img%s' %(link[27:]))
    myMessage = await sendSinglePic(ctx, link, embed)
    await myMessage.add_reaction(emojis["checkmark"])
    await myMessage.add_reaction(emojis["crossmark"])
    time.sleep(15)
    myMessage = await ctx.fetch_message(myMessage.id)
    if myMessage.reactions[0].count > myMessage.reactions[1].count:
        await ctx.send(ejected %(member.display_name, "."))
    else:
        await ctx.send(ejected %("No one", ". (Skipped)"))

#============== ALT COMMANDS ==========================
@bot.command(pass_context = True)
async def h(ctx, detail = "None"):
    """Same as }help"""
    await help(ctx, detail)

@bot.command()
async def isekai(ctx, member: discord.Member):
    """Same as }truck"""
    await truck(ctx, member)

@bot.command()
async def q(ctx, raidName: str = "None"):
    """Same as }queue"""
    await queue(ctx, raidName)

@bot.command()
async def n(ctx):
    """Same as }next"""
    await next(ctx)

@bot.command()
async def c(ctx):
    """Same as }clearqueue"""
    await clearqueue(ctx)

@bot.command()
async def r(ctx, entry: int):
    """Same as }remove"""
    await remove(ctx, entry)

#============== BOT LOOPS =============================
@tasks.loop(seconds=10)
async def downSpam(ctx):
    link = allImages["down"][random.randint(0,len(downImages)-1)]
    await sendPics(ctx, link, True, downSpam.current_loop)

@tasks.loop(seconds=10)
async def downSpamBot(target_channel):
    link = allImages["down"][random.randint(0,len(downImages)-1)]
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

def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

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
            return await ctx.send(file=discord.File(data, 'img%s'%(imglink[27:])), embed = embed)

async def getBackgroundImage(imglink: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(imglink) as resp:
            if resp.status != 200:
                print('Could not download file...')
                return None
            aImage = io.BytesIO(await resp.read())
            myImage = Image.open(aImage)
            myImage = myImage.convert('RGBA')
            return myImage
        
bot.run(TOKEN)

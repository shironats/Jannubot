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
import time         #for delay in votestart
import datetime     #timestamp in on_message_delete
import numpy        #for calculation for F
import pickle       #for storing access data for google sheets
import pytz         #for time zone data

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='}', activity=discord.Game(name='}help'), case_insensitive=True, intents=intents)
bot.remove_command('help')

#============== SENSITIVE NUMBERS ==============
TOKEN = 'IDHere'
SPREADSHEET_ID = 'IDHere'

miscID = {"jannupals"   : IDHere, #server
          "botfest"     : IDHere, #channel
          "general"     : IDHere, #channel
          "deletedMsg"  : IDHere, #channel
          }

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
          "chinpo"      : IDHere,
          "lilium"      : IDHere,
          "alwing"      : IDHere,
          "malsi"       : IDHere,
          "islam"       : IDHere,
          "invar"       : IDHere,
          }

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
              'https://i.imgur.com/SA4uMHJ.jpg',
              'https://i.imgur.com/as1DDi7.gif']

evadeImages = ['https://i.imgur.com/ruwTwKI.png',
               'https://i.imgur.com/HW6rPzB.png',
               'https://i.imgur.com/uYd12fT.png',
               'https://i.imgur.com/N8NCQWH.jpg']

miscImages = ['https://i.imgur.com/h7xGExX.png',    #bonkcounterBG
              'https://i.imgur.com/4LVGMPn.jpg',    #respectBG
              'https://i.imgur.com/8n1zvzR.jpg',    #aaaaa
              'https://tenor.com/wjNW.gif',         #cricket
              'https://i.imgur.com/fyG8NZk.png',    #riot
              'https://i.imgur.com/EmrHMS7.jpg',    #mango
              'https://i.imgur.com/MYhwSHm.gif',    #solaire
              'https://tenor.com/bnM1E.gif',        #stickbug
              'https://i.imgur.com/eywxw5g.gif',    #RAID
              'https://i.imgur.com/GWiQcKX.jpg',    #umaruSHUTUP
              'https://i.imgur.com/ZvUC0Eq.jpg',    #joe/chinpo bonk
              'https://i.imgur.com/rkXH0dl.jpg',    #votestart
              'https://i.imgur.com/Py5OCUW.png',    #bonked
              'https://i.imgur.com/xb4ieP2.png',    #bonker
              'https://i.imgur.com/X6HEDCc.png',    #kiryu
              ]

allImages = {"down"     : downImages,
             "up"       : upImages,
             "truck"    : truckImages,
             "bonk"     : bonkImages,
             "evade"    : evadeImages,
             "misc"     : miscImages}

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
          "F"           : '🇫',
          "catcry"      : '<:catcry:686044174570881027>',
          }

ejected = """.      　。　　　•　    　ﾟ　　。　ﾟ
　　.　　　.　　　  　　.　　　　　。
　.　　      。　        ඞ   。　    .    •
  •              %s was %s%s 。　.
　 　　。　　 　　　　ﾟ　　　.　    　　　。
,　　　　.　 .　　    .             .                  ."""

raidQueue = []
myCurrentQueue = [0]
data_folder = Path("DiscordBot_source/")
newLine = "\n"

#============== BOT EVENTS ================================
@bot.event
async def on_connect():
    print('Connected')
    try:
        clearBirthdays()
        getBirthdays()        
    except:
        print('Birthdays not found, leaving as empty')
    global bonkcountBGImage
    global respectBGImage
    global bonkedImage
    global bonkerImage
    global kiryuBGImage
    bonkcountBGImage = await getBackgroundImage(allImages["misc"][0])
    respectBGImage = await getBackgroundImage(allImages["misc"][1])
    bonkedImage = await getBackgroundImage(allImages["misc"][11])
    bonkerImage = await getBackgroundImage(allImages["misc"][12])
    kiryuBGImage = await getBackgroundImage(allImages["misc"][13])
    print('Resources loaded')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    dev = bot.get_user(nukeCode["user"]["self"])
    await dev.send('I have logged on at {0}.'.format(datetime.datetime.now(pytz.timezone('Asia/Jakarta'))))

@bot.event
async def on_message_delete(message):
    if message.guild.id == nukeCode["misc"]["jannupals"]:
        # disregard deleted bot messages
        if not message.author.bot:
            if not message.content.startswith(('!', '?', '-', '}', '.', '$', 't!')):
                # sends the deleted message back to deleted messages channel w/ timestamp
                msgChannel = bot.get_channel(nukeCode["misc"]["deletedMsg"])
                embed = discord.Embed(colour = discord.Colour.teal(),
                                    description='Message sent by {0.mention} deleted in {1.mention}\n\n{2}'.format(message.author, message.channel, message.content))
                embed.set_author(name=str(message.author), icon_url=message.author.avatar_url)
                embed.set_footer(text=datetime.datetime.now(pytz.timezone('Asia/Tokyo')))
                if len(message.attachments) > 0:
                    embed.set_image(url=message.attachments[0].proxy_url)

                await msgChannel.send(embed=embed)

@bot.event
async def on_message(message):
    nadeko = bot.get_user(nukeCode["user"]["nadekoBOT"])

    # disregard messages from itself
    if message.author == bot.user:
        return
    # nadeko-triggered }down
    elif message.author == nadeko:
        if message.content.startswith('}down'):
            if message.content.endswith('general'):
                downSpamBot.start(nukeCode["misc"]["general"])
            else:
                downSpamBot.start(nukeCode["misc"]["botfest"])

#send Screaming cat image
    if message.content.lower().endswith('aaaaa'):
        await message.channel.send(allImages["misc"][2])
#send Jangkrik
    elif message.content.lower().endswith('cricket cricket') and message.content.lower().startswith('cricket cricket'):
        await message.channel.send(allImages["misc"][3])

#send Riot pic
    if message.content.lower().find('riot') != -1:
        await message.channel.send(allImages["misc"][4])
#send Solaire
    elif message.content.lower().find('praise the sun') != -1:
        await message.channel.send(allImages["misc"][6])
#send stickbug
    elif message.content.lower().find('stickbug') != -1:
        await message.channel.send(allImages["misc"][7])
#send RAID: SHADOW LEGENDS
    elif message.content.lower().find('ra') != -1:
        if message.content.lower().find('aai') > message.content.lower().find('ra'):
            if message.content.lower().find('id') > message.content.lower().find('aai'):
                await message.channel.send(allImages["misc"][8])

#fixes accidental Europa bot mentions
    if len(message.mentions) > 0:
        if bot.get_user(nukeCode["user"]["europaBOT"]) in message.mentions:
            raidCode = message.content.split(" ")
            await message.delete()
            await message.channel.send("%s %s"%(nukeCode["role"]["europa"], raidCode[-1]))

    await bot.process_commands(message)

#============== BOT HELP COMMANDS ==============================
@bot.group(aliases=['h'], case_insensitive=True)
async def help(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(colour = discord.Colour.teal(), description = "Type `}help [command]` for more help.\tE.g. `}help down`")
        embed.set_author(name='Help')
        embed.add_field(name='Global Commands', value="`up` `checkImages` `truck` `bonk` `evade` `F` `votestart` `yeet` `emote` `baka` `UStime`", inline=False)
        embed.add_field(name='Jannupals-Exclusive Commands', value="`down` `bday` `birthday` `queue` `next` `clearqueue` `remove` `bonkcounter` `cleaning`", inline=False)
        embed.add_field(name='Keywords Bot will React to', value='`aaaaa` `riot` `cricket cricket` `raaid` `Praise the sun` `stickbug`', inline=False)
        embed.add_field(name='Other stuff', value='''[Source Code](https://github.com/shironats/Jannubot/blob/master/DiscordBot.py)
                                                    [Jannubot invite link](https://discord.com/api/oauth2/authorize?client_id=731865140068089897&permissions=523328&scope=bot)''', inline=False)
        await ctx.send(embed=embed)

@help.command()
async def down(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Spams random "Buff is down" images')
    embed.set_author(name='}down')
    embed.add_field(name='Note', value='Only available to Jannupals members.', inline=False)
    await ctx.send(embed=embed)

@help.command()
async def up(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Sends a random "Buff is up" image')
    embed.set_author(name='}up')
    await ctx.send(embed=embed)

@help.command()
async def checkImages(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Check all images')
    embed.set_author(name='}checkImages')
    await ctx.send(embed=embed)

@help.command(aliases=['isekai'])
async def truck(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Sends a truck after that person')
    embed.set_author(name='}truck [@ someone]')
    embed.add_field(name='Aliases', value='`}isekai`', inline=False)
    await ctx.send(embed=embed)

@help.command()
async def bonk(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Bonks that person')
    embed.set_author(name='}bonk [@ someone] "reason for bonk [optional]"')
    await ctx.send(embed=embed)

@help.command()
async def evade(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Rolls for bonk evasion')
    embed.set_author(name='}evade')
    await ctx.send(embed=embed)

@help.command()
async def birthday(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Sends your birthday to my txt file.\nBoth inputs must be numbers.')
    embed.set_author(name='}birthday [date] [month]')
    embed.add_field(name='Note', value='Only available to Jannupals members.', inline=False)
    await ctx.send(embed=embed)

@help.command()
async def F(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Press F to Pay Respects')
    embed.set_author(name='}F [@ someone]')
    await ctx.send(embed=embed)

@help.command(aliases=['q'])
async def queue(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Check raid host queue')
    embed.set_author(name='}queue')
    embed.add_field(name='}queue [raid name]', value='Add to raid host queue', inline=False)
    embed.add_field(name='Note', value='Only available to Jannupals members.', inline=False)
    embed.add_field(name='Aliases', value='`}q`')
    await ctx.send(embed=embed)

@help.command(aliases=['n'])
async def next(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Moves the raid host queue')
    embed.set_author(name='}next')
    embed.add_field(name='Note', value='Only available to Jannupals members.', inline=False)
    embed.add_field(name='Aliases', value='`}n`', inline=False)
    await ctx.send(embed=embed)

@help.command(aliases=['r'])
async def remove(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Removes selected entry from the raid host queue')
    embed.set_author(name='}remove [entry number]')
    embed.add_field(name='Note', value='Only available to Jannupals members.', inline=False)
    embed.add_field(name='Aliases', value='`}r`', inline=False)
    await ctx.send(embed=embed)

@help.command(aliases=['c'])
async def clearqueue(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Clears the raid host queue')
    embed.set_author(name='}clearqueue')
    embed.add_field(name='Note', value='Only available to Jannupals members.', inline=False)
    embed.add_field(name='Aliases', value='`}c`', inline=False)
    await ctx.send(embed=embed)

@help.command()
async def votestart(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Vote to YEET that person')
    embed.set_author(name='}votestart [@ someone]')
    await ctx.send(embed=embed)

@help.command()
async def yeet(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Just YEET anything')
    embed.set_author(name='}yeet [something]')
    await ctx.send(embed=embed)

@help.command()
async def bonkcounter(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Displays your bonk counters')
    embed.set_author(name='}bonkcounter')
    embed.add_field(name='Note', value='Only available to Jannupals members.', inline=False)
    await ctx.send(embed=embed)

@help.command(aliases=['emo', 'emotes'])
async def emote(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Sends an animated emote\nWill send a list of animated emotes instead if argument is not given')
    embed.set_author(name='}emote [emote name]')
    embed.add_field(name='Aliases', value='`}emo` `}emotes`', inline=False)
    await ctx.send(embed=embed)

@help.command()
async def bday(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Displays recorded member birthdays')
    embed.set_author(name='}bday')
    embed.add_field(name='Note', value='Only available to Jannupals members.', inline=False)
    await ctx.send(embed=embed)

@help.command()
async def baka(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Kiryu is sad for you')
    embed.set_author(name='}baka [@ someone]')
    await ctx.send(embed=embed)

@help.command()
async def UStime(ctx):
    embed = discord.Embed(colour = discord.Colour.teal(), description = 'Converts given JST time to US times')
    embed.set_author(name='}time [####]')
    await ctx.send(embed=embed)

#============== BOT COMMANDS ==============================
@bot.command()
async def down(ctx):
    """Sends a random 'Buff is down' image"""
    if(ctx.guild.id == nukeCode["misc"]["jannupals"]):
        downSpam.start(ctx)
    else:
        await ctx.send("Sorry, permission denied.")

@bot.command()
async def up(ctx):
    """Stops 'Buff is down' image spam"""
    downSpam.cancel()
    downSpamBot.cancel()
    link = allImages["up"][random.randrange(0,len(upImages))]
    await sendSinglePic(ctx, link)

@bot.command()
async def checkImages(ctx):
    """Checks all images"""
    for imgList in allImages:
        for iCounter in range(len(allImages[imgList])):
            link = allImages[imgList][iCounter]
            # solves problem with gifs not loading properly if sent directly
            if 'tenor' in link or 'gif' not in link:
                await ctx.send(link)
            else:
                await sendSinglePic(ctx, link)

@bot.command(aliases=['isekai'])
async def truck(ctx, member: discord.Member):
    """Sends a truck over"""
    link = allImages["truck"][random.randrange(0,len(truckImages))]
    embed = discord.Embed(colour = discord.Colour.teal(), description = '{0.mention}, {1.mention} sends their regards.'.format(member, ctx.message.author))
    embed.set_image(url='attachment://img%s' %(link[link.find(".",link.find(".com")+1):]))
    await sendSinglePic(ctx, link, embed)

@bot.command()
async def bonk(ctx, member: discord.Member, reason = "being bad"):
    """Bonks a member"""
    # use special bonk image for joe and chinpo
    if ((member == bot.get_user(nukeCode["user"]["joe"])) or (member == bot.get_user(nukeCode["user"]["chinpo"]))):
        link = allImages["misc"][10]
    else:
        link = allImages["bonk"][random.randrange(0,len(bonkImages))]

    #returns bonk to sender if targeted at dev
    if ((member == bot.get_user(nukeCode["user"]["self"])) or (member == bot.get_user(nukeCode["user"]["invar"])) 
    or (ctx.author.id == nukeCode["user"]["malsi"]) or (ctx.author.id == nukeCode["user"]["islam"])):
        embed = discord.Embed(colour = discord.Colour.teal(), description = "{0.mention} has been BONKED by {1.mention} for {2}.".format(ctx.message.author, member, reason))
        memberIDs = (str(ctx.author.id), str(member.id))
    else:
        embed = discord.Embed(colour = discord.Colour.teal(), description = "{0.mention} has been BONKED by {1.mention} for {2}.".format(member, ctx.message.author, reason))
        memberIDs = (str(member.id), str(ctx.author.id))

    embed.set_image(url='attachment://img%s' %(link[link.find(".",link.find(".com")+1):]))
    await sendSinglePic(ctx, link, embed)
    if(ctx.guild.id == nukeCode["misc"]["jannupals"]):
        # send a message to dev if bonk sheet is not updated
        if not updateSheet(memberIDs[0], memberIDs[1]):
            dev = bot.get_user(nukeCode["user"]["self"])
            await dev.send('Failed to update sheet')

@bot.command()
async def bonkcounter(ctx, member: discord.Member = None):
    """Checks bonk counter"""
    if(ctx.guild.id == nukeCode["misc"]["jannupals"]):
        if member == None:
            target = ctx.author
        else:
            target = member
        stats = readSheet(str(target.id))

        if stats == None:
            await ctx.send("You are not in DA's database yet")
        else:
            card = bonkCard(target.name, stats)
            card = await setAvatarnIcon(target, card)

            #send image
            imgBuffer = io.BytesIO()
            card.save(imgBuffer, format='PNG')
            imgBuffer.seek(0)
            await ctx.send("Border credits to %s"%(bot.get_user(nukeCode["user"]["alwing"])), file=discord.File(imgBuffer, 'myimg.png'))
    else:
        await ctx.send("Sorry, permission denied.")

@bot.command()
async def evade(ctx):
    """Roll for evasion"""
    # evade chance of 2/20
    if((random.randint(1,20) > 15) or (ctx.author.id == nukeCode["user"]["invar"])):
        link = allImages["evade"][random.randrange(0,len(evadeImages))]
        embed = discord.Embed(colour = discord.Colour.teal(), description = "{0.mention} evades the thing.".format(ctx.message.author))
    else:
        link = allImages["bonk"][random.randrange(0,len(bonkImages))]
        embed = discord.Embed(colour = discord.Colour.teal(), description = "{0.mention} is BONKED again by {1.mention} for trying to evade the thing.".format(ctx.message.author, bot.user))
    embed.set_image(url='attachment://img%s' %(link[link.find(".",link.find(".com")+1):]))
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
##    if(ctx.author.id == nukeCode["user"]["self"]):
        try:
            addBirthdays(ctx, date, month)
        except:
            await ctx.send("Sorry, something went wrong")
        else:
            clearBirthdays()
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
    topLeft = (976, 353)
    topRight = (1094, 354)
    bottomLeft = (990, 551)
    bottomRight = (1112, 540)

    # loads user profile picture and pastes it on a new image layer
    avatarAsset = member.avatar_url_as(format='png', size=256)
    bufferAvatar = io.BytesIO(await avatarAsset.read())
    avatarImage = Image.open(bufferAvatar)
    avatarImage = avatarImage.resize((avatarSize,avatarSize))
    avatarLayer = Image.new('RGBA', (imgWidth, imgHeight))
    avatarLayer.paste(avatarImage, topLeft)

    # finds perspective coefficients and transforms image to desired perspective
    coeffs = find_coeffs(
        [topLeft, topRight, bottomRight, bottomLeft],
        [topLeft, (topLeft[0]+avatarSize, topLeft[1]), (topLeft[0]+avatarSize, topLeft[1]+avatarSize), (topLeft[0], topLeft[1]+avatarSize)])
    avatarLayer = avatarLayer.transform((imgWidth, imgHeight), Image.PERSPECTIVE, coeffs)

    # pastes profile picture layer on image
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

@bot.command(aliases=['q'])
async def queue(ctx, raidName: str = "None"):
    """Add raid to queue"""
    if(ctx.guild.id == nukeCode["misc"]["jannupals"]):
        # appends raid entry to the queue
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
                    # for members with nicknames
                    if(raidQueue[x].find("<@!") != -1):
                        qMember = await bot.get_guild(nukeCode["misc"]["jannupals"]).fetch_member(int(raidQueue[x][raidQueue[x].find("<@!")+3:raidQueue[x].find(">", raidQueue[x].find("<@!"))]))
                        qUser = qMember.display_name
                        qString = qString + str(x+1) + ") " + raidQueue[x][:raidQueue[x].find("<@!")] + qUser + newLine
                    # for members without nicknames
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

@bot.command(aliases=['n'])
async def next(ctx):
    """Next raid up"""
    if(ctx.guild.id == nukeCode["misc"]["jannupals"]):
        # empty queue
        if len(raidQueue) == 0:
            embed = discord.Embed(colour = discord.Colour.teal(), description = "Please fill with `}queue`")
            embed.set_author(name = "Queue is empty")
        # reached last queue
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

@bot.command(aliases=['r'])
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

@bot.command(aliases=['c'])
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
    link = allImages["misc"][11]
    embed = discord.Embed(colour = discord.Colour.teal(), description = "You have 15 seconds to vote.")
    embed.set_author(name = "Emergency meeting called to eject %s." %(member.display_name))
    embed.set_image(url='attachment://img%s' %(link[link.find(".",link.find(".com")+1):]))
    myMessage = await sendSinglePic(ctx, link, embed)
    await myMessage.add_reaction(emojis["checkmark"])
    await myMessage.add_reaction(emojis["crossmark"])
    time.sleep(15)
    myMessage = await ctx.fetch_message(myMessage.id)
    # more 'yes' than 'no'
    if myMessage.reactions[0].count > myMessage.reactions[1].count:
        await ctx.send(ejected %(member.display_name, "ejected", "."))
    # more 'no' than 'yes'
    else:
        await ctx.send(ejected %("No one", "ejected", ". (Skipped)"))

@bot.command()
async def yeet(ctx, thing: str):
    """Just kick off"""
    await ctx.send(ejected %(thing, "yeeted", "."))

@bot.command(aliases=['emo'])
async def emote(ctx, emoteName: str = None):
    """Let the people use animated emotes"""
    emotesList = getEmojis(ctx.guild, True)
    if emoteName != None:
        # create and initialize variable 'check'
        check = False
        for content in emotesList:
            if emoteName.lower() in content.lower():
                check = True
                await ctx.send(content)
        if not check:
            await ctx.send('Emote not found')
    else:
        try:
            await ctx.send(" ".join(emotesList))
        except:
            part1 = emotesList[:len(emotesList)//2]
            part2 = emotesList[len(emotesList)//2:]
            await ctx.send(" ".join(part1))
            await ctx.send(" ".join(part2))

@bot.command()
async def baka(ctx, member: discord.Member):
    avatarSize = 256
    myImage = kiryuBGImage.copy()
    imgWidth, imgHeight = myImage.size
    topLeft = (323, 364)
    topRight = (568, 335)
    bottomLeft = (352, 609)
    bottomRight = (597, 580)

    # loads user profile picture and pastes it on a new image layer
    avatarAsset = member.avatar_url_as(format='png', size=256)
    bufferAvatar = io.BytesIO(await avatarAsset.read())
    avatarImage = Image.open(bufferAvatar)
    avatarImage = avatarImage.resize((avatarSize,avatarSize))
    avatarLayer = Image.new('RGBA', (imgWidth, imgHeight))
    avatarLayer.paste(avatarImage, topLeft)

    # finds perspective coefficients and transforms image to desired perspective
    coeffs = find_coeffs(
        [topLeft, topRight, bottomRight, bottomLeft],
        [topLeft, (topLeft[0]+avatarSize, topLeft[1]), (topLeft[0]+avatarSize, topLeft[1]+avatarSize), (topLeft[0], topLeft[1]+avatarSize)])
    avatarLayer = avatarLayer.transform((imgWidth, imgHeight), Image.PERSPECTIVE, coeffs)

    # pastes profile picture layer on image
    myImage = Image.alpha_composite(myImage, avatarLayer)
    myImage = myImage.convert("RGB")

    buffer_output = io.BytesIO()
    myImage.save(buffer_output, format='JPEG')
    buffer_output.seek(0)

    embed = discord.Embed(colour = discord.Colour.teal(), description = "だめだね！\nだめよ！\nだめなのよ！！".format(ctx.message.author, member))
    embed.set_image(url='attachment://img.jpeg')
    myMessage = await ctx.send(file=discord.File(buffer_output, "img.jpeg"), embed = embed)
    await myMessage.add_reaction(emojis["catcry"])

@bot.command()
async def test(ctx, func: str, imgID: int):
    """Function for testing"""
    link = allImages[func][imgID]
    await sendSinglePic(ctx, link)

@bot.command()
async def cleaning(ctx):
    """For emote cleaning"""
    if(ctx.guild.id == nukeCode["misc"]["jannupals"]):
        emotesList = getEmojis(ctx.guild, False)
        if len(emotesList) != 100:
            await ctx.send("Not yet 100, no needa clean yet.")
        else:
            batch1 = await ctx.send("Batch 1")
            batch2 = await ctx.send("Batch 2")
            batch3 = await ctx.send("Batch 3")
            batch4 = await ctx.send("Batch 4")
            batch5 = await ctx.send("Batch 5")
            for i in range(20):
                await batch1.add_reaction(emotesList[i])
            for i in range(20,40):
                await batch2.add_reaction(emotesList[i])
            for i in range(40,60):
                await batch3.add_reaction(emotesList[i])
            for i in range(60,80):
                await batch4.add_reaction(emotesList[i])
            for i in range(80,100):
                await batch5.add_reaction(emotesList[i])
    else:
        await ctx.send("Sorry, permission denied.")

@bot.command()
async def UStime(ctx, jst: str = "now"):
    """Converts JST to PST/MST/CST/EST"""
    myFlag = False
    if (jst == 'now') or (len(jst) == 4):
        UTCTime = None
        embed = discord.Embed(colour = discord.Colour.teal())
        if jst == 'now':
            UTCTime = datetime.datetime.now(pytz.timezone('UTC'))
            embed.set_author(name='Now')
        else:
            UTCh = int(jst[:2]) - 9
            UTCm = int(jst[2:])
            # fixes negative hours if entered time is earlier than 9am
            if UTCh < 0:
                UTCh = UTCh + 24
            # checks for 60+ minutes
            try:
                currentTime = datetime.datetime.utcnow()
                UTCTime = datetime.datetime(currentTime.year, currentTime.month, currentTime.day,
                                            UTCh, UTCm, 0, 0,
                                            pytz.timezone('UTC'))
                embed.set_author(name='%s JST'%(jst))
            except:
                await UStime(ctx, "wrong")
        # converts requested time to specified timezones
        timeList = cvtTime(UTCTime)
        embed.add_field(name='HST', value=timeList[0].strftime("%X"), inline=False)
        embed.add_field(name='PST', value=timeList[1].strftime("%X"), inline=False)
        embed.add_field(name='MST', value=timeList[2].strftime("%X"), inline=False)
        embed.add_field(name='CST', value=timeList[3].strftime("%X"), inline=False)
        embed.add_field(name='EST', value=timeList[4].strftime("%X"), inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Please enter JST time in 2400 format or 'now'")

@bot.command()
async def asd(ctx):
    server = ctx.guild
    emojis = [str(x) for x in server.emojis]
    emojis.sort()
    emojis1 = emojis[0:len(emojis)//2]
    emojis2 = emojis[len(emojis)//2:-1]
    await ctx.send(" ".join(emojis1))
    await ctx.send(" ".join(emojis2))

##@bot.command()
##async def aaa(ctx, msgID: int):
##    msg = await ctx.fetch_message(msgID)
##    print(msg.content)
##    embed = discord.Embed(colour = discord.Colour.teal(), description = msg.content)
##    await ctx.send(embed=embed)

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

def clearBirthdays():
    for i in months:
        birthdays[i] = 'None (yet)'

def addBirthdays(ctx, date: int, month: int):
    textfile = data_folder/"JannupalsBirthdays.txt"
    lines = textfile.read_text().split("\n")
    fullText = ""
    linesToDel = []
    strMonth = months[month-1]
    myFlag = False
    for iCounter in range(len(lines)):
        if myFlag == False:
            if lines[iCounter] == strMonth:
                myFlag = True
        else:
            try:
                if lines[iCounter][0].isalpha():
                    lines.insert(iCounter, "{0} - {1}".format(date, ctx.message.author.name))
                    myFlag = False
                elif lines[iCounter][0].isdigit():
                    if int(lines[iCounter][:2]) >= date:
                        lines.insert(iCounter, "{0} - {1}".format(date, ctx.message.author.name))
                        myFlag = False
            except:
                linesToDel.append(iCounter)
    for i in range(len(linesToDel)):
        del lines[linesToDel[0]]
    for iCounter in range(len(lines)):
        fullText += lines[iCounter]
        fullText += newLine

    textfile.write_text(fullText)

def find_coeffs(pa, pb):
    # https://stackoverflow.com/questions/14177744/
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

def updateSheet(bonked: str, bonker: str):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    RANGE_NAME = 'Sheet1!A2:C'

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(data_folder/'token.pickle'):
        with open(data_folder/'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                data_folder/'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(data_folder/'token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    # Call the Sheets API
    sheet = service.spreadsheets()

    # Read
    readResult = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = readResult.get('values', [])

    if not values:
        print('No data found.')
        return False
    else:
        users = []
        for row in values:
            users.append(str(row[0]))
            # Bonker -> Column B
            # Bonked -> Column C
            # If user is the bonker
            if str(row[0]) == bonker:
                row[1] = int(row[1]) + 1
                row[2] = int(row[2])
            # If user is the bonked
            elif str(row[0]) == bonked:
                row[1] = int(row[1])
                row[2] = int(row[2]) + 1
            # Even if user is not both, we rewrite the data
            # Because otherwise there is data type mismatch
            # And this results in existing entries disregarded, causing duplicate entries
            else:
                row[1] = int(row[1])
                row[2] = int(row[2])
        if bonker not in users:
            values.append([bonker, 1, 0])
        if bonked not in users:
            values.append([bonked, 0, 1])

    # Write
    body = {'values': values}
    writeResult = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                                   range=RANGE_NAME,
                                   valueInputOption='USER_ENTERED',
                                   body=body).execute()
    return True

def readSheet(memberID):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    RANGE_NAME = 'Sheet1!A2:C'

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(data_folder/'token.pickle'):
        with open(data_folder/'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                data_folder/'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(data_folder/'token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    # Call the Sheets API
    sheet = service.spreadsheets()

    # Read
    readResult = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = readResult.get('values', [])

    if not values:
        print('No data found.')
        return None
    else:
        users = []
        for row in values:
            users.append(row[0])
            # Bonker -> Column B
            # Bonked -> Column C
            if row[0] == memberID:
                stats = (int(row[1]), int(row[2]))
                return stats
        if memberID not in users:
            return None

def bonkCard(userName, bonkStats):
    avatarSize = 128
    iconSize = 70
    nameSize = 1
    numSize = 1
    myImage = bonkcountBGImage.copy()

    imgWidth, imgHeight = myImage.size

    #name box
    rectLeft = 50
    rectTop = 30
    rectRight = imgWidth - 50
    rectBottom = rectTop + avatarSize + 5
    rectWidth = rectRight - rectLeft
    rectHeight = rectBottom - rectTop
    #bonked box
    bonkedRectLeft = rectLeft
    bonkedRectTop = rectBottom + 10
    bonkedRectRight = imgWidth / 2 - 5
    bonkedRectBottom = bonkedRectTop + iconSize + 5
    bonkedRectWidth = bonkedRectRight - bonkedRectLeft
    bonkedRectHeight = bonkedRectBottom - bonkedRectTop
    #bonker box
    bonkerRectLeft = bonkedRectRight + 10
    bonkerRectTop = rectBottom + 10
    bonkerRectRight = imgWidth - 50
    bonkerRectBottom = bonkerRectTop + iconSize + 5
    bonkerRectWidth = bonkerRectRight - bonkerRectLeft
    bonkerRectHeight = bonkerRectBottom - bonkerRectTop
    #draw boxes
    rectImg = Image.new('RGBA', (imgWidth, imgHeight))
    rectDraw = ImageDraw.Draw(rectImg)
    rectDraw.rectangle((rectLeft, rectTop, rectRight, rectBottom), fill=(255,255,255,125), outline=(0,0,0,255))
    rectDraw.rectangle((bonkedRectLeft, bonkedRectTop, bonkedRectRight, bonkedRectBottom), fill=(255,255,255,125), outline=(0,0,0,255))
    rectDraw.rectangle((bonkerRectLeft, bonkerRectTop, bonkerRectRight, bonkerRectBottom), fill=(255,255,255,125), outline=(0,0,0,255))
    myImage = Image.alpha_composite(myImage, rectImg)

    #set text and font
    drawImg = ImageDraw.Draw(myImage)
    imgText = '%s'%(userName)
    bonkerText = '%i'%(bonkStats[0])
    bonkedText = '%i'%(bonkStats[1])
    fontFile = 'times.ttf'
    try:
        ImageFont.truetype(fontFile, nameSize)
    except:
        fontFile = '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf'
        print('Using backup font')
    imgFont = ImageFont.truetype(fontFile, nameSize)
    numFont = ImageFont.truetype(fontFile, numSize)

    #adjust font size
    while (imgFont.getsize(imgText)[0] < (rectWidth - avatarSize - 100)) and (imgFont.getsize(imgText)[1] < (rectHeight - 30)):
        nameSize += 1
        imgFont = ImageFont.truetype(fontFile, nameSize)
    nameSize -= 1
    imgFont = ImageFont.truetype(fontFile, nameSize)
    while (numFont.getsize(bonkerText)[0] < (bonkerRectWidth - iconSize - 20)) and (numFont.getsize(bonkerText)[1] < (bonkerRectHeight * 0.9)):
        numSize += 1
        numFont = ImageFont.truetype(fontFile, numSize)
    numSize -= 1
    numFont = ImageFont.truetype(fontFile, numSize)

    #set text position and place text
    imgText_width, imgText_height = drawImg.textsize(imgText, font=imgFont)
    textX = (rectWidth - imgText_width + avatarSize)//2 + rectLeft
    textY = (rectHeight - imgText_height)//2 + rectTop
    drawImg.text( (textX, textY), imgText, fill=(255,255,255), font=imgFont, stroke_width=2, stroke_fill=(0,0,0))

    bonkerText_width, bonkerText_height = drawImg.textsize(bonkerText, font=numFont)
    bonkerTextX = (bonkerRectWidth - bonkerText_width + iconSize)//2 + bonkerRectLeft
    bonkerTextY = bonkerRectTop - bonkerText_height//10
    drawImg.text( (bonkerTextX, bonkerTextY), bonkerText, fill=(255,255,255), font=numFont, stroke_width=2, stroke_fill=(0,0,0))

    bonkedText_width, bonkedText_height = drawImg.textsize(bonkedText, font=numFont)
    bonkedTextX = (bonkedRectWidth - bonkedText_width + iconSize)//2 + bonkedRectLeft
    bonkedTextY = bonkedRectTop - bonkedText_height//10
    drawImg.text( (bonkedTextX, bonkedTextY), bonkedText, fill=(255,255,255), font=numFont, stroke_width=2, stroke_fill=(0,0,0))

    return myImage

def getEmojis(server, isAnimated: bool):
    emojis = [str(x) for x in server.emojis]
    final = []
    if emojis == None:
        print("Emojis unavailable")
        return None
    for a in emojis:
        if isAnimated:
            if '<a:' in a:
                final.append(a)
        else:
            if '<a:' not in a:
                final.append(a)
    return final

def cvtTime(UTCTime):
    HSTTime = UTCTime.astimezone(pytz.timezone('US/Hawaii'))
    PSTTime = UTCTime.astimezone(pytz.timezone('America/Los_Angeles'))
    MSTTime = UTCTime.astimezone(pytz.timezone('America/Denver'))
    CSTTime = UTCTime.astimezone(pytz.timezone('America/Chicago'))
    ESTTime = UTCTime.astimezone(pytz.timezone('America/New_York'))
    return [HSTTime, PSTTime, MSTTime, CSTTime, ESTTime]

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
                await ctx.send(file=discord.File(data, 'img%s'%(imglink[imglink.find(".",imglink.find(".com")+1):])))

async def sendSinglePic(ctx, imglink, embed = None):
    async with aiohttp.ClientSession() as session:
        async with session.get(imglink) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            return await ctx.send(file=discord.File(data, 'img%s'%(imglink[imglink.find(".",imglink.find(".com")+1):])), embed = embed)

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

async def setAvatarnIcon(member, myImage):
    avatarSize = 128
    iconSize = 70
    imgWidth, imgHeight = myImage.size

    bonkedImg = bonkedImage.resize((iconSize,iconSize))
    bonkerImg = bonkerImage.resize((iconSize,iconSize))

    #name box
    rectLeft = 50
    rectTop = 30
    rectRight = imgWidth - 50
    rectBottom = rectTop + avatarSize + 5
    rectWidth = rectRight - rectLeft
    rectHeight = rectBottom - rectTop
    #other boxes
    bonkedRectLeft = rectLeft
    bonkedRectTop = rectBottom + 10
    bonkerRectLeft = imgWidth // 2 + 5
    bonkerRectTop = rectBottom + 10

    #get user avatar image
    avatarAsset = member.avatar_url_as(format='png', size=256)
    bufferAvatar = io.BytesIO(await avatarAsset.read())
    avatarImage = Image.open(bufferAvatar)
    avatarImage = avatarImage.resize((avatarSize,avatarSize))
    #make circle mask
    circleAvatar = Image.new('L', (avatarSize, avatarSize))
    circleDraw = ImageDraw.Draw(circleAvatar)
    circleDraw.ellipse((0, 0, avatarSize, avatarSize), fill=255)
    #combine avatar, mask, and spark image
    avatarLayer = Image.new('RGBA', (imgWidth, imgHeight))
    avatarLayer.paste(avatarImage, (rectLeft+2, rectTop+2), circleAvatar)
    avatarLayer.paste(bonkedImg, (bonkedRectLeft+2, bonkedRectTop+2))
    avatarLayer.paste(bonkerImg, (bonkerRectLeft+2, bonkerRectTop+2))
    myImage = Image.alpha_composite(myImage, avatarLayer)

    return myImage

#============== BOT LOOPS =============================
@tasks.loop(seconds=10)
async def downSpam(ctx):
    link = allImages["down"][random.randrange(0,len(downImages))]
    await sendPics(ctx, link, True, downSpam.current_loop)

@tasks.loop(seconds=10)
async def downSpamBot(target_channel):
    link = allImages["down"][random.randrange(0,len(downImages))]
    msgChannel = bot.get_channel(target_channel)
    await sendPics(msgChannel, link, True, downSpamBot.current_loop)

bot.run(TOKEN)

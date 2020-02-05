import requests
import discord
from discord.ext import commands
import asyncio
import json
import time
from plexapi.server import PlexServer
import os
from SynDSapi import *
from cred import *

def filmembed(movietitles,downloaded, imdbs, years, ctx):
    print(type(downloaded))
    i = 0
    embed = discord.Embed(
        description= "",
        color=discord.Color.orange()
        )
    embed.set_author(name="Films Found")
    for download in downloaded:
        if download == False:
            embed.add_field(name=i, value="[{0} ({1})](https://www.imdb.com/title/{2}/)".format(movietitles[i], years[i],imdbs[i]))
        else:
            embed.add_field(name=i, value="[~~{0} ({1})~~](https://www.imdb.com/title/{2}/)".format(movietitles[i], years[i],imdbs[i]))
        i += 1
    embed.set_footer(text=("Requested by {0}").format(ctx.message.author))
    return embed

def chosenfilmebed(movietitle, movieposter, imdb, ctx):
    embed = discord.Embed(
        description= "",
        color=discord.Color.green()
        )
    embed.set_author(name="Film chosen")
    embed.add_field(name="Movie", value=movietitle)
    embed.add_field(name="IMDB", value="[{0}](https://www.imdb.com/title/{0}/)".format(imdb))
    embed.set_thumbnail(url=movieposter)
    embed.set_footer(text=("Requested by {0}").format(ctx.message.author))
    return embed

def check(author):
    def inner_check(message):
        return message.author == author 
    return inner_check

def torrentembed(downloadname, downloadpage, downloadsize, seeders, leechers, movieposters, optionchoosen, ctx):
    embed = discord.Embed(
            description= "A Torrent has been found and added!",
            color=discord.Color.green()
        )
    embed.set_author(name="RARBG-Torrent")
    embed.add_field(name="Name", value=("[{0}]({1}&app_id=rarbgapi)").format(downloadname, downloadpage))
    embed.add_field(name="Size", value="{0} GB".format(downloadsize))
    embed.add_field(name="S/L", value="{0}/{1}".format(seeders, leechers))
    embed.set_thumbnail(url=movieposters[optionchoosen])
    embed.set_footer(text=("Requested by {0}").format(ctx.message.author))
    return embed

def wrongchannelembed(args):
    embed = discord.Embed(
            title ="Wrong Channel",
            description= "Search {0} somewhere else dumbass".format(args),
            colour=discord.Color.red()
        )
    embed.add_field(name="Command", value="Downloading Movies")
    return embed

def updatetorrentembed(downloadname, downloadpage, downloadsize, seeders, leechers, movieposters, optionchoosen, ctx):
    embed = discord.Embed(
            description= "A Torrent has been found and added!",
            color=discord.Color.green()
        )
    embed.set_author(name="RARBG-Torrent")
    embed.add_field(name="Name", value=("[{0}]({1}&app_id=rarbgapi)").format(downloadname, downloadpage))
    embed.add_field(name="Size", value="{0} GB".format(downloadsize))
    embed.add_field(name="S/L", value="{0}/{1}".format(seeders, leechers))
    embed.add_field(name="Time left", value="{0}".format())
    embed.set_thumbnail(url=movieposters[optionchoosen])
    embed.set_footer(text=("Requested by {0}").format(ctx.message.author))
    return embed

async def update(messageid, magnetlink, ctx):
    status = 'downloading'
    firstTime = True
    while status == 'downloading':
        status, downloadSpeed, synologyDownloaded, size, seeders, leechers  = checkDownload(magnetlink)

        if size < 2:
            size = 2
        if synologyDownloaded < 1:
            synologyDownloaded = 1
        if downloadSpeed < 1:
            downloadSpeed = 1


        downloadTime = (size-synologyDownloaded)/downloadSpeed/60
        downloadTimeMin = int(downloadTime)
        downloadTimeSec = int((downloadTime -int(downloadTime)) * 60)

        synologyDownloadedGB = round(synologyDownloaded/1000000000, 2)
        downloadSpeedMB = round(downloadSpeed/1000000, 2)

        size = round((size/1000000000), 3)

        embedmessage = await ctx.fetch_message(messageid)
        embed1 = embedmessage.embeds[0]
        if firstTime:
            embed1.set_field_at(index=1,name=embed1.fields[1].name,value="{0} GB".format(size)) #Size of torrent
            embed1.add_field(name="Already downloaded", value="{0} GB".format(synologyDownloadedGB))
            embed1.add_field(name="Downloadspeed", value="{0} MB/s".format(downloadSpeedMB))
            embed1.add_field(name="Time left", value="{0}min {1}s".format(downloadTimeMin, downloadTimeSec))
            firstTime = False

        embed1.set_field_at(index=1,name=embed1.fields[1].name,value="{0} GB".format(size))
        embed1.set_field_at(index=2,name=embed1.fields[2].name,value="{0}/{1}".format(seeders, leechers))
        embed1.set_field_at(index=3,name=embed1.fields[3].name,value="{0} GB".format(synologyDownloadedGB))
        embed1.set_field_at(index=4,name=embed1.fields[4].name,value="{0} MB/s".format(downloadSpeedMB))
        embed1.set_field_at(index=5,name=embed1.fields[5].name,value="{0}min {1}s".format(downloadTimeMin, downloadTimeSec))
        await embedmessage.edit(embed=embed1)
        await asyncio.sleep(10) # 10 sec
        
    embedmessage = await ctx.fetch_message(messageid)
    embed1 = embedmessage.embeds[0]
    embed1.remove_field(index=2)
    embed1.remove_field(index=2)
    embed1.remove_field(index=2)
    embed1.remove_field(index=2)
    embed1.add_field(name="Tag", value="The Film has been downloaded <@{0}>".format(ctx.message.author.id))
    await embedmessage.edit(embed=embed1)

def seasonsEmbed(seasons, seriestitle, seriesposter, ctx):
    embed = discord.Embed(
        description= seriestitle,
        color=discord.Color.orange()
        )
    embed.set_author(name="Seasons Found")
    for season in seasons:
        embed.add_field(name="Season", value="{0}".format(season))
    
    embed.set_thumbnail(url=seriesposter)
    embed.set_footer(text=("Requested by {0}").format(ctx.message.author))
    return embed

def chosenSeriesEmbed(movietitle, movieposter, imdb, season, episode,  ctx):
    embed = discord.Embed(
            description= "",
            color=discord.Color.green()
        )
    embed.set_author(name="Series and Season chosen")
    embed.add_field(name="Series", value="[{0}](https://www.imdb.com/title/{1}/)".format(movietitle, imdb))
    embed.add_field(name="Season", value=season)
    embed.set_thumbnail(url=movieposter)
    embed.set_footer(text=("Requested by {0}").format(ctx.message.author))
    
    if episode == 0:
        embed.set_author(name="Series and Season chosen")
    else:
        embed.set_author(name="Series, Season and Episode chosen")
        embed.add_field(name="Episode", value=episode)

    return embed

def episodeEmbed(episodes, inPlex, seriestitle, seriesposter, ctx):
    i = 0
    embed = discord.Embed(
        description= seriestitle,
        color=discord.Color.orange()
        )
    embed.set_author(name="Episodes Found")
    print(inPlex)
    if all(x == True for x in inPlex):
        embed.add_field(name="~~Season~~", value="~~0~~")
    else:
        embed.add_field(name="Season", value="0")

    for episode in episodes:
        if inPlex[i]:
            embed.add_field(name="~~Episode~~", value="~~{0}~~".format(episode))
        else:
           embed.add_field(name="Episode", value="{0}".format(episode)) 
        i +=1
        
    embed.set_thumbnail(url=seriesposter)
    embed.set_footer(text=("Requested by {0}").format(ctx.message.author))
    return embed
import requests
import discord
from discord.ext import commands
import asyncio
import json
import time
from SynDSapi import *
from modules import *
import os
testing

client = commands.Bot(command_prefix='!')
@client.command(pass_context = True)
async def dwn(ctx, *args):
    if ctx.message.channel.id == 668218711571955732:
        imdbIDs, movietitles, movieposters, downloaded  = imdbsearch(str(args))
        embed = filmembed(movietitles,downloaded, imdbIDs, ctx) 
        await ctx.send(embed=embed)
        
        option = "empty"
        option = await client.wait_for('message', timeout=30, check=check(ctx.author))
        print(option.content)
        if option == "empty":
            await ctx.send("Time is up. Please start over")
        try:
            optionchoosen = int(option.content)
        except:
            await ctx.send("Please provide a valid Option")
        if optionchoosen <= len(downloaded) and optionchoosen >= 0:
            embed = chosenfilmebed(movietitles[optionchoosen], movieposters[optionchoosen], imdbIDs[optionchoosen], ctx)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Number is not in Range")

        downloadlink, downloadname, downloadsize, downloadcategory, downloadpage, seeders, leechers = getmagnet(imdbIDs[optionchoosen]) 
        if downloadlink == "404 No Movies have been found":
            embed = discord.Embed(
                description= "404 - No Torrent could be found!",
                color=discord.Color.red()
            )
            embed.set_author(name="RARBG-Torrent")
            embed.add_field(name="IMDB-Title", value="Your movie '{0}' isn't on RARBG!".format(movietitles[optionchoosen]))
            embed.set_footer(text=("Requested by {0}").format(ctx.message.author))
            await ctx.send(embed=embed)

        startDownload(downloadlink, downloadcategory)
        embed = torrentembed(downloadname, downloadpage, downloadsize, seeders, leechers, movieposters, optionchoosen, ctx)
        messageid = await ctx.send(embed=embed)
        await asyncio.sleep(10)
        client.loop.create_task(update(messageid, downloadlink, ctx))

    else:
        print("Wrong channel")
        embed = wrongchannelembed(args)
        await ctx.send(embed=embed)


@client.command(pass_context = True)
async def GetInfo(ctx):
    if ctx.message.channel.id == 668218711571955732:
        DSinfos = getDSinfo()
        embed = discord.Embed(
                description= "Info about currently downloading torrents.",
                color=discord.Color.blue()
            )
        embed.set_author(name="Download Station Infos")
        for downloads in DSinfos.items():
            embed.add_field(name="Title", value=("{0}".format(downloads[0][0])))

        embed.set_footer(text=("Requested by {0}").format(ctx.message.author))
        await ctx.send(embed=embed)


@client.command(pass_context= True)
async def Chg(ctx, arg):
    #embedmessage = await client.get_message(668218711571955732, arg)
    embedmessage = await ctx.fetch_message(arg)
    embed1 = embedmessage.embeds[0]
    #embed1.add_field(name=embed1.fields[3].name, value=embed1.fields[3].value)
    embed1.set_field_at(index=3,name=embed1.fields[3].name,value="600")
    await ctx.send(embed=embed1)


client.run('NjMwNDg1MjY2NjM2OTk2NjA5.XiOElQ.pmtdhLDgKCuaAsA3KGMTKY-YDGc')
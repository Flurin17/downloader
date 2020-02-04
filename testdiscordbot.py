import requests
import discord
from discord.ext import commands
import asyncio
import json
import time
from SynDSapi import *
from modules import *
import os

client = commands.Bot(command_prefix='!')
@client.command(pass_context = True)
async def dwn(ctx, *args):
    if ctx.message.channel.id == 668218711571955732:
        args = ' '.join(args)   
        imdbIDs, movietitles, movieposters, downloaded, years  = imdbsearch(str(args))
        embed = filmembed(movietitles,downloaded, imdbIDs, years, ctx) 
        await ctx.send(embed=embed)
        
        try:
            option = await client.wait_for('message', timeout=45, check=check(ctx.author))
        except asyncio.TimeoutError:
            await ctx.send("Time is up. Please start over")
            return

        if "!dwn" in option.content:
            return

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
        message = await ctx.send(embed=embed)
        await asyncio.sleep(10)
        client.loop.create_task(update(message.id, downloadlink, ctx))

    else:
        print("Wrong channel")
        embed = wrongchannelembed(args)
        await ctx.send(embed=embed)


client.run('NjMwNDg1MjY2NjM2OTk2NjA5.XiOElQ.pmtdhLDgKCuaAsA3KGMTKY-YDGc')
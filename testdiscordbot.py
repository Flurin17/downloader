import requests
import discord
from discord.ext import commands
import asyncio
import json
import time
from SynDSapi import *
from modules import *
from embeds import *
from cred import *
import os

client = commands.Bot(command_prefix='!')
@client.command(pass_context = True)
async def movie(ctx, *args):
    args = ' '.join(args)
    messages = []
    messages.append(ctx.message) 
    if ctx.message.channel.id == discordChannelId:
        output = imdbsearch(str(args))
        if type(output) is tuple and output[3] != []: 
            imdbIDs, movietitles, movieposters, downloaded, years  = output
            embed = filmembed(movietitles,downloaded, imdbIDs, years, ctx) 
            messages.append(await ctx.send(embed=embed))
        
        else:
            messages.append(await ctx.send("Something has gone wrong. Start over"))
            await deleteMessages(messages)
            return

        try:
            option = await client.wait_for('message', timeout=45, check=check(ctx.author))
            messages.append(option)
        except asyncio.TimeoutError:
            messages.append(await ctx.send("Time is up. Please start over"))
            await deleteMessages(messages)
            return
        
        if "!movie" in option.content:
            del messages[-1]
            await deleteMessages(messages)
            return

        try:
            optionchoosen = int(option.content)
        except:
            messages.append(await ctx.send("Please provide a valid Option"))
            await deleteMessages(messages)
            return

        if optionchoosen <= len(downloaded) and optionchoosen >= 0: 
            embed = chosenfilmebed(movietitles[optionchoosen], movieposters[optionchoosen], imdbIDs[optionchoosen], ctx)
            messages.append(await ctx.send(embed=embed))
        else:
            messages.append(await ctx.send("Number is not in Range"))
            await deleteMessages(messages)
            return

        output = getmagnet(imdbIDs[optionchoosen]) 
        if type(output) is tuple:
            downloadlink, downloadname, downloadsize, downloadcategory, downloadpage, seeders, leechers = output
        else:
            embed = rarbgNotFound(movietitles[optionchoosen], ctx)
            await ctx.send(embed=embed)
            await deleteMessages(messages)
            return
        
        embed = torrentembed(downloadname, downloadpage, downloadsize, seeders, leechers, movieposters, optionchoosen, ctx)
        await ctx.send(embed=embed)
        try:
            Worked = startDownload(downloadlink, downloadcategory) 
        except:
            Worked = False

        if Worked:
            print("Start updating torrent embed")
            #client.loop.create_task(update(message.id, downloadlink, ctx))

        else:
            messages.append(ctx.send("Failed to add Torrent to diskstation"))


    else:
        print("Wrong channel")
        embed = wrongchannelembed(args)
        await ctx.send(embed=embed)


@client.command(pass_context = True)
async def show(ctx, *args):
    args = ' '.join(args) 
    messages = []
    messages.append(ctx.message)   
    if ctx.message.channel.id == discordChannelId:
        output = imdbSeriesSearch(str(args))
        print(type(output))
        if type(output) is tuple and output[3] != []: 
            imdbIDs, seriestitles, seriesposters, downloaded, years  = output
            embed = filmembed(seriestitles,downloaded, imdbIDs, years, ctx) 
            messages.append(await ctx.send(embed=embed))
        else:
            messages.append(await ctx.send("Something has gone wrong. Start over"))
            await deleteMessages(messages)
            return
        
        try:
            option = await client.wait_for('message', timeout=45, check=check(ctx.author))
            messages.append(option)
        except asyncio.TimeoutError:
            messages.append(await ctx.send("Time is up. Please start over"))
            await deleteMessages(messages)
            return

        if "!show" in option.content:
            del messages[-1]
            await deleteMessages(messages)
            return

        try:
            optionchoosen = int(option.content)
        except:
            messages.append(await ctx.send("Please provide a valid Option"))
        if optionchoosen <= len(downloaded) and optionchoosen >= 0:
            output = imdbSeriesSearchSeason(imdbIDs[optionchoosen])
            if type(output) is tuple:
                seasons, jsonseries = output
                embed = seasonsEmbed(seasons, seriestitles[optionchoosen], seriesposters[optionchoosen], ctx)
                message = await ctx.send(embed=embed)
                messages.append(message)
            else:
                messages.append(await ctx.send("Something has gone wrong. Start over"))
                await deleteMessages(messages)
                return

        else:
            messages.append(await ctx.send("Number is not in Range. Start over"))
            await deleteMessages(messages)
            return


        try:
            option = await client.wait_for('message', timeout=45, check=check(ctx.author))
            messages.append(option)
        except asyncio.TimeoutError:
            messages.append(await ctx.send("Time is up. Please start over"))
            await deleteMessages(messages)
            return

        if "!show" in option.content:
            del messages[-1]
            await deleteMessages(messages)
            return

        try:
            optionchoosenSeries = int(option.content)
        except:
            messages.append(await ctx.send("Please provide a valid Option"))
        if optionchoosenSeries <= len(seasons) and optionchoosenSeries >= 1:
            optionchoosenSeries = optionchoosenSeries - 1

            episodes, inPlex = checkEpisodes(jsonseries ,seasons[optionchoosenSeries], imdbIDs[optionchoosen], seriestitles[optionchoosen])
            embed = episodeEmbed(episodes, inPlex, seriestitles[optionchoosen], seriesposters[optionchoosen], imdbIDs[optionchoosen], seasons[optionchoosenSeries],   ctx)
            messages.append(await ctx.send(embed=embed))
        else:
            messages.append(await ctx.send("Number is not in Range. Start over"))
            await deleteMessages(messages)
            return
        
        try:
            option = await client.wait_for('message', timeout=45, check=check(ctx.author))
            messages.append(option)
        except asyncio.TimeoutError:
            messages.append(await ctx.send("Time is up. Please start over"))
            await deleteMessages(messages)
            return

        if "!show" in option.content:
            del messages[-1]
            await deleteMessages(messages)
            return
        try:
            optionchoosenEpisode = int(option.content)
        except:
            messages.append(await ctx.send("Please provide a valid Option"))
            await deleteMessages(messages)
            return

        if optionchoosenEpisode <= len(episodes) and optionchoosenEpisode >= 0:
            embed = chosenSeriesEmbed(seriestitles[optionchoosen], seriesposters[optionchoosen], imdbIDs[optionchoosen], seasons[optionchoosenSeries], optionchoosenEpisode, ctx)
            await ctx.send(embed=embed)
        else:
            messages.append(await ctx.send("Number is not in Range. Start over"))
            await deleteMessages(messages)
            return

        output = downloadShow(imdbIDs[optionchoosen], seasons[optionchoosenSeries], optionchoosenEpisode, seriestitles[optionchoosen])
        if type(output) is tuple:
            downloadlink, downloadname, downloadsize, downloadcategory, downloadpage, seeders, leechers = output
        else:
            embed = rarbgNotFound(seriestitles[optionchoosen], ctx)
            await ctx.send(embed=embed)
            await deleteMessages(messages)
            return

        embed = torrentembed(downloadname, downloadpage, downloadsize, seeders, leechers, seriesposters, optionchoosen, ctx)
        await ctx.send(embed=embed)
        await deleteMessages(messages)
        try:
            Worked = startDownload(downloadlink, downloadcategory) #Just for testing put it over embed again
        except:
            Worked = False

        if Worked == True:
            print("Start updating torrent embed")
            #client.loop.create_task(update(message.id, downloadlink, ctx))
        else:
            messages.append(ctx.send("Failed to add Torrent to diskstation"))

    else:
        print("Wrong channel")
        embed = wrongchannelembed(args)
        await ctx.send(embed=embed)

client.run(discordBotToken)
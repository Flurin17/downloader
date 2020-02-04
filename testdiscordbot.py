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
    if ctx.message.channel.id == discordChannelId:
        imdbIDs, movietitles, movieposters, downloaded, years  = imdbsearch(str(args))
        embed = filmembed(movietitles,downloaded, imdbIDs, years, ctx) 
        await ctx.send(embed=embed)
        
        try:
            option = await client.wait_for('message', timeout=45, check=check(ctx.author))
        except asyncio.TimeoutError:
            await ctx.send("Time is up. Please start over")
            return

        if "!movie" in option.content:
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
        #startDownload(downloadlink, downloadcategory) 
        embed = torrentembed(downloadname, downloadpage, downloadsize, seeders, leechers, movieposters, optionchoosen, ctx)
        message = await ctx.send(embed=embed)

        #await asyncio.sleep(10)
        #client.loop.create_task(update(message.id, downloadlink, ctx))

    else:
        print("Wrong channel")
        embed = wrongchannelembed(args)
        await ctx.send(embed=embed)

@client.command(pass_context = True)
async def season(ctx, *args):
    args = ' '.join(args)   
    if ctx.message.channel.id == discordChannelId:
        imdbIDs, seriestitles, seriesposters, downloaded, years  = imdbSeriesSearch(str(args))
        embed = filmembed(seriestitles,downloaded, imdbIDs, years, ctx) 
        await ctx.send(embed=embed)
        
        try:
            option = await client.wait_for('message', timeout=45, check=check(ctx.author))
        except asyncio.TimeoutError:
            await ctx.send("Time is up. Please start over")
            return

        if "!season" in option.content:
            return

        try:
            optionchoosen = int(option.content)
        except:
            await ctx.send("Please provide a valid Option")
        if optionchoosen <= len(downloaded) and optionchoosen >= 0:
            print("all good")
        else:
            await ctx.send("Number is not in Range. Start over")
            return

        seasons, jsonseries = imdbSeriesSearchSeason(imdbIDs[optionchoosen])

        embed = seasonsEmbed(seasons, seriestitles[optionchoosen], seriesposters[optionchoosen], ctx)
        await ctx.send(embed=embed)

        try:
            option = await client.wait_for('message', timeout=45, check=check(ctx.author))
        except asyncio.TimeoutError:
            await ctx.send("Time is up. Please start over")
            return

        if "!season" in option.content:
            return

        try:
            optionchoosenSeries = int(option.content)
        except:
            await ctx.send("Please provide a valid Option")
        if optionchoosenSeries <= len(seasons) and optionchoosenSeries >= 1:
            optionchoosenSeries = optionchoosenSeries -1
            embed = chosenSeriesEmbed(seriestitles[optionchoosen], seriesposters[optionchoosen], imdbIDs[optionchoosen], seasons[optionchoosenSeries], ctx)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Number is not in Range. Start over")
            return
        
        downloadlink, downloadname, downloadsize, downloadcategory, downloadpage, seeders, leechers = getSeries(imdbIDs[optionchoosen], seasons[optionchoosenSeries]) 
        if downloadlink == "404 No  have been found":
            embed = discord.Embed(
                description= "404 - No Torrent could be found!",
                color=discord.Color.red()
            )
            embed.set_author(name="RARBG-Torrent")
            embed.add_field(name="IMDB-Title", value="Your Season '{0}' isn't on RARBG!".format(seriestitles[optionchoosen]))
            embed.set_footer(text=("Requested by {0}").format(ctx.message.author))
            await ctx.send(embed=embed)

        embed = torrentembed(downloadname, downloadpage, downloadsize, seeders, leechers, seriesposters, optionchoosen, ctx)
        message = await ctx.send(embed=embed)
        
        #startDownload(downloadlink, downloadcategory) #Just for testing put it over embed again
        #await asyncio.sleep(10)
        #client.loop.create_task(update(message.id, downloadlink, ctx))

    else:
        print("Wrong channel")
        embed = wrongchannelembed(args)
        await ctx.send(embed=embed)

@client.command(pass_context = True)
async def episode(ctx, *args):
    args = ' '.join(args)   
    if ctx.message.channel.id == discordChannelId:
        imdbIDs, seriestitles, seriesposters, downloaded, years  = imdbSeriesSearch(str(args))

        embed = filmembed(seriestitles,downloaded, imdbIDs, years, ctx) 
        await ctx.send(embed=embed)
        


        try:
            option = await client.wait_for('message', timeout=45, check=check(ctx.author))
        except asyncio.TimeoutError:
            await ctx.send("Time is up. Please start over")
            return

        if "!episode" in option.content:
            return

        try:
            optionchoosen = int(option.content)
        except:
            await ctx.send("Please provide a valid Option")
        if optionchoosen <= len(downloaded) and optionchoosen >= 0:
            print("all good")
            seasons, jsonseries = imdbSeriesSearchSeason(imdbIDs[optionchoosen])

            embed = seasonsEmbed(seasons, seriestitles[optionchoosen], seriesposters[optionchoosen], ctx)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Number is not in Range. Start over")
            return


        try:
            option = await client.wait_for('message', timeout=45, check=check(ctx.author))
        except asyncio.TimeoutError:
            await ctx.send("Time is up. Please start over")
            return

        if "!episode" in option.content:
            return

        try:
            optionchoosenSeries = int(option.content)
        except:
            await ctx.send("Please provide a valid Option")
        if optionchoosenSeries <= len(seasons) and optionchoosenSeries >= 1:
            optionchoosenSeries = optionchoosenSeries - 1
            episodes = checkEpisodes(jsonseries ,seasons[optionchoosenSeries])
            embed = episodeEmbed(episodes, seriestitles[optionchoosen], seriesposters[optionchoosen], ctx)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Number is not in Range. Start over")
            return
        
        try:
            option = await client.wait_for('message', timeout=45, check=check(ctx.author))
        except asyncio.TimeoutError:
            await ctx.send("Time is up. Please start over")
            return

        if "!episode" in option.content:
            return
        try:
            optionchoosenEpisode = int(option.content)
        except:
            await ctx.send("Please provide a valid Option")
        if optionchoosenEpisode <= len(episodes) and optionchoosenEpisode >= 1:
            optionchoosenEpisode = optionchoosenEpisode - 1 
        else:
            await ctx.send("Number is not in Range. Start over")
            return



        downloadlink, downloadname, downloadsize, downloadcategory, downloadpage, seeders, leechers = getEpisode(imdbIDs[optionchoosen], seasons[optionchoosenSeries], episodes[optionchoosenEpisode], seriestitles[optionchoosen]) 
        if downloadlink == "404 No  have been found":
            embed = discord.Embed(
                description= "404 - No Torrent could be found!",
                color=discord.Color.red()
            )
            embed.set_author(name="RARBG-Torrent")
            embed.add_field(name="IMDB-Title", value="Your Season '{0}' isn't on RARBG!".format(seriestitles[optionchoosen]))
            embed.set_footer(text=("Requested by {0}").format(ctx.message.author))
            await ctx.send(embed=embed) # Fix this errorhandling

        embed = torrentembed(downloadname, downloadpage, downloadsize, seeders, leechers, seriesposters, optionchoosen, ctx)
        message = await ctx.send(embed=embed)
        
        #startDownload(downloadlink, downloadcategory) #Just for testing put it over embed again
        #await asyncio.sleep(10)
        #client.loop.create_task(update(message.id, downloadlink, ctx))

    else:
        print("Wrong channel")
        embed = wrongchannelembed(args)
        await ctx.send(embed=embed)

client.run(discordBotToken)
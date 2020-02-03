import requests
import discord
from discord.ext import commands
import asyncio
import json
import time
from plexapi.server import PlexServer
import os
from SynDSapi import * 

def imdbsearch(movie):
    url = "https://imdb8.p.rapidapi.com/title/find"
    querystring = {"q":"{0}".format(movie)}
    baseurl = 'http://192.168.0.10:32400'
    token = 'jvpX1PCPamD8fuQ-XV6D'
    plex = PlexServer(baseurl, token)
    movies = plex.library.section('Kinofilme')
    filmeplex = []
    for video in movies.search():
        filmeplex.append(video.guid)
    downloaded = []
    imdbIDs =[]
    movietitles = []
    movieposters =  []
    years = []
    headers = {
        'x-rapidapi-host': "imdb8.p.rapidapi.com",
        'x-rapidapi-key': "fafc5b8916msh957f0d1eee88e85p13674bjsn85b23f581d9c"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)

    jsonmovie = json.loads(response.text)
    results = jsonmovie["results"]
    for result in results:
        try:
            if result["titleType"] == "movie":
                print("Movie found")
                imdbID = result["id"].replace("/title/",'')
                imdbID = imdbID.replace("/",'')
                imdbIDs.append(imdbID)
                imdbIDplexurl = "com.plexapp.agents.imdb://{0}?lang=en".format(imdbID)
                years.appen(result["year"])
                movietitles.append(result["title"])
                movieposters.append(result["image"]["url"])
                if imdbIDplexurl in filmeplex:
                    print("Film is on Plex")
                    downloaded.append("True")
                else:
                    downloaded.append("False")
        except:
            print("This Result is not a movie")
    print(imdbIDs)
    print(movietitles)
    print(movieposters)
    print(downloaded)
    return imdbIDs, movietitles, movieposters, downloaded, years

def getmagnet(imdbID):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    session = requests.Session()
    torrentapi = "https://torrentapi.org/pubapi_v2.php?get_token=get_token&app_id=rarbgapi"
    scores =[]
    notworked = True
    count = 0
    print(imdbID)


    token = session.get(torrentapi, headers=agent).text
    token = json.loads(token)
    token = token["token"]
    print(token)
    time.sleep(2.1)
    searchurl = "https://torrentapi.org/pubapi_v2.php?mode=search&search_imdb={0}&sort=seeders&category=44&format=json_extended&token={1}&app_id=rarbgapi".format(imdbID, token)

    while notworked and count < 5:
        searchurlresponse = session.get(searchurl, headers=agent)
        print(searchurl)
        searchurljson = json.loads(searchurlresponse.text)
        try:
            downloadlinks = searchurljson["torrent_results"]
            notworked = False
            print("Movies have been found")
        except:
            time.sleep(2.1)
            count += 1 
    if notworked:
        return "404 No Movies have been found"

    for torrent in downloadlinks:
        downloadsize = torrent["size"]
        if int(downloadsize) > 2000000000 and int(downloadsize) < 30000000000:
            seeders = torrent["seeders"]
            leechers = torrent["leechers"]
            print(downloadsize)
            print(torrent["title"])
            if int(leechers) == 0:
                leechers = 1
            score = int(seeders)/int(leechers)

            score = int(seeders) + int(score)
            if "BluRay" in torrent["title"]:
                score = int(score) * 2 
            score = int(round(int(torrent["size"])/1000000000,3)) * 3 + score
            scores.append(int(score))
        else:
            score = 0.0
    print(scores)
    if scores == []:
        print("No good copies have been found Choosing first one")
        position = 0

    else:
        print("Best copy will be choosen")
        position =  scores.index(max(scores))
    print(position)

    downloadlink = downloadlinks[position]["download"]
    downloadname = downloadlinks[position]["title"]
    downloadcategory = downloadlinks[position]["category"]
    seeders = downloadlinks[position]["seeders"]
    leechers = downloadlinks[position]["leechers"]
    downloadsize =  str(round((downloadlinks[position]["size"]/1000000000),2))
    downloadpage = downloadlinks[position]["info_page"]
    print(downloadname)

    return downloadlink, downloadname, downloadsize, downloadcategory, downloadpage, seeders, leechers

def getmagnetseries(imdbID):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    session = requests.Session()
    torrentapi = "https://torrentapi.org/pubapi_v2.php?get_token=get_token&app_id=rarbgapi"
    scores =[]
    notworked = True
    count = 0
    print(imdbID)

    token = session.get(torrentapi, headers=agent).text
    token = json.loads(token)
    token = token["token"]
    print(token)
    time.sleep(2.1)
    searchurl = "https://torrentapi.org/pubapi_v2.php?mode=search&search_imdb={0}&sort=seeders&category=41&format=json_extended&token={1}&app_id=rarbgapi".format(imdbID, token)

    while notworked and count < 5:
        searchurlresponse = session.get(searchurl, headers=agent)
        print(searchurl)
        searchurljson = json.loads(searchurlresponse.text)
        try:
            downloadlinks = searchurljson["torrent_results"]
            notworked = False
            print("Movies have been found")
        except:
            time.sleep(2.1)
            count += 1 
    if notworked:
        return "404 No Movies have been found"
    

def checkplex(imdbID):
    baseurl = 'http://192.168.0.10:32400'
    token = 'jvpX1PCPamD8fuQ-XV6D'
    plex = PlexServer(baseurl, token)
    movies = plex.library.section('Kinofilme')

    alreadydown = False
    for video in movies.search():
        imdbplexurl = video.guid
        if imdbID in imdbplexurl:
            print("Film is on Plex")
            alreadydown = True
    return alreadydown

def filmembed(movietitles,downloaded, imdbs, ctx):
    print("in Variable")
    print(type(downloaded))
    i = 0
    embed = discord.Embed(
        description= "",
        color=discord.Color.orange()
        )
    embed.set_author(name="Films Found")
    for download in downloaded:
        if download == "False":
            embed.add_field(name=i, value="[{0}](https://www.imdb.com/title/{1}/#downloader)".format(movietitles[i],imdbs[i]))
        else:
            embed.add_field(name=i, value="[~~{0}~~](https://www.imdb.com/title/{1}/#downloader)".format(movietitles[i],imdbs[i]))
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
    embed.add_field(name="IMDB", value="[{0}](https://www.imdb.com/title/{0}/#downloader)".format(imdb))
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
    embed.add_field(name="!dwn", value="Downloading Movies")
    return embed


async def update(messageid, magnetlink, ctx):
    status = 'downloading'
    firstTime = True
    while status == 'downloading':
        status, downloadSpeed, synologyDownloaded, size, seeders, leechers  = checkDownload(magnetlink)
        if size < 2:
            size = 2
        if synologyDownloaded <1:
            synologyDownloaded = 1
        if downloadSpeed < 1:
            downloadSpeed = 1
        size = round((size/1000000000), 3)

        downloadTime = (size-synologyDownloaded)/downloadSpeed/60
        downloadTimeMin = int(downloadTime)
        downloadTimeSec = (downloadTime -int(downloadTime)) * 60

        synologyDownloadedGB = round(synologyDownloaded/1000000000, 2)
        downloadSpeedMB = round(downloadSpeed/1000000, 2)

        embedmessage = await ctx.fetch_message(messageid)
        embed1 = embedmessage.embeds[0]
        if firstTime:
            embed1.set_field_at(index=1,name=embed1.fields[1].name,value="{0} GB".format(size)) #Size of torrent
            embed1.add_field(name="Already downloaded", value="{0} GB".format(synologyDownloadedGB))
            embed1.add_field(name="Downloadspeed", value="{0} MB/s".format(downloadSpeedMB))
            embed1.add_field(name="Time left", value="{0} min {1} sec".format(downloadTimeMin, downloadTimeSec))
            firstTime = False
        embed1.set_field_at(index=2,name=embed1.fields[2].name,value="{0}/{1}".format(seeders, leechers))
        embed1.set_field_at(index=3,name=embed1.fields[3].name,value="{0} GB".format(synologyDownloadedGB))
        embed1.set_field_at(index=4,name=embed1.fields[4].name,value="{0} MB/s".format(downloadSpeedMB))
        embed1.set_field_at(index=5,name=embed1.fields[5].name,value="{0} min {1} sec".format(downloadTimeMin, downloadTimeSec))
        await embedmessage.edit(embed=embed1)
        await asyncio.sleep(10) # 10 sec

    embedmessage = await ctx.fetch_message(messageid)
    embed1 = embedmessage.embeds[0]
    embed1.remove_field(index=2)
    embed1.remove_field(index=3)
    embed1.remove_field(index=4)
    embed1.remove_field(index=5)
    embed1.add_field(name="Tag", value="The Film has been downloaded. <@{0}>".format(ctx.message.author.id))
    await embedmessage.edit(embed=embed1)
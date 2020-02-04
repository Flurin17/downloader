import requests
import discord
from discord.ext import commands
import asyncio
import json
import time
from plexapi.server import PlexServer
import os
from SynDSapi import *


def checkplex():
    baseurl = 'https://christian-bosshard.com:32400'
    token = 'jQLssu8zXvdvAJdAg_8v'
    plex = PlexServer(baseurl, token)
    media = plex.library.all()
    filmeplex = []
    for video in media:
        filmeplex.append(video.guid)
    print(filmeplex)
    return filmeplex

def imdbsearch(movie):
    url = "https://imdb8.p.rapidapi.com/title/find"
    querystring = {"q":"{0}".format(movie)}
    filmeplex =checkplex()
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
                years.append(result["year"])
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

def imdbSeriesSearch(imdb):
    url = "https://imdb8.p.rapidapi.com/title/find"
    querystring = {"q":"{0}".format(imdb)}
    filmeplex =checkplex()
    downloaded = []
    imdbIDs =[]
    seriestitles = []
    seriesposters =  []
    years = []
    headers = {
        'x-rapidapi-host': "imdb8.p.rapidapi.com",
        'x-rapidapi-key': "fafc5b8916msh957f0d1eee88e85p13674bjsn85b23f581d9c"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)

    jsonmseries = json.loads(response.text)
    results = jsonmseries["results"]
    for result in results:
        try:
            if result["titleType"] == "tvSeries":
                print("series found")
                imdbID = result["id"].replace("/title/",'')
                imdbID = imdbID.replace("/",'')
                imdbIDs.append(imdbID)
                imdbIDplexurl = "com.plexapp.agents.imdb://{0}?lang=en".format(imdbID)
                years.append(result["year"])
                seriestitles.append(result["title"])
                seriesposters.append(result["image"]["url"])
                if imdbIDplexurl in filmeplex:
                    print("Series is on Plex")
                    downloaded.append("True")
                else:
                    downloaded.append("False")
        except:
            print("This Result is not a series")
    print(imdbIDs)
    print(seriestitles)
    print(seriesposters)
    print(downloaded)
    return imdbIDs, seriestitles, seriesposters, downloaded, years

def imdbSeriesSearchSeason(imdbID):
    seasons = []
    url = "https://imdb8.p.rapidapi.com/title/get-seasons"
    querystring = {"tconst":"{0}".format(imdbID)}

    headers = {
        'x-rapidapi-host': "imdb8.p.rapidapi.com",
        'x-rapidapi-key': "fafc5b8916msh957f0d1eee88e85p13674bjsn85b23f581d9c"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    jsonseries = json.loads(response.text)
    for season in jsonseries:
        seasonnumber = season["season"]
        seasons.append(seasonnumber)
    print(seasons)
    return seasons
def rarbgsearchmovie(imdbID):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    session = requests.Session()
    torrentapi = "https://torrentapi.org/pubapi_v2.php?get_token=get_token&app_id=rarbgapi"
    notworked = True
    count = 0
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
    else:
        return downloadlinks

def rarbgsearchseries(imdbID):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    session = requests.Session()
    torrentapi = "https://torrentapi.org/pubapi_v2.php?get_token=get_token&app_id=rarbgapi"
    notworked = True
    count = 0
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
    else:
        return downloadlinks

def getmagnet(imdbID):
    scores =[]
    print(imdbID)

    downloadlinks = rarbgsearchmovie(imdbID)
    if downloadlinks == "404 No Movies have been found":
        return
    
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

def getSeries(imdbID, season):
    scores =[]
    print(imdbID)
    print("User has chosen season {0}".format(season))
    downloadlinks = rarbgsearchseries(imdbID)
    if downloadlinks == "404 No Movies have been found":
        return

    for torrent in downloadlinks:
        downloadSize = torrent["size"]
        seeders = torrent["seeders"]
        seriesTitle = torrent["episode_info"]["title"]
        print(seeders)
        print(seriesTitle)
        if "Season Pack {0}".format(season) in seriesTitle :
            scores.append(seeders)
        else:
            scores.append(0)

    position =  scores.index(max(scores))

    downloadlink = downloadlinks[position]["download"]
    downloadname = downloadlinks[position]["title"]
    downloadcategory = downloadlinks[position]["category"]
    seeders = downloadlinks[position]["seeders"]
    leechers = downloadlinks[position]["leechers"]
    downloadsize =  str(round((downloadlinks[position]["size"]/1000000000),2))
    downloadpage = downloadlinks[position]["info_page"]
    print(downloadname)
    print(scores)
    return downloadlink, downloadname, downloadsize, downloadcategory, downloadpage, seeders, leechers

        



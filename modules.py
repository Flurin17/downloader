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
import urllib.parse

def getPlexLibrariesPath():
    baseurl = plexBaseUrl
    token = plexToken
    plex = PlexServer(baseurl, token)
    moviePath = None
    showPath = None
    
    sections = plex.library.sections()
    for section in sections:
        if section.type == "movie":
            moviePath = section.locations
        if section.type == "show":
            showPath = section.locations
    return moviePath, showPath


def searchplexMovie(imdbId):
    baseurl = plexBaseUrl
    token = plexToken
    media = []
    plex = PlexServer(baseurl, token)
    titleurl = "com.plexapp.agents.imdb://{0}?lang=en".format(imdbId)
    media = plex.library.search(guid=titleurl)
    if not media:
        found = False
    else:
        found = True
    print(media)
    return found

def searchPlexName(imdb, season, episodenumber, seriesTitle):
    baseurl = plexBaseUrl
    token = plexToken
    media = []
    season = int(season) + 1
    plex = PlexServer(baseurl, token)
    media = plex.library.search(title=seriesTitle)
    print(media)
    if not media:
        found = False
    else:
        try:
            plexSeason = media[0].episode(title=None,season=int(season), episode=int(episodenumber))
            found = True
        except:
            found = False
    return found

def updateplex():
    baseurl = plexBaseUrl
    token = plexToken
    plex = PlexServer(baseurl, token)
    plex.library.update()

def imdbsearch(movie):
    url = "https://imdb8.p.rapidapi.com/title/find"
    querystring = {"q":"{0}".format(movie)}
    downloaded = []
    imdbIDs = []
    movietitles = []
    movieposters =  []
    years = []
    headers = {
        'x-rapidapi-host': "imdb8.p.rapidapi.com",
        'x-rapidapi-key': rapidApiKey
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
                years.append(result["year"])
                movietitles.append(result["title"])
                movieposters.append(result["image"]["url"])
                downloaded.append(searchplexMovie(imdbID))
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
    downloaded = []
    imdbIDs = []
    seriestitles = []
    seriesposters =  []
    years = []
    headers = {
        'x-rapidapi-host': "imdb8.p.rapidapi.com",
        'x-rapidapi-key': rapidApiKey
        }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=5)
        jsonmseries = json.loads(response.text)
        results = jsonmseries["results"]
    except:
        return "Has not worked"

    for result in results:
        try:
            if result["titleType"] == "tvSeries":
                print("series found")
                imdbID = result["id"].replace("/title/",'')
                imdbID = imdbID.replace("/",'')
                imdbIDs.append(imdbID)
                years.append(result["year"])
                seriestitles.append(result["title"])
                seriesposters.append(result["image"]["url"])
                downloaded.append(searchplexMovie(imdbID))

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
        'x-rapidapi-key': rapidApiKey
        }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        jsonseries = json.loads(response.text)
    except:
        return "Something has went wrong"
    for season in jsonseries:
        try:
            seasonnumber = season["season"]
            seasons.append(seasonnumber)
        except:
            print("error: no season found, maybe special episode")

    print(seasons)
    return seasons, jsonseries
    
def rarbgsearchmovie(imdbID):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    session = requests.Session()
    torrentapi = "https://torrentapi.org/pubapi_v2.php?get_token=get_token&app_id=rarbgapi"
    notworked = True
    count = 0
    token = session.get(torrentapi, headers=agent, timeout=5).text
    token = json.loads(token)
    token = token["token"]
    print(token)
    time.sleep(2.6)
    searchurl = "https://torrentapi.org/pubapi_v2.php?mode=search&search_imdb={0}&search_string=1080p&sort=seeders&limit=100&category=44&format=json_extended&token={1}&app_id=rarbgapi".format(imdbID, token)

    while notworked and count < 5:
        searchurlresponse = session.get(searchurl, headers=agent)
        print(searchurl)
        searchurljson = json.loads(searchurlresponse.text)
        try:
            downloadlinks = searchurljson["torrent_results"]
            notworked = False
            print("Movies have been found")
        except:
            time.sleep(3)
            count += 1 
    if notworked:
        return False
    else:
        return downloadlinks

def rarbgSearchSeries(imdbID, season):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    session = requests.Session()
    torrentapi = "https://torrentapi.org/pubapi_v2.php?get_token=get_token&app_id=rarbgapi"
    notworked = True
    count = 0
    if len(str(season)) == 1:
        season = "0{0}".format(season)
    seasonquery = "S{0}".format(season)
    token = session.get(torrentapi, headers=agent, timeout=5).text
    token = json.loads(token)
    token = token["token"]
    print(token)
    time.sleep(2.1)
    searchurl = "https://torrentapi.org/pubapi_v2.php?mode=search&search_imdb={0}&search_string={1}%1080p&sort=seeders&limit=100&category=41&format=json_extended&token={2}&app_id=rarbgapi".format(imdbID, seasonquery,  token)
    while notworked and count < 5:
        searchurlresponse = session.get(searchurl, headers=agent)
        print(searchurl)
        searchurljson = json.loads(searchurlresponse.text)
        try:
            downloadlinks = searchurljson["torrent_results"]
            notworked = False
            print("Movies have been found")
        except:
            time.sleep(2.3)
            count += 1 
    if notworked:
        return "404 No Movies have been found"
    else:
        return downloadlinks

def rarbgSearchEpisode(seriestitle, season, episode):
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    session = requests.Session()
    torrentapi = "https://torrentapi.org/pubapi_v2.php?get_token=get_token&app_id=rarbgapi"
    notworked = True
    count = 0
    if len(str(episode)) == 1:
        episode = "0{0}".format(episode)
    if len(str(season)) == 1:
        season = "0{0}".format(season)
    seriestitle = seriestitle.replace(' ', '%')  

    searchQuery = "{0}%S{1}E{2}".format(seriestitle, season, episode)
    
    token = session.get(torrentapi, headers=agent, timeout=5).text
    token = json.loads(token)
    token = token["token"]
    print(token)
    time.sleep(2.1)
    searchurl = "https://torrentapi.org/pubapi_v2.php?mode=search&search_string={0}%1080p&sort=seeders&limit=100&category=41&format=json_extended&token={1}&app_id=rarbgapi".format(searchQuery, token)
    while notworked and count < 5:
        searchurlresponse = session.get(searchurl, headers=agent, timeout=5)
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
    if downloadlinks == False:
        return "404 not found"
    
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
        position = scores.index(max(scores))
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
    downloadlinks = rarbgSearchSeries(imdbID, season)
    if downloadlinks == "404 No Movies have been found":
        return False 

    for torrent in downloadlinks:
        try:
            seriesTitle = torrent["episode_info"]["title"]
        except:
            seriesTitle = "torrent has no title attribute"
        print(seriesTitle)
        if "Season Pack {0}".format(season) in seriesTitle:
            seeders = torrent["seeders"]
            scores.append(seeders)
        else:
            scores.append(0)

    position =  scores.index(max(scores))
    if max(scores) <= 0:
        return False
    else:
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
   
def getEpisode(imdbID, season, episode, seriestitle):
    scores =[]
    print(imdbID)
    print("User has chosen season {0} and Epsiode {1}".format(season, episode))
    downloadlinks = rarbgSearchEpisode(seriestitle, season, episode)
    if downloadlinks == "404 No Movies have been found":
        return downloadlinks

    for torrent in downloadlinks:
        downloadSize = torrent["size"]
        seeders = torrent["seeders"]
        seriesTitle = torrent["episode_info"]["title"]
        episodenumtorrent = torrent["episode_info"]["epnum"]
        seasonnumtorrent = torrent["episode_info"]["seasonnum"]
        print(seeders)
        print(seriesTitle)
        if str(episode) in episodenumtorrent and str(season) in seasonnumtorrent:
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

def downloadShow(imdbID, season, episode, seriestitle):
    if episode == 0:
        output = getSeries(imdbID, season)
        if type(output) == tuple:
            downloadlink, downloadname, downloadsize, downloadcategory, downloadpage, seeders, leechers = output
            return output
        else:
            return "not worked"
    else:
        output = getEpisode(imdbID, season, episode, seriestitle)
        if type(output) == tuple:
            downloadlink, downloadname, downloadsize, downloadcategory, downloadpage, seeders, leechers = output
            return output
        else:
            return "not worked"

def checkEpisodes(jsonseries, season, imdb, seriesTitle):
    episodes1 = []
    inPlex = []
    season = season - 1 
    episodesjson = jsonseries[season]["episodes"]
    for episode in episodesjson:
        episodenumber = episode["episode"]
        episodes1.append(episodenumber)
        inPlex.append(searchPlexName(imdb, season,episodenumber, seriesTitle))

    print(episodes1)
    return episodes1, inPlex 

async def deleteMessages(messages):
    await asyncio.sleep(10)
    for message in reversed(messages):
        try:
            await message.delete()
        except:
            print("Message has not been found to be deleted")
    print("All Messages deleted")
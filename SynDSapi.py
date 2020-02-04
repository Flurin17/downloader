import requests as rs
from cred import *
import json


def startDownload(magnetUrl, category):
    username = dsUsername
    password = dsPassword

    baseUrl = dsBaseUrl

    urlInfo = 'https://{0}:5001/webapi/query.cgi?api=SYNO.API.Info&version=1&method=query&query=SYNO.API.Auth,SYNO.DownloadStation.Task'.format(baseUrl)
    urlAuth = 'https://{0}:5001/webapi/auth.cgi?api=SYNO.API.Auth&version=6&method=login&account={1}&passwd={2}&session=DownloadStation&format=cookie'.format(baseUrl,username,password)
    urlDisco = 'https://{0}:5001/webapi/auth.cgi?api=SYNO.API.Auth&version=6&method=logout&session=DownloadStation'.format(baseUrl)

    urlTasks = 'https://{0}:5001/webapi/DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=3&method=list'.format(baseUrl)
    urlCreate = 'https://{0}:5001/webapi/DownloadStation/task.cgi'.format(baseUrl)
    urlResume = 'https://{0}:5001/webapi/DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=3&method=downloading&id='.format(baseUrl)

    if 'Movies' in category:
        dest = 'homes/plex/Movies'
    elif 'TV' in category:
        dest = 'homes/plex/TV Shows'

    data = {
        'api': 'SYNO.DownloadStation.Task',
        'version': '3',
        'method': 'create',
        'uri': magnetUrl,
        'destination': dest
    }

    sess = rs.session()
    auth = sess.get(urlAuth)
    if auth.status_code == 200:
        if json.loads(auth.text)['success'] == True:
            createTask = sess.post(urlCreate, data=data)
            if json.loads(createTask.text)['success'] == True:
                print('Successfully added Torrent')


def checkDownload(magnetlink):
    username = dsUsername
    password = dsPassword

    baseUrl = dsBaseUrl

    urlInfo = 'https://{0}:5001/webapi/query.cgi?api=SYNO.API.Info&version=1&method=query&query=SYNO.API.Auth,SYNO.DownloadStation.Task'.format(baseUrl)
    urlAuth = 'https://{0}:5001/webapi/auth.cgi?api=SYNO.API.Auth&version=6&method=login&account={1}&passwd={2}&session=DownloadStation&format=cookie'.format(baseUrl,username,password)
    urlDisco = 'https://{0}:5001/webapi/auth.cgi?api=SYNO.API.Auth&version=6&method=logout&session=DownloadStation'.format(baseUrl)
    urlTasks = 'https://{0}:5001/webapi/DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=3&method=list&additional=detail,transfer'.format(baseUrl)

    sess = rs.session()
    auth = sess.get(urlAuth)
    if auth.status_code == 200:
        if json.loads(auth.text)['success'] == True:
            taskList = sess.get(urlTasks)
            if taskList.status_code == 200:
                json.loads(taskList.text)['data']['total']
                for torrent in json.loads(taskList.text)['data']['tasks']:
                    if magnetlink.split('&tr=')[0] == torrent['additional']['detail']['uri'].split('&tr=')[0]:
                        print(torrent['title'])
                        return torrent['status'], torrent['additional']['transfer']['speed_download'], torrent['additional']['transfer']['size_downloaded'], torrent['size'], torrent['additional']['detail']['connected_seeders'], torrent['additional']['detail']['connected_leechers']

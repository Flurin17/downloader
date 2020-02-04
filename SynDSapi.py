import requests as rs
import json



def getDSinfo():
    #with open("C:/Users/cboss/Desktop/PY/creds.json") as json_file:
    #    data = json.load(json_file)
    #    username = data['Users'][0]['username']
    #    password = data['Users'][0]['password']
    username = ""
    password = ""

    urlInfo = 'https://christian-bosshard.com:5001/webapi/query.cgi?api=SYNO.API.Info&version=1&method=query&query=SYNO.API.Auth,SYNO.DownloadStation.Task'
    urlAuth = 'https://christian-bosshard.com:5001/webapi/auth.cgi?api=SYNO.API.Auth&version=6&method=login&account={0}&passwd={1}&session=DownloadStation&format=cookie'.format(username,password)
    urlDisco = 'https://christian-bosshard.com:5001/webapi/auth.cgi?api=SYNO.API.Auth&version=6&method=logout&session=DownloadStation'
    urlTasks = 'https://christian-bosshard.com:5001/webapi/DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=3&method=list&additional=detail'

    downTorrents = {}

    sess = rs.session()
    auth = sess.get(urlAuth)
    if auth.status_code == 200:
        if json.loads(auth.text)['success'] == True:
            taskList = sess.get(urlTasks)
            if taskList.status_code == 200:
                json.loads(taskList.text)['data']['total']
                for torrent in json.loads(taskList.text)['data']['tasks']:
                    print(torrent['additional']['detail']['uri'])
                    #if torrent['status'] == 'downloading':
                    downTorrents[torrent['id']] = { 'title':torrent['title'], 'seeders': torrent['additional']['detail']['connected_seeders'], 'leechers': torrent['additional']['detail']['connected_leechers'] }

                return downTorrents



def startDownload(magnetUrl, category):
    #with open("C:/Users/cboss/Desktop/PY/creds.json") as json_file:
    #    data = json.load(json_file)
    #    username = data['Users'][0]['username']
    #    password = data['Users'][0]['password']
    username = ""
    password = ""

    urlInfo = 'https://christian-bosshard.com:5001/webapi/query.cgi?api=SYNO.API.Info&version=1&method=query&query=SYNO.API.Auth,SYNO.DownloadStation.Task'
    urlAuth = 'https://christian-bosshard.com:5001/webapi/auth.cgi?api=SYNO.API.Auth&version=6&method=login&account={0}&passwd={1}&session=DownloadStation&format=cookie'.format(username,password)
    urlDisco = 'https://christian-bosshard.com:5001/webapi/auth.cgi?api=SYNO.API.Auth&version=6&method=logout&session=DownloadStation'

    urlTasks = 'https://christian-bosshard.com:5001/webapi/DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=3&method=list'
    urlCreate = 'https://christian-bosshard.com:5001/webapi/DownloadStation/task.cgi'
    urlResume = 'https://christian-bosshard.com:5001/webapi/DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=3&method=downloading&id='

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
    username = ""
    password = ""

    urlInfo = 'https://christian-bosshard.com:5001/webapi/query.cgi?api=SYNO.API.Info&version=1&method=query&query=SYNO.API.Auth,SYNO.DownloadStation.Task'
    urlAuth = 'https://christian-bosshard.com:5001/webapi/auth.cgi?api=SYNO.API.Auth&version=6&method=login&account={0}&passwd={1}&session=DownloadStation&format=cookie'.format(username,password)
    urlDisco = 'https://christian-bosshard.com:5001/webapi/auth.cgi?api=SYNO.API.Auth&version=6&method=logout&session=DownloadStation'
    urlTasks = 'https://christian-bosshard.com:5001/webapi/DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=3&method=list&additional=detail,transfer'

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


test = checkDownload('magnet:?xt=urn:btih:06f100df33e1d96fefa27c28b108c78a45d33a00&dn=Inception.2010.1080p.BluRay.H264.AAC-RARBG&tr=http%3A%2F%2Ftracker.trackerfix.com%3A80%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2770&tr=udp%3A%2F%2F9.rarbg.to%3A2750')
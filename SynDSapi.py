import requests as rs
import json



def getDSinfo():
    #with open("C:/Users/cboss/Desktop/PY/creds.json") as json_file:
    #    data = json.load(json_file)
    #    username = data['Users'][0]['username']
    #    password = data['Users'][0]['password']
    username = "admin"
    password = ""

    urlInfo = 'http://192.168.0.10:5000/webapi/query.cgi?api=SYNO.API.Info&version=1&method=query&query=SYNO.API.Auth,SYNO.DownloadStation.Task'
    urlAuth = 'http://192.168.0.10:5000/webapi/auth.cgi?api=SYNO.API.Auth&version=6&method=login&account={0}&passwd={1}&session=DownloadStation&format=cookie'.format(username,password)
    urlDisco = 'http://192.168.0.10:5000/webapi/auth.cgi?api=SYNO.API.Auth&version=6&method=logout&session=DownloadStation'
    urlTasks = 'http://192.168.0.10:5000/webapi/DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=3&method=list&additional=detail'

    downTorrents = {}

    sess = rs.session()
    auth = sess.get(urlAuth)
    if auth.status_code == 200:
        if json.loads(auth.text)['success'] == True:
            taskList = sess.get(urlTasks)
            if taskList.status_code == 200:
                json.loads(taskList.text)['data']['total']
                for torrent in json.loads(taskList.text)['data']['tasks']:
                    #print(torrent['title'])
                    if torrent['status'] == 'downloading':
                        downTorrents[torrent['id']] = { 'title':torrent['title'], 'seeders': torrent['additional']['detail']['connected_seeders'], 'leechers': torrent['additional']['detail']['connected_leechers'] }

                return downTorrents



def startDownload(magnetUrl, category):
    #with open("C:/Users/cboss/Desktop/PY/creds.json") as json_file:
    #    data = json.load(json_file)
    #    username = data['Users'][0]['username']
    #    password = data['Users'][0]['password']
    username = ""
    password = "" 

    urlInfo = 'http://192.168.0.10:5000/webapi/query.cgi?api=SYNO.API.Info&version=1&method=query&query=SYNO.API.Auth,SYNO.DownloadStation.Task'
    urlAuth = 'http://192.168.0.10:5000/webapi/auth.cgi?api=SYNO.API.Auth&version=6&method=login&account={0}&passwd={1}&session=DownloadStation&format=cookie'.format(username,password)
    urlDisco = 'http://192.168.0.10:5000/webapi/auth.cgi?api=SYNO.API.Auth&version=6&method=logout&session=DownloadStation'

    urlTasks = 'http://192.168.0.10:5000/webapi/DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=3&method=list'
    urlCreate = 'http://192.168.0.10:5000/webapi/DownloadStation/task.cgi'
    urlResume = 'http://192.168.0.10:5000/webapi/DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=3&method=downloading&id='

    if 'Movies' in category:
        dest = 'homes/Filme_Fotos_Plex/Kinofilme'
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

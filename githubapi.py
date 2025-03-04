import requests
import json
import datetime
import numpy as np
class Githubapi:
    def __init__(self, api_key):
        self.api_key = api_key

    def define_repo(self, rep):
        headers = {"Authorization": f"token {self.api_key}"}
        try:
            if 'github' in rep:
                if rep.count('/') == 4:
                    return rep[19:]
                elif rep.count('/') == 3:
                    url = 'https://api.github.com/orgs/' + rep[19:] + '/repos'
                    response = requests.get(url, headers=headers)
                    data = response.json()
                    mx = float('-inf')
                    name = ''
                    ch = 0
                    for i in range(len(data)):
                        if data[i]['stargazers_count'] is not None:
                            stars = data[i]['stargazers_count']
                            #print(stars)
                            if stars > mx:
                                mx = stars
                                name = data[i]['name']
                                ch = i
                    if name=='':
                        return np.nan
                    else:
                        url = "https://api.github.com/repos/" + rep[19:] + '/' + name
                        response = requests.get(url, headers=headers)
                        data = response.json()
                        return rep[19:] + '/' + data['name']

        except KeyError :
            print('Что-то пошло не так')
        return None


    def stat(self, rep, st):
        headers = {"Authorization": f"token {self.api_key}"}
        if rep is not None:
            url = "https://api.github.com/repos/"+rep
            response = requests.get(url, headers=headers)
            data = response.json()
            return data.get(st, 'Нет данных')

    def commits(self, rep):
        if not rep:
            return 0

        url = 'https://api.github.com/repos/'+ rep + '/commits'
        headers = {"Authorization": self.api_key}
        days_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=30)).isoformat()
        params = {"since": days_ago}
        response = requests.get(url, headers=headers, params=params)
        comm = response.json()

        return len(comm)















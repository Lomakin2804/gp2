import pandas as pd
from githubapi import Githubapi
import numpy as np
import time


git_key = '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'
df = pd.read_csv('Projects_financials.csv')


# Для начала убираем проекты, у которых нет гитхаба
df = df[df['github'].isna()==False]
df=df.reset_index()
githubs = df['github'].to_list()
print(githubs)
print()
# Итак, мы оцениваем проекты по активности в гитхабе. Однако, после того как мы вытянули ссылки на гитхабы проектов через коинмаркеткэп,
# мы заметили, что некоторые ссылки ведут на конкретный репозиторий, а некоторые ссылки просто на аккаунт в гитхабе. Поэтому для тех проектов
# у которых ссылка ведет на репозиторий, мы будет вытягивать характеристики только для этого репозитория, а для остальных вытянем характеристики для закрепленных репозиториев
# И будем брать по каким-то метрикам среднее значение, а по каким-то метрикам наилучшее

git=Githubapi(git_key)

#df = pd.DataFrame()
#df['repo']=''
#df['description']=''
#df['stargazers_count']=np.nan
#df['subscribers_count']=np.nan
#df['forks'] = np.nan
#df['commits'] = np.nan
ch=0

for i in range(len(githubs)):
    # Создаем колонку с отобранными репозиториями так как у некоторых проектов не указан репозиторий и приходится выбирать самый популярный по звездам
    # Попyлярный репозиторий определяем как раз в функйии define_repo()
    #print(df['repo'])
    if ch!=4000:
        # Выносим в столбец названия репозиториев, которые мы отобрали путем оценки по количеству stars
        df.loc[i, 'repo'] = git.define_repo(githubs[i])
    #print(df['repo'])

    else:
        ch=0
        time.sleep(65)

print(df['repo'].head())
df = df[df['repo']!='None']
print(df['repo'])
repositories = df['repo'].to_list()
for i in range(len(repositories)):
    df.loc[i, 'stargazers_count'] = git.stat(repositories[i], 'stargazers_count')

    # Вытягиваем количество звезд
    df.loc[i,'stargazers_count'] = git.stat(repositories[i], 'stargazers_count')

    # Вытягиваем количество подписчиков
    df.loc[i,'subscribers_count'] = git.stat(repositories[i], 'subscribers_count')

    # Вытягиваем количество форков
    df.loc[i, 'forks'] = git.stat(repositories[i], 'forks')

    #Вытягиваем количество коммитов за 30 дней
    df.loc[i,'commits_per30d'] = git.commits(df.loc[i,'repo'])

df.to_csv("Projects_github_statictics.csv", index=False)

print(df.head(100))









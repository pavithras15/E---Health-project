import pandas as pd


df=pd.read_csv('Google-Playstore.csv')

#####################################################################################################################
# Categories we are interested in: 
# Education, Educational, Puzzle, Strategy

# Education NB: 15 minutes to run just this :/ 1239 elements at this point for rate 3.5 without min installs
education_df=df.loc[df['Category']=='Education']
education_df=education_df.loc[df['Rating']>=3.7]
education_df=education_df.loc[df['Rating Count']>=100000]
education_df=education_df.loc[df['Minimum Installs']>=100]

# Educational
educational_df=df.loc[df['Category']=='Educational']
educational_df=educational_df.loc[df['Rating']>=3.7]
educational_df=educational_df.loc[df['Rating Count']>=100000]
educational_df=educational_df.loc[df['Minimum Installs']>=100]

# Puzzle
puzzle_df=df.loc[df['Category']=='Puzzle']
puzzle_df=puzzle_df.loc[df['Rating']>=3.7]
puzzle_df=puzzle_df.loc[df['Rating Count']>=100000]
puzzle_df=puzzle_df.loc[df['Minimum Installs']>=100]

# Strategy
strategy_df=df.loc[df['Category']=='Strategy']
strategy_df=strategy_df.loc[df['Rating']>=3.7]
strategy_df=strategy_df.loc[df['Rating Count']>=100000]
strategy_df=strategy_df.loc[df['Minimum Installs']>=100]

#####################################################################################################################
#####################################################################################################################

# Creation of the database that will store apps' info
from tinydb import TinyDB
db=TinyDB('./Ourdatabase.json')

###APIs -> json files
from google_play_scraper import app
import json
import  urllib.request
import urllib.parse
from bs4 import BeautifulSoup

#####################################################################################################################
# Loop on education apps
IDs=education_df[["App Id"]]

for i in range(education_df.shape[0]):
    #print(IDs.iloc[i-1,0])

    existing=1
    try:
        response = urllib.request.urlopen("https://play.google.com/store/apps/details?id="+IDs.iloc[i-1,0])
    except urllib.error.HTTPError as exception:
        print(exception)
        existing=0

    if existing==1:
        result = app(IDs.iloc[i-1,0], lang='en', country='us')
        db.insert(result)

#####################################################################################################################
# Loop on educational apps
IDs=educational_df[["App Id"]]

for i in range(educational_df.shape[0]):
    existing=1
    try:
        response = urllib.request.urlopen("https://play.google.com/store/apps/details?id="+IDs.iloc[i-1,0])
    except urllib.error.HTTPError as exception:
        print(exception)
        existing=0

    if existing==1:
        result = app(IDs.iloc[i-1,0], lang='en', country='us')
        db.insert(result)

#####################################################################################################################
# Loop on puzzle apps
IDs=puzzle_df[["App Id"]]

for i in range(puzzle_df.shape[0]):
    existing=1
    try:
        response = urllib.request.urlopen("https://play.google.com/store/apps/details?id="+IDs.iloc[i-1,0])
    except urllib.error.HTTPError as exception:
        print(exception)
        existing=0

    if existing==1:
        result = app(IDs.iloc[i-1,0], lang='en', country='us')
        db.insert(result)

#####################################################################################################################
# Loop on strategy apps
IDs=strategy_df[["App Id"]]

for i in range(strategy_df.shape[0]):

    existing=1
    try:
        response = urllib.request.urlopen("https://play.google.com/store/apps/details?id="+IDs.iloc[i-1,0])
    except urllib.error.HTTPError as exception:
        print(exception)
        existing=0

    if existing==1:
        result = app(IDs.iloc[i-1,0], lang='en', country='us')
        db.insert(result)

#####################################################################################################################
# Once we have the db, we can enrich it with another API: play_scraper
import play_scraper

def ISIN(string, database):
    for item in database:
        if item['appId']==string:
            return(1)
    return(0)

# Print(ISIN("ru.yandex.translate", db)) #returns 1 since it is already in db
# Print(ISIN("com.combo.matcher", db)) # returns 0 since it is not in db 

query="serious game"
answer=play_scraper.search(query)
for item in answer:
    print(item['app_id'])
    if ISIN(item['app_id'],db)==0: #mean the item is not in the db
        result = app(item['app_id'], lang='en', country='us')
        if result['score']>3.5 :
            if result['minInstalls']>100:
                db.insert(result)

query = 'game ADHSD'
answer=play_scraper.search(query)
for item in answer:
    print(item['app_id'])
    if ISIN(item['app_id'],db)==0: #mean the item is not in the db
        result = app(item['app_id'], lang='en', country='us')
        if result['score']>3.5 :
            if result['minInstalls']>100:
                db.insert(result)

query = 'serious game ADHD'
answer=play_scraper.search(query)
for item in answer:
    print(item['app_id'])
    if ISIN(item['app_id'],db)==0: #mean the item is not in the db
        result = app(item['app_id'], lang='en', country='us')
        if result['score']>3.5 :
            if result['minInstalls']>100:
                db.insert(result)

# At this point we updated the db with new apps obtained from specific queries
#####################################################################################################################
# Delete columns (selecting relevant information)

from tinydb.operations import delete
db.update(delete('descriptionHTML'))
db.update(delete('summaryHTML'))
db.update(delete('free'))
db.update(delete('currency'))
db.update(delete('saleTime'))
db.update(delete('originalPrice'))
db.update(delete('saleText'))
db.update(delete('offersIAP'))
db.update(delete('androidVersionText'))
db.update(delete('developerAddress'))
db.update(delete('developerInternalID'))
db.update(delete('icon'))
db.update(delete('headerImage'))
db.update(delete('screenshots'))
db.update(delete('video'))
db.update(delete('recentChangesHTML'))
db.update(delete('videoImage'))

#####################################################################################################################
# First element of the db
db.all()[0]


#####################################################################################################################
# Creating a db of "random" games (fitting some queries) that we will manually score: Serious (1) or Non-Serious (0)
# The automatic db creation prevents repetition

import play_scraper
ref_list=[]

query = 'game for children'
answer=play_scraper.search(query, page=2)
for item in answer:
    print(item['app_id'])
    ref_list.append(item['app_id'])

query='games'
answer=play_scraper.search(query, page=2)
for item in answer:
    print(item['app_id'])
    if ref_list.count(item['app_id'])==0:
        ref_list.append(item['app_id'])

query='game'
answer=play_scraper.search(query, page=2)
for item in answer:
    print(item['app_id'])
    if ref_list.count(item['app_id'])==0:
        ref_list.append(item['app_id'])

query='children games'
answer=play_scraper.search(query, page=2)
for item in answer:
    print(item['app_id'])
    if ref_list.count(item['app_id'])==0:
        ref_list.append(item['app_id'])

query='education games'
answer=play_scraper.search(query, page=2)
for item in answer:
    print(item['app_id'])
    if ref_list.count(item['app_id'])==0:
        ref_list.append(item['app_id'])

len(ref_list)

import pandas as pd    
ref_df = pd.DataFrame(ref_list)
ref_df.to_csv('ref_to_be_labeled.csv', index=False)

#####################################################################################################################
# EVALUATING THE PERFORMANCE OF THE ALGORITHM
import numpy as np

ref=pd.read_excel('156refApps.xlsx') #this is the manually annotated file

# We could have passed the file through the whole code but we realized all the apps were contained in the google play csv file used at the beginning of the code
# So we are just going to check if the apps are returned at the end of the code

# If they are returned, the code says they are positive. 
# Depending on the label we assign to them, they will be either false positive or true positive, since our labelling is supposed to be the gold standard.

ref=ref.assign(AutomaticScore=pd.Series(np.random.randn(156)).values) #creation of a new column in the database for the automatic score

for index, row in ref.iterrows():
    print(row['AppID'])
    if ISIN(row['AppID'], db)==1:
        ref.at[index,'AutomaticScore']=1
    else:
        ref.at[index,'AutomaticScore']=0

# Computing TP, FP, FN, TN
TP_count=0
FP_count=0
TN_count=0
FN_count=0

ref=ref.assign(Class='What') #creation of a new column in the database 

for index, row in ref.iterrows():
    if row['AutomaticScore']==1: #gold standard positive
        if row['Scores']==1:
            ref.at[index,'Class']='TP'
            TP_count=TP_count+1
        else:
            ref.at[index,'Class']='FP'
            FP_count=FP_count+1
    else:
        if row['Scores']==0:
            ref.at[index,'Class']='TN'
            TN_count=TN_count+1
        else:
            ref.at[index,'Class']='FN'
            FN_count=FN_count+1


ref.to_csv('156refApps_results.csv', index=False)

# Sensitivity (True Positive Rate)
Sensitivity=TP_count/(TP_count+FN_count)

# Specificity (True Negative Rate)
Specificity=TN_count/(TN_count+FP_count)

#####################################################################################################################
# END
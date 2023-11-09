import os
import time
import re
import pickle
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

driver = webdriver.Chrome()
df = pd.DataFrame(columns=['URL', 'Video_ID', 'Video_Title', 'Creator', 'Avg_viewers', 'Max_viewers', 'SuperChat_total', 'Stream_Start_Date_UST', 'Stream_Start_Time_UST', 'duration'])

# DURING THIS TIME YOU NEED TO CHANGE THE CURRENCY FROM YEN TO DOLLARS AND TIME TO UST MANUALLY IN THE WEBSITE SETTINGS
driver.get('https://vt.poi.cat/settings')
time.sleep(30)

#year = input('Please enter the year you want to colect')

#holostats = pickle.load(open(f'holostats_URL_2022_REF.pkl','rb'))
#holostats = pickle.load(open(f'\\Pickled data\\holostats_URL_{year}_REF.pkl','rb'))
holostats = pickle.load(open('vstats_URL_2022.pkl','rb'))

data_list = []

for x in range(len(holostats)):

    url = holostats[x]
    driver.get(url)

    temp = []
    temp.append(url)
    time.sleep(5)
    page_sour = driver.page_source
    doc = BeautifulSoup(page_sour, "lxml")

    vid_id = str(url).split('/')
    vid_id = vid_id[-1]
    print(vid_id, end =" ")
    temp.append(vid_id)

    try:
        #title = doc.find('title')
        title = driver.title
        title = str(title)
        #title = title[:-12]
        print(title, end =" ")
        temp.append(title)
    except:
        temp.append(" ")
        continue

    try:
        creator = doc('span', {'class': 'ml-2 align-middle'})[0].text
        print(creator, end =" ")
        temp.append(creator)
    except:
        temp.append(" ")
        continue

    try:
        avg_max_view = doc('div', {'class': 'mat-headline-5 m-0'})[0].text
        avg_max_view = avg_max_view.split('/')

        avg_view = avg_max_view[0]
        avg_view = avg_view[1:-1]
        print(avg_view, end =" ")
        temp.append(avg_view)

        max_view = avg_max_view[1]
        max_view = max_view[1:-1]
        print(max_view, end =" ")
        temp.append(max_view)
    except:
        temp.append(" ")
        temp.append(" ")
        continue

    try:   
        #sup_chat_tot = doc.find_all(text=re.compile("\¥.*"))
        sup_chat_tot = doc.find_all(text=re.compile("\$.*"))
        print(sup_chat_tot, end =" ")
        temp.append(sup_chat_tot[0][3:]) 
    except:
        temp.append(" ")
        continue
        
    try:
        stream_date_time = doc('span', {'class': 'mat-body-1'})[0].text
        date_time_split = stream_date_time.split(' ')
        print(date_time_split[2], end=" ")
        temp.append(date_time_split[1])
        print(date_time_split[2], end=" ")
        temp.append(date_time_split[2])
    except:
        temp.append(" ")
        continue
        
    try:
        duration = doc('span', {'class': 'mat-body-1'})[2].text
        print(duration, end=" ")
        temp.append(duration)
    except:
        temp.append(" ")
        continue
    
    print(" ")
    data_list.append(temp)
    df.loc[len(df)] = temp

#df.to_excel(f'output_{year}.xlsx')
df.to_excel('vstats_2022_RAW.xlsx')
#pickle.dump(df, open(f'holostats_{year}.pkl','wb'))
driver.quit()
#print(doc.prettify())
#title = doc.find_all('span')
#print(title)
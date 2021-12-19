#TODO: Figure out format of email
#TODO: failsafes condition if nothing is pulled 
#TODO: Store p/w info in config file

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pytz
import json
import os
import dictdiffer
from dateutil.parser import parse

#saving the json file
def saving_json(resources_dir, all_challenge_info):
    tz = pytz.timezone('US/Pacific')
    file_name = resources_dir + datetime.now(tz).strftime("%Y_%m_%d-%I_%M_%S_%p") + '.json'
    with open(file_name,'w') as fp: 
        json.dump(all_challenge_info, fp, indent=4)

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def reading_old_files(resources_dir):
    all_old_files = {}
    for file in os.listdir(resources_dir): 
        if file.endswith('.json'): 
            date = str.split(file,'-')[0]
            splits = str.split(date,'_')
            old_date = datetime(int(splits[0]), int(splits[1]),int(splits[2])).strftime("%Y-%m-%d")
            tz = pytz.timezone('US/Pacific')
            date_now = datetime.now(tz).strftime("%Y-%m-%d")
            dist = days_between(date_now, old_date)
            all_old_files[dist] = file 
    return all_old_files

def getting_old_challenges(all_old_files, resources_dir):
    sort_list = sorted(all_old_files.keys())
    newest_file = resources_dir + all_old_files[sort_list[0]]
    f = open(newest_file)
    old_challenges = json.load(f)
    return old_challenges, newest_file


#doing the actual scraping
def scraping_helper():
    option = webdriver.ChromeOptions()
    option.add_argument('--log-level=1')
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-sh-usage')
    driver = webdriver.Chrome('chromedriver.exe', options=option)
    page = driver.get('https://www.challenge.gov/') # Getting page HTML through request
    soup = BeautifulSoup(driver.page_source, 'html.parser') # Parsing content using beautifulsoup
    chall_titles = soup.select("section div.cards div.challenge-tile.card p.challenge-tile__title.test") # Selecting all of the anchors with titles
    chall_agency = soup.select("section div.cards div.challenge-tile.card p.challenge-tile__agency-name") # Selecting all of the anchors with titles
    chall_ref = soup.select("section div.cards div.challenge-tile.card a") # Selecting all of the anchors with titles
    chall_tagline = soup.select("section div.cards div.challenge-tile.card p.challenge-tile__tagline") # Selecting all of the anchors with titles
    chall_date = soup.select("section div.cards div.challenge-tile.card p.challenge-tile__date") # Selecting all of the anchors with titles
    return chall_titles, chall_agency, chall_ref, chall_tagline, chall_date

#scraping and formating info
def scrape_info(printed = False):   
    chall_titles, chall_agency, chall_ref, chall_tagline, chall_date = scraping_helper()
    tot_challenges = len(chall_date)
    challenges= {}
    for i in range(tot_challenges):
        chall_ref[i]['href'] = chall_ref[i]['href'] if chall_ref[i]['href'][0:4] == 'http' else 'https://www.challenge.gov' + chall_ref[i]['href']
        curr_chall_date, open_now = process_date_str(chall_date[i].text)
        challenges['Challenge ' + str(i)] = {'Title':chall_titles[i].text , 'Agency':chall_agency[i].text , 'Reference':chall_ref[i]['href'] , 'Tagline':chall_tagline[i].text, 'Date': curr_chall_date, 'Active': open_now}
    if printed:
        for i in range(tot_challenges):
            print('--------------Challenge #',str(i),'--------------')
            print('Title: ', chall_titles[i].text)
            print('Agency: ', chall_agency[i].text)
            print('Link: ', chall_ref[i]['href'])
            print('Summary: ', chall_tagline[i].text)
            print('Date: ', chall_date[i].text)            
    return challenges

def analyzing_changes(old_challenges,all_challenge_info):
    if old_challenges.__contains__('change_log'): old_challenges.pop('change_log')
    changes_done = {'change':[]}
    for diff in list(dictdiffer.diff(old_challenges, all_challenge_info)):         
        if diff[0] == 'remove':
            changes_done['remove'] = diff[2]
        elif diff[0] == 'add':
            changes_done['add'] = diff[2]
        elif diff[0] == 'change':
            changes_done['change'].append((diff[1], diff[2]))
    return changes_done

def process_date_str(raw_date_str):
    splits = raw_date_str.split()
    date = ''
    active = True if raw_date_str.find('until') != -1 else False # true if the challenge is currently open
    for each in splits:
        if each.find('/') != -1: date = each
    each_date_split = date.split('/')
    date_challenge = datetime(int('20' + each_date_split[2]), int(each_date_split[0]), int(each_date_split[1])).strftime("%Y-%m-%d")
    tz = pytz.timezone('US/Pacific')
    date_now = datetime.now(tz).strftime("%Y-%m-%d")
    ##days_to_challenge_date = days_between(date_challenge, date_now)
    return date_challenge, active


        
if __name__ == '__main__':
    resources_dir = 'resources\\'
    all_challenge_info = scrape_info(printed = False)    
    all_old_files = reading_old_files(resources_dir)
    old_challenges, old_challenge_file = getting_old_challenges(all_old_files, resources_dir)
    changes_found = analyzing_changes(old_challenges,all_challenge_info)
    print('Looking at file: ', old_challenge_file)
    if (len(changes_found.keys()) == 1 and changes_found['change'] == []):
        print('No Change')
    else: 
        print('Saved New List of Challenges')
        all_challenge_info['change_log'] = changes_found
        saving_json(resources_dir, all_challenge_info)
    

    
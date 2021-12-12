#TODO: Fix semi complete lines
#TODO: Figure out the newest challenge 
#TODO: Maybe sort the challenges based on the date they are due

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
def scrape_info(print = False):   
    chall_titles, chall_agency, chall_ref, chall_tagline, chall_date = scraping_helper()
    tot_challenges = len(chall_date)
    if print:
        for i in range(tot_challenges):
            print('--------------Challenge #',str(i),'--------------')
            print('Title: ', chall_titles[i].text)
            print('Agency: ', chall_agency[i].text)
            print('Link: ', 'https://www.challenge.gov' + chall_ref[i]['href'])
            print('Summary: ', chall_tagline[i].text)
            print('Date: ', chall_date[i].text)
    challenges= {}
    for i in range(tot_challenges): challenges['Challenge ' + str(i)] = {'Title':chall_titles[i].text , 'Agency':chall_agency[i].text , 'Reference':chall_ref[i].text , 'Tagline':chall_tagline[i].text , 'Date':chall_date[i].text}
    return challenges

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

if __name__ == '__main__':
    resources_dir = 'resources\\'
    all_challenge_info = scrape_info(print = False)
    all_old_files = reading_old_files(resources_dir)
    old_challenges, old_challenge_file = getting_old_challenges(all_old_files, resources_dir)
    print('Looking at file: ', old_challenge_file)
    print(all_challenge_info == old_challenges)
    if not all_challenge_info == old_challenges:
        print('Saved New List of Challenges')
        saving_json(resources_dir, all_challenge_info)
    else:
        print('Same Challenges')

    
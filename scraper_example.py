import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
 
option = webdriver.ChromeOptions()
option.add_argument('--log-level=1')
# I use the following options as my machine is a window subsystem linux. 
# I recommend to use the headless option at least, out of the 3
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-sh-usage')
# Replace YOUR-PATH-TO-CHROMEDRIVER with your chromedriver location
driver = webdriver.Chrome('chromedriver.exe', options=option)
 
page = driver.get('https://www.imdb.com/chart/top/') # Getting page HTML through request
soup = BeautifulSoup(driver.page_source, 'html.parser') # Parsing content using beautifulsoup
 
totalScrapedInfo = [] # In this list we will save all the information we scrape
links = soup.select("table tbody tr td.titleColumn a") # Selecting all of the anchors with titles
first10 = links[:10] # Keep only the first 10 anchors
for anchor in first10:
    print(anchor)
    driver.get('https://www.imdb.com/' + anchor['href']) # Access the movie’s page 
    infolist = driver.find_elements_by_css_selector('.ipc-inline-list')[0] # Find the first element with class ‘ipc-inline-list’
    informations = infolist.find_elements_by_css_selector("[role='presentation']") # Find all elements with role=’presentation’ from the first element with class ‘ipc-inline-list’
    scrapedInfo = {
        "title": anchor.text,
        "year": informations[0].text,
        "duration": informations[2].text,
    } # Save all the scraped information in a dictionary
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='firstListCardGroup-editorial']")))  # We are waiting for 5 seconds for our element with the attribute data-testid set as `firstListCardGroup-editorial`
    listElements = driver.find_elements_by_css_selector("[data-testid='firstListCardGroup-editorial'] .listName") # Extracting the editorial lists elements
    listNames = [] # Creating an empty list and then appending only the elements texts
    for el in listElements:
        listNames.append(el.text)
    scrapedInfo['editorial-list'] = listNames # Adding the editorial list names to our scrapedInfo dictionary
    totalScrapedInfo.append(scrapedInfo) # Append the dictionary to the totalScrapedInformation list
    
#print(totalScrapedInfo) # Display the list with all the information we scraped
#print(type(totalScrapedInfo))
"""
page = requests.get('https://www.challenge.gov/') # Getting page HTML through request
soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup
print(soup)
spans = soup.find_all('div', {'class' : 'challenge-tile card'})
print(spans)
"""
#print(len(spans))
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import os 
import requests
from random import randint
import re
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options

def google_scraper(DANCE_TYPE,CITY):
    
    chromedriver_autoinstaller.install()
    chrome_options = Options()
    # chrome_options.add_argument(f"user-data-dir={os.path.join(os.getcwd(),'Selenium')}") 
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"+"AppleWebKit/537.36 (KHTML, like Gecko)"+"Chrome/87.0.4280.141 Safari/537.36")

    google_events_data = []
    driver = webdriver.Chrome(options=chrome_options)
    # driver.get(f'https://www.google.com/search?q={DANCE_TYPE}+{CITY}+events&ibp=htl;events')
    driver.get(f'https://www.google.com/search?q={DANCE_TYPE}+{CITY}+events&oq=salsa+paris+events&aqs=chrome..69i57.3875j0j1&sourceid=chrome&ie=UTF-8&ibp=htl;events')
    sleep(5)

    try:
        for i in range(20):
            g_event_list_temp = driver.find_elements(By.CSS_SELECTOR,".PaEvOc.tv5olb.gws-horizon-textlists__li-ed")
            actions = ActionChains(driver)
            actions.move_to_element(g_event_list_temp[-1]).perform()
            sleep(2)
    except Exception as e:
        print(e)

    g_event_list = driver.find_elements(By.CSS_SELECTOR,".PaEvOc.tv5olb.gws-horizon-textlists__li-ed")
    print(len(g_event_list))
    for li in g_event_list:
            try:
                actions = ActionChains(driver)
                actions.move_to_element(li).perform()

                li.click()
                try:
                    eventID_url = driver.current_url
                    eventID = re.search(r"id=([\w]+)",eventID_url).group(1)
                except:
                    eventID = 'unknown'
                try:
                    url_div = li.find_element(By.XPATH,"//body[1]/div[2]/div[2]/div[2]/div[2]/div[3]/div[3]/div[1]/div[1]/g-sticky-content-container[1]/div[1]/div[2]/div[1]/div[2]/a[1]")
                    url = url_div.get_attribute('href')
                except:
                    url='unknown'
                try:
                    heading_div = li.find_element(By.XPATH,"//body/div[@role='main']/div/div/div/div/div/div[@jsname='aXNgRd']/div[@jsname='qlMead']/g-sticky-content-container/div/div[@jsname='tJHJj']/div[2]")
                    heading = heading_div.text
                except:
                    heading = 'uknown'
                print(heading)
                try:
                    date_div_child = li.find_element(By.XPATH,"//body/div[@role='main']/div/div/div/div/div/div[@jsname='aXNgRd']/div[@jsname='qlMead']/g-sticky-content-container/div/div/div[2]/div[1]/div[1]")
                    date = date_div_child.text
                except:
                    date='unknown'
                try:
                    location_div = li.find_element(By.XPATH,"//body/div[@role='main']/div/div/div/div/div/div[@jsname='aXNgRd']/div[@jsname='qlMead']/g-sticky-content-container/div/div/div/a/div[1]")
                    location = location_div.text
                except:
                    location = 'unknown'
                
                try:
                    img_div = li.find_element(By.XPATH,"//div[@jsname='aXNgRd']//div[@jsname='qlMead']//g-sticky-content-container//div//image-carousel//g-scrolling-carousel//div[@jsname='haAclf']//div//div[@jsname='HiaYvf']//img")
                    img = img_div.get_attribute('src')
                except:
                    img = 'unknown'
                try:
                    description_div = li.find_element(By.XPATH,"//div[@jsname='aXNgRd']//div[@jsname='qlMead']//g-sticky-content-container[@class='scm-c']//div//span[@class='PVlUWc']")
                    description = description_div.text
                except:
                    description = 'unkown'
                
                
                try:
                    apiKey = "HOYLcKv-GPRni9vRgx94s9avp2sOqCAFwUjnr3tmJKk"
                    adr = re.sub(r"\s+","+",location)
                    r = requests.get('https://geocode.search.hereapi.com/v1/geocode?q={}&apikey={}'.format(adr,apiKey))
                    lat = r.json()["items"][0]["position"]['lat']
                    lng = r.json()["items"][0]["position"]["lng"]
                except:
                    lat = 'unknown'
                    lng = 'unknown'

                google_events_data.append([DANCE_TYPE,eventID,url,heading,date,location,lat,lng,CITY,img,description])
                sleep(randint(5,10))
            except Exception as e:
                print(e)
                continue
    return google_events_data
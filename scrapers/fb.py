from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import os
import requests
from random import randint
import re
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
import pycountry

def facebook_scraper(DANCE_TYPE,CITY):
    chromedriver_autoinstaller.install()
    
    chrome_options = Options()
    # chrome_options.add_argument(f"user-data-dir={os.path.join(os.getcwd(),'Selenium')}") 
    chrome_options.add_argument("--headless")

    facebook_events_data = []
    driver = webdriver.Chrome(options=chrome_options)
    if (pycountry.countries.get(name = CITY)):
        print(pycountry.countries.get(name = CITY))
        driver.get(f'https://www.facebook.com/events/search?q={DANCE_TYPE}%20{CITY}')
    else:
        driver.get(f'https://www.facebook.com/events/search?q={DANCE_TYPE}')
        sleep(5)
        location_filter_button = driver.find_element(By.XPATH,"/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]/span[1]")
        location_filter_button.click()
        print('done')
        enter_location = driver.find_element(By.XPATH,"/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/input")
        for i in CITY:
            enter_location.send_keys(i)
        sleep(5)
        filter_button = driver.find_element(By.XPATH,"/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/li[1]")
        filter_button.click()
    sleep(10)
    SCROLL_PAUSE_TIME = 3

    last_height = driver.execute_script("return document.body.scrollHeight")

    while(True):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    f_feed = driver.find_element(By.XPATH,"(//div[@role='feed'])[1]")
    event_list = f_feed.find_elements(By.TAG_NAME,"a")
    f_event_list = []
    for i in event_list:
        f_event_list.append(i.get_attribute('href'))
    f_event_set = set(f_event_list)
    print(len(f_event_set))
    for li in f_event_set:
        try:
            driver.get(li)
            sleep(5)
            try:
                eventID_url = driver.current_url
                eventID = re.search(r"facebook\.com/events/(\d+)",eventID_url).group(1)
            except:
                eventID = 'unknown'
            try:
                url = driver.current_url
            except:
                url='unknown'
            try:
                heading_div = driver.find_element(By.XPATH,"(//span[@class='x1lliihq x6ikm8r x10wlt62 x1n2onr6'])[1]")
                heading = heading_div.text
            except:
                heading = 'uknown'
            print(heading)
            try:
                date_div_child = driver.find_element(By.XPATH,"(//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x41vudc x6prxxf xvq8zen x1xlr1w8 x1a1m0xk x1yc453h'])[1]")
                date = date_div_child.text
            except NoSuchElementException:
                date_div_child = driver.find_element(By.XPATH,"(//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x41vudc x6prxxf xvq8zen x1xlr1w8 x1dntmbh x1yc453h'])[1]")
                date = date_div_child.text
            except:
                # print(e)
                date='unknown'

            # print(date)
            try:
                location_div = driver.find_element(By.XPATH,"(//div[@class='x78zum5 xdt5ytf xz62fqu x16ldp7u'])[7]")
                location = location_div.text
            except:
                location = 'unknown'
            # print(location)
            
            try:
                img_div = driver.find_element(By.XPATH,"(//img[@data-imgperflogname='profileCoverPhoto'])[1]")
                img = img_div.get_attribute('src')
            except:
                img = 'unknown'
            # print(img)
            try:
                description_div = driver.find_element(By.XPATH,"(//div[@class='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs'])[1]")
                description = description_div.text
            except:
                description = 'unkown'
            # print(description)
                
                
            try:
                apiKey = "HOYLcKv-GPRni9vRgx94s9avp2sOqCAFwUjnr3tmJKk"
                adr = re.sub(r"\s+","+",location)
                r = requests.get('https://geocode.search.hereapi.com/v1/geocode?q={}&apikey={}'.format(adr,apiKey))
                lat = r.json()["items"][0]["position"]['lat']
                lng = r.json()["items"][0]["position"]["lng"]
            except:
                lat = 'unknown'
                lng = 'unknown'

            facebook_events_data.append([DANCE_TYPE,eventID,url,heading,date,location,lat,lng,CITY,img,description])
            sleep(randint(5,10))
        except Exception as e:
            print(e)
            continue
    print(f"done for {CITY}")
    sleep(30)
    return facebook_events_data


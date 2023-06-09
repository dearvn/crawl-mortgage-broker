import requests, json
import time
import argparse
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import re

def main():
    # Chrome driver options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", { \
        "profile.default_content_setting_values.notifications": 1
    })
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')  # for interface progressing

    # Prepare driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    
    try:
        # get url facebook from database
        url = 'https://www.facebook.com/PlatinumBrian'
        
        driver.get(url)
        time.sleep(5)

        source = driver.page_source

        match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', source)
        if match is None:
            exit()

        email = match.group(0)

        print(">>>>>>", email)

        #save email to database

    except:
        print("An exception occurred")


if __name__ == "__main__":
    main()

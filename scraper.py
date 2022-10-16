from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd


START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

# Webdriver
browser = webdriver.Edge("msedgedriver.exe")
browser.get(START_URL)

time.sleep(10)

star_data = []

# Define Exoplanet Data Scrapping Method
def scrape():

    for i in range(0,10):
        print(f'Scrapping page {i+1} ...' )
        
        # BeautifulSoup Object     
        soup = BeautifulSoup(browser.page_source, "html.parser")

        # Loop to find element using XPATH
        for ul_tag in soup.find_all("ul", attrs={"class", "star"}):

            li_tags = ul_tag.find_all("li")
           
            temp_list = []

            for index, li_tag in enumerate(li_tags):

                if index == 0:                   
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")

            star_data.append(temp_list)

        # Find all elements on the page and click to move to the next page
        browser.find_element(by=By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

# Calling Method    
scrape()

# Define Header
headers = ["V Mag. (mV) ", "Proper name ", "Bayer designation", "Distance (ly) ", "Spectral class ",'Mass (M☉) ','Radius (R☉) ','Luminosity (L☉)' ]

# Define pandas DataFrame   
star_df_1 = pd.DataFrame(star_data, columns=headers)

# Convert to CSV
star_df_1.to_csv('scraped_data.csv',index=True, index_label="id")

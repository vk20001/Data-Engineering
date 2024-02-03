#!/usr/bin/env python
# coding: utf-8

# In[2]:


import re
import csv
from time import sleep, strftime
from random import randint
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib

# Load more results to maximize the scraping
def load_more():
    try:
        more_results = '//div[@class="ULvh-button show-more-button"]'
        driver.find_element_by_xpath(more_results).click()
        print('sleeping.....')
        sleep(0.50)
    except:
        pass


# Collect data at one place

def page_scrape():

    #Airline logo image
    image_list = []
    xp_image = driver.find_elements_by_xpath('//div[@class="c5iUd-leg-carrier"]')

    for xp_images in xp_image:
        img_elements = xp_images.find_elements_by_xpath('.//img')
        for img_element in img_elements:
            img_src = img_element.get_attribute('src')
            image_list.append(img_src)

    # Airline_Name
    airline_name = []
    xp_name = driver.find_elements_by_xpath('//div[@class="c5iUd-leg-carrier"]')

    for xp_names in xp_name:
        img_elements = xp_names.find_elements_by_xpath('.//img')
        for img_element in img_elements:
            alt_attribute = img_element.get_attribute('alt')
            airline_name.append(alt_attribute)

    # Hault_location
    lay_over_location = []
    lay_overs = driver.find_elements_by_xpath('//div[@class="JWEO"]')
    for lay_over in lay_overs:
        lay_over_text = lay_over.text.split()
        lay_over_location.append(lay_over_text[2:])


    # Departure From and To
    departures_location = driver.find_elements_by_xpath('//div[@class="c_cgF c_cgF-mod-variant-full-airport-wide"]')
    titles = []
    for departure in departures_location:
        title = departure.get_attribute('title')
        titles.append(title)

    titles = titles
    Departure_list = []
    Arrival_list = []

    for title in titles:
        if title == 'Lissabon':
            Departure_list.append(title)
        elif title == 'Singapur Changi':
            Arrival_list.append(title)

    # Departure and Arival time 
    departure_time = driver.find_elements_by_xpath('//div[@class="VY2U"]/div[1]')
    time_list = []
    for time_element in departure_time:
        time_text = time_element.text.replace('\n+1','').replace('\n+2', '').replace('\n+3', '')
        time_list.append(time_text)

    # Airline Price
    xp_prices = '//div[@class="f8F1-price-text"]'
    prices = driver.find_elements_by_xpath(xp_prices)
    prices_list = [price.text.replace('€','') if price.text.strip() else 'N/A' for price in prices]
    prices_list


    cols = (['Airline_logo', 'Airline_Name', 'Departure_From', 'Departure_To', 'Hault_location', 'Time' ,'Price'])
    flights_df = pd.DataFrame({'Airline_logo' : image_list[0:200] ,
                               'Airline_Name' : airline_name[0:200] ,
                               'Departure_From': Departure_list[0:200] ,
                               'Departure_To' : Arrival_list[0:200] , 
                               'Hault_location' : lay_over_location[0:200],
                               'Time' : time_list[0:200] ,
                               'Price' : prices_list[0:200]})[cols]
    
    flights_df.to_csv("kayak_df.csv")

#     with open("kayak_df.csv", "w") as csvfile:
        
#         writer = csv.writer()
#         writer.writerows(flights_df)

    return flights_df


# https://www.kayak.de/flights/FRA-LHR/2024-03-16?sort=bestflight_a
chromedriver_path = 'C:/Users/arave/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe' 
driver = webdriver.Chrome(executable_path=chromedriver_path)
sleep(2)
kayak = 'https://www.kayak.de/flights/LIS-SIN/2024-03-16?sort=bestflight_a'
driver.get(kayak)
sleep(2)
xp_popup_click = '//*[@id="portal-container"]/div/div[2]/div/div/div[1]/div/span[2]'
driver.find_element_by_xpath(xp_popup_click).click()
sleep(1)
for i in range(1,14):
    print("loading_more_page_" + str(i))
    load_more()
    
page_scrape()
sleep(10)
driver.quit()


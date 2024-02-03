import csv
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
 
def scrape_page(driver):
    wait = WebDriverWait(driver,1500 )
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[2]')))
   
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    flight_rows = soup.find_all('div', class_='m-result-list')
   
    flights_list = []
   
    for flight_row in flight_rows:
        Destination = flight_row.find('span', {'class': 'flight-info-stop__code_sKh'})
        Departure = flight_row.find('span', {'class': 'flight-info-stop__code_sKh'})
        # mar_23 = flight_row.find('div', {'data-testid': 'flight_card_segment_departure_date_0'})
        Airline_Name = flight_row.find('div', {'data-testid': 'flights-name'})
        Departure_time = flight_row.find('span', {'class': 'time'})
        Destination_time = flight_row.find('span', {'class': 'time'})
        price = flight_row.find('span', {'class': 'ThemeColor8 f-20 o-price-flight_sbf no-cursor_sb0'})
        Duration = flight_row.find('div', {'class': 'v-center flight-info-stop__segline-wrapper_sMN'})
   
        if Destination is not None:  
 
            Departure_time = datetime.strptime(Departure_time.text, '%H:%M')
            Destination_time = datetime.strptime(Destination_time.text, '%H:%M')
 
            Duration= Destination_time - Departure_time
 
            flight = {
                'Destination': Destination.text,
                'Departure': Departure.text,
                # 'mar_23': mar_23.text,
                'Airline_Name': Airline_Name.text,
                'price': price.text,
                'Departure_time': Departure_time.strftime('%H:%M'),
                'Destination_time': Destination_time.strftime('%H:%M'),
                'Duration': str(Duration)  
               
            }
            flights_list.append(flight)
   
    return flights_list
 
def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
   
    driver = webdriver.Chrome(options=chrome_options)
   
    base_url = 'https://uk.trip.com/flights/frankfurt-to-london/tickets-fra-lon?dcity=fra,fra&acity=lon,lhr&ddate=2024-03-23&rdate=2024-03-26&flighttype=ow&class=y&lowpricesource=searchform&quantity=1&searchboxarg=t'
    
    current_page_number = 1
    max_pages = 5  # Set the maximum number of pages you want to scrape
   

    all_flights_list = []
   
    while current_page_number <= max_pages:
        page_url = f'{base_url}&page={current_page_number}'
        driver.get(page_url)


        # driver.execute_script for of window screen
        
        # driver.find_element('')

       
        flights_list = scrape_page(driver)
        all_flights_list.extend(flights_list)
       
        current_page_number += 1
 
    flights_df = pd.DataFrame(flights_list)
   
    with open('all_flights_trip.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Destination', 'Departure', 'Airline_Name', 'price', 'Departure_time','Destination_time','Duration'])
        for flight in all_flights_list:
            writer.writerow([flight['Destination'], flight['Departure'], flight['Airline_Name'], flight['price'], flight['Departure_time'],flight['Destination_time'],flight['Duration']])
        print("csv file is done")
 
    flights_df.to_excel('all_flights_trip.xlsx', index=False)
    print("Excel file is done")
   
    driver.close()
 
if __name__ == '__main__':
    main()
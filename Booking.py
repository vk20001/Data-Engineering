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
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="basiclayout"]/div/div/div[2]/div/div/div/div/div[2]/div[3]/div[1]')))
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    flight_rows = soup.find_all('div', class_='Frame-module__margin-bottom_4___6J8o7')
    
    flights_list = []
    
    for flight_row in flight_rows:
        Destination = flight_row.find('div', {'data-testid': 'flight_card_segment_destination_airport_0'})
        Departure = flight_row.find('div', {'data-testid': 'flight_card_segment_departure_airport_0'})
        # mar_23 = flight_row.find('div', {'data-testid': 'flight_card_segment_departure_date_0'})
        Airline_Name = flight_row.find('div', {'data-testid': 'flight_card_carrier_0'})
        Departure_time = flight_row.find('div', {'data-testid': 'flight_card_segment_departure_time_0'})
        Destination_time = flight_row.find('div', {'data-testid': 'flight_card_segment_destination_time_0'})
        price = flight_row.find('div', {'class': 'FlightCardPrice-module__priceContainer___nXXv2'})
    
        if Destination is not None:   

            Departure_time = datetime.strptime(Departure_time.text, '%H:%M')
            Destination_time = datetime.strptime(Destination_time.text, '%H:%M')

            Duration= Destination_time - Departure_time

            # print('Destination: ', Destination.text)
            # print('Departure: ', Departure.text)
            # # print('mar_23: ', mar_23.text)
            # print('Airline_Name: ', Airline_Name.text)
            # print('price: ', price.text)
            # print('Departure_time: ', Departure_time.text)
            # print('Destination_time: ', Destination_time.text)
            # print('----------------------')
    
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
    
    base_url = 'https://flights.booking.com/flights/LHR.AIRPORT-AMS.AIRPORT/?type=MULTISTOP&adults=1&cabinClass=ECONOMY&children=&from=LHR.AIRPORT&to=AMS.AIRPORT&fromCountry=GB&toCountry=NL&fromLocationName=London+Heathrow+Airport&toLocationName=Schiphol+Airport&multiStopDates=2024-04-06&sort=BEST&travelPurpose=leisure&aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaDuIAQGYAQm4AQfIAQzYAQHoAQH4AQyIAgGoAgO4AqfHya0GwAIB0gIkOTQ3NjI5OTktNDk1MC00NzBiLThkZTYtM2Y2M2JmNjhiOTNi2AIG4AIB&airlines=EI%2CAC%2CAF%2COS%2CBA%2CSN%2CEK%2C9F%2CAY%2CAZ%2CIB%2CLO%2CLH%2CKM%2CDY%2CD8%2CQR%2CSK%2CLX%2CTP%2CTK%2CUA'
    
    current_page_number = 1
    max_pages = 21  # Set the maximum number of pages you want to scrape
    
    all_flights_list = []
    
    while current_page_number <= max_pages:
        page_url = f'{base_url}&page={current_page_number}'
        driver.get(page_url)
        
        flights_list = scrape_page(driver)
        all_flights_list.extend(flights_list)
        
        current_page_number += 1

    flights_df = pd.DataFrame(flights_list)
    
    with open('flights_19.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Destination', 'Departure', 'Airline_Name', 'price', 'Departure_time','Destination_time','Duration'])
        for flight in all_flights_list:
            writer.writerow([flight['Destination'], flight['Departure'], flight['Airline_Name'], flight['price'], flight['Departure_time'],flight['Destination_time'],flight['Duration']])
        print("csv file is done")

    flights_df.to_excel('flights_19.xlsx', index=False)
    print("Excel file is done")
    
    driver.close()

if __name__ == '__main__':
    main()

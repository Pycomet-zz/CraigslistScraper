# BY CODEFREDY
# This is wriiten to be compactible with Python 3.6.7

# Importing needed modules for this script
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import csv
from bs4 import BeautifulSoup
import requests

class CraigslistScraper(object):
    def __init__(self, location, max_price, min_price):
        self.location = location
        self.max_price = max_price
        self.min_price = min_price
        self.driver = webdriver.Chrome('./chromedriver')
        self.sleep = time.sleep(4)
        self.url = f"https://{location}.craigslist.org/search/hhh?query=rent&sort=rel&min_price={min_price}&max_price={max_price}&min_bedrooms=3&availabilityMode=0&housing_type=3&housing_type=4&housing_type=5&housing_type=6&housing_type=7&housing_type=8&housing_type=10&housing_type=11&housing_type=12&sale_date=all+dates&lang=en&cc=gb"
        self.url2 = f"https://{location}.craigslist.org/search/hhh?query=sale%20by%20owner&sort=rel&min_price{min_price}&max_price={max_price}&min_bedrooms=3&availabilityMode=0&sale_date=all+dates&lang=en&cc=gb"

    def forRent(self):
        """Open the Craiglist Search Result For Rent"""

        try:
            self.driver.get(self.url)
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.ID, "searchform")))
            print("Page is ready!")
        except TimeoutException:
            self.driver.get(self.url)
            print("BAD NETWORK! RESTART APPLICATION")

    def forSale(self):
        """Open the Craiglist Search Result For Sale By Owner"""

        try:
            self.driver.get(self.url2)
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.ID, "searchform")))
            print("Page is ready!")
        except TimeoutException:
            self.driver.get(self.url2)
            print("loading took too much time")

    def extract_titles(self):
        """Scraping Searched Names, Date-posted and Price"""

        titles = self.driver.find_elements_by_class_name("result-row")
        self.names = []
        self.dates = []
        self.prices = []

        # Spliting the extracted title content to smaller data
        for post in titles:
            title = post.text.split("$")

            if title[0] == '':
                title = title[1]
            else:
                title = title[0]

            title = title.split("\n")
            price = title[0]
            title = title[-1]

            title = title.split(" ")

            month = title[0]
            day = title[1]
            title = ''.join(title[2:])
            date = month + " " + day

            self.dates.append(date)
            self.prices.append(price)
            self.names.append(title)

    def extract_links(self):
        """Scraping Search Results Individual Email Links"""

        self.url_list = []
        print("Extract links....")

        for a in range(500):
            self.driver.find_elements_by_class_name("result-row")[a].click()
            self.sleep
            link = self.driver.current_url
            self.sleep

            self.url_list.append(link)
            self.driver.get(self.url) 
            self.sleep

    def read_forRent_to_csv(self):
        """Reading Scraped Data For Rent To CSV File"""

        #Open csv file
        with open("CraigslistForRent.csv", "w", newline='') as csvfile:
        #Input headers
            fieldnames = ['Names', 'Dates', 'Prices', 'Links']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
        #Input scraped content
            for i in range(500):
                writer.writerow({'Names': self.names[i].ljust(50), 'Prices': self.prices[i], 'Dates': self.dates[i], 'Links': self.url_list[i]})

    def read_forSale_to_csv(self):
        """Reading Scraped Data For Sale By Owner To CSV File"""

        #Open csv file
        with open("CraigslistForSaleByOwner.csv", "w", newline='') as csvfile:
        #Input headers
            fieldnames = ['Names', 'Dates', 'Prices', 'Links']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
        #Input scraped content
            for i in range(500):
                writer.writerow({'Names': self.names[i].ljust(50), 'Prices': self.prices[i], 'Dates': self.dates[i], 'Links': self.url_list[i]})

    def quit(self):
        """Exit CraigslistBot"""

        self.driver.quit()




while True:

    # Choose between For Rent and For Sale
    print("""HEY! I AM GOING TO SCRAPE YOUR REQUESTED CONTENT FROM CRAIGSLIST TO AN EXCEL FILE""")
    search = input("Reply with '1' To Search By Rent or '2' To Search By For Sale From Owner:-")

    if search == '1':
        print("All necessary types are checked off!")
        location = input("Input Location Here(States Only e.g 'houston'): ")
        max_price = input("Input Maximum Price Here: ")
        min_price = input("Input Minimum Price Here: ")
        scraper = CraigslistScraper(location, max_price, min_price)
        print("BOT LOADING........")

        scraper.forRent()
        scraper.extract_titles()
        scraper.extract_links()
        scraper.read_forRent_to_csv()

        print("DONE!!")
        scraper.quit()  

    elif search == '2':
        location = input("Input Location Here: ")
        max_price = input("Input Maximum Price Here: ")
        min_price = input("Input Minimum Price Here: ")
        scraper = CraigslistScraper(location, max_price, min_price)
        print("BOT LOADING........")

        scraper.forSale()
        scraper.extract_titles()
        scraper.extract_links()
        scraper.read_forSale_to_csv()

        print("DONE!!")
        scraper.quit() 

    else:
        print("WRONG INPUT!!! TRY AGAIN.")

        print("DONE!!")
        scraper.quit()    

from bs4 import BeautifulSoup
import urllib3
import time
import json
import sys

"""
Author: David Hill, Jr.
Version: 1.0.0
This web scraper tool allows a user to input web urls and scrape data from 
the html of the given page. Ideally I would like this CLI tool to be robust with a
lot of features.
"""

class WebScraper():
    urls = {}

    def __init__(self):
        self.http = urllib3.PoolManager()
        urllib3.disable_warnings()

    def println(self, str):
        print(str, end='\r', flush=True)

    def menu(self):
        self.displayMenu()
        scraper = WebScraper()
        param = int(input("        >>> "))
        if param == 1:
            url = input("        Enter a URL to Scrape: ")
            scraper.addUrl(url)
            self.menu()
        if param == 2:
            self.displayUrls()
            idx_delete = input("        Select a URL to Delete: ")
            item_delete = list(self.urls.keys())[int(idx_delete)-1]
            self.delUrl(item_delete)
            self.menu()
        if param == 3:
            self.displayUrls()
            idx_scrape = input("        Select a URL to scrape: ")
            item_scrape = list(self.urls.keys())[int(idx_scrape)-1]
            self.scrapeUrl(self.urls[item_scrape])
            self.menu()
        if param == 4:
            self.displayUrls()
            self.menu()
        if param == 5:
            self.menu()
        if param == 6:
            exit(0)
        else:
            print("Please enter a valid menu option")
            self.menu()

    def displayMenu(self):
        print("""
        MENU________________________________________________
        [1] Add a URL
        [2] Delete a URL
        [3] Scrape a URL
        [4] Display all URLs
        [5] Export Data to File
        [6] EXIT
        ____________________________________________________ 
        """)
           
    def addUrl(self, url):
        self.println("        Adding " + url + " to URL list.")   
        try:
            page_request = self.http.request('GET', url)
            soup = BeautifulSoup(page_request.data, 'html.parser')
            self.urls[url] = soup
            print("        Operation Successful!")
        except:
            print("        An error occurred getting the page you requested.")
            self.urls[url] = ""
            return

    def delUrl(self, url):
        if url in self.urls.keys():
            self.println("        Deleting " + url + " from URL List.")
            del self.urls[url]
        else:
            print("        URL does not exist or has already beed deleted!")
        return

    def scrapeUrl(self, url):
        return

    def displayUrls(self):
        url_list = list(self.urls.keys())
        for i in range(len(url_list)):
            print("        ["+ str(i+1) +"]: " + url_list[i])
        return
    
scraper = WebScraper()
scraper.menu()
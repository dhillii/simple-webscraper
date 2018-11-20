from bs4 import BeautifulSoup
import urllib3
import time
import json

def main():

    http = urllib3.PoolManager()

    start_url = 'https://shop.naturallycurly.com/find-your-texture-type/'

    start_page = http.request('GET', start_url)

    soup = BeautifulSoup(start_page.data, 'html.parser')

    secondary_links = ['https://shop.naturallycurly.com/shop-by-texture-4a/',
    'https://shop.naturallycurly.com/shop-by-texture-4b/',
    'https://shop.naturallycurly.com/shop-by-texture-4c/',
    'https://shop.naturallycurly.com/shop-by-texture-3a/',
    'https://shop.naturallycurly.com/shop-by-texture-3b/',
    'https://shop.naturallycurly.com/shop-by-texture-3c/',
    'https://shop.naturallycurly.com/shop-by-texture-2a/',
    'https://shop.naturallycurly.com/shop-by-texture-2b/',
    'https://shop.naturallycurly.com/shop-by-texture-2c/']

    database = {
        'hair_types':{
            '4A':{'products':[]},
            '4B':{'products':[]},
            '4C':{'products':[]},
            '3A':{'products':[]},
            '3B':{'products':[]},
            '3C':{'products':[]},
            '2A':{'products':[]},
            '2B':{'products':[]},
            '2C':{'products':[]}
        }
    }

    pageWalker(secondary_links, database)















#unfortunately this will probably be O(n*n) but at 3am I cant think of anything better.
#let me push before I forget
def pageWalker(secondary_links, database):

    http = urllib3.PoolManager()

    iterator = '?sort=featured&page='

    #for every link - key value
    for link, key in zip(secondary_links, database['hair_types']):
        start = 1
        time.sleep(2)

        #For each page paginate through the first 5 pages
        for subpage in range(5):
            new_link = link + iterator + str(start)
            start += 1
            
            page_request = http.request('GET', new_link)
            soup = BeautifulSoup(page_request.data, 'html.parser')

            #Runs through all product links on page and scrapes each product
            for prod in soup.find_all('h1', class_='product-item-title'):
                a = prod.contents[1]
                product = scrapeProduct(a['href'])
                database['hair_types'][key]['products'].append(product)
                time.sleep(2)

                
    with open('curl-iq-final.json', 'w') as file:
        json.dump(database, file)
                

#This function scrapes product data from a product page on NaturallyCurly.com works for the most part
def scrapeProduct(url):

    http = urllib3.PoolManager()

    classifiers = {'condition':'Conditioner', 'shampoo': 'Shampoo', 'oil': 'Styler', 'moisturizer': 'Styler', 'custard': 'Styler', 'butter': 'Styler', 'cream': 'Styler'}
    product = {}

    page = http.request('GET', url)
    soup = BeautifulSoup(page.data, 'html.parser')

    prod_price = soup.find(class_ = 'price-value').get_text()
    prod_price = prod_price.strip()

    prod_name = soup.find(class_='product-title').get_text()                    # Gets product title, brand, and description

    product_string = prod_name.lower()

    prod_type = ''

    for key in classifiers:
        if key in product_string:
            prod_type = classifiers[key]

    brand = soup.find(class_='product-brand').get_text()
    description = soup.find(id='product-tab-description').get_text()
    description = description.strip()
    description = description.replace('\n', '')
    description = description.replace('\xa0', '')


    prod_img_element = soup.find('img', alt=prod_name)                          # Gets image element ang source url
    prod_img = prod_img_element['src']

    try:
        ingredients = soup.find('strong', text='Ingredients:').next_sibling     # Get next sibling of Key ingredients 
        ingredients = ingredients.strip()

    except:
        ingredients = "Could not find..."     


    product[prod_name] ={'prod_brand':brand, 'prod_type': prod_type ,'price': prod_price,'description':description, 'ingredients':ingredients,'image': prod_img, 'prod_url': url}

    return product


if __name__ == "__main__":
    main()
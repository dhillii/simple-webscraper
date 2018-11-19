from bs4 import BeautifulSoup
import urllib3

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
'https://shop.naturallycurly.com/type-2b-wavy-hair/',
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

#unfortunately this will probably be O(n*n) but at 3am I cant think of anything better.
#let me push before I forget
def pageWalker(secondary_links, database):

    for link in secondary_links:



#This function scrapes product data from a product page on NaturallyCurly.com works for the most part
def scrapeProduct(url):
    product = {}

    page = http.request('GET', url)
    soup = BeautifulSoup(page.data, 'html.parser')

    prod_price = soup.find(class_ = 'price-value').get_text()
    prod_price = prod_price.strip()

    prod_name = soup.find(class_='product-title').get_text()                    # Gets product title, brand, and description
    brand = soup.find(class_='product-brand').get_text()
    description = soup.find(id='product-tab-description').get_text()
    description = description.strip()

    prod_img_element = soup.find('img', alt=prod_name)                          # Gets image element ang source url
    prod_img = prod_img_element['src']

    try:
        ingredients = soup.find('strong', text='Key ingredients:').next_sibling
    
    except:
        ingredients = "Could not find..."     # Get next sibling of Key ingredients 

    ingredients = ingredients.strip()

    product[prod_name] ={'prod_brand':brand, 'price': prod_price,'description':description, 'ingredients':ingredients,'image': prod_img, 'prod_url': url}
    
    return product

def main():


    return

    
if __name__ == "__main__":
    main()
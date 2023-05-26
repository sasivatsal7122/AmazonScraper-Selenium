from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import argparse


PAGE_LIMIT =20
SEARCH_TERM = "men shoes"
OUTPUT_FILENAME = 'scraped products'
OUTPUT_FILEFORMAT = 'xlsx'


def getSearchResults(driver):

    items = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
    
    productNames = []
    for item in items:
        pdname = item.find_element(By.CSS_SELECTOR, "h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-2")
        productNames.append(pdname.text)
        
    productUrl = []
    for item in items:
        pdlinks = item.find_element(By.CSS_SELECTOR, "a.a-link-normal.a-text-normal")
        productUrl.append(pdlinks.get_attribute('href'))
        
    productPrice = []
    for item in items:
        try:
            pdprice = item.find_element(By.CSS_SELECTOR, "span.a-price").text
        except:
            pdprice = "Not Found"
        productPrice.append(pdprice)
        
    productRating = []
    productReviews = []
    for item in items:
        ratings_box = item.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')

        if ratings_box != []:
            pdratingStars = ratings_box[0].get_attribute('aria-label')
            pdratingNumber = ratings_box[1].get_attribute('aria-label')
        else:
            pdratingStars, pdratingNumber = 0, 0

        productRating.append(pdratingStars)
        productReviews.append(pdratingNumber)
    
    return productNames,productUrl,productPrice,productRating,productReviews


def startAmazonScraper(driver):
    
    current_page = 1
    driver.get(f"https://www.amazon.in/s?k={SEARCH_TERM}&ref=nb_sb_noss")
    while current_page<=PAGE_LIMIT:
        
        print(f"Starting to Scrape Page-{current_page}",end="\r")
        productNames,productUrl,productPrice,productRating,productReviews = getSearchResults(driver)
        
        MasterproductNames.extend(productNames)
        MasterproductUrl.extend(productUrl)
        MasterproductPrice.extend(productPrice)
        MasterproductRating.extend(productRating)
        MasterproductReviews.extend(productReviews)
        print(f"Page-{current_page} Scraping completed",end="\r")
        current_page+=1
        driver.get(f"https://www.amazon.in/s?k={SEARCH_TERM}&page={current_page}&ref=sr_pg_1")

    data = {
        'Product Name': MasterproductNames,
        'Product URL': MasterproductUrl,
        'Product Price': MasterproductPrice,
        'Product Rating': MasterproductRating,
        'Product Reviews': MasterproductReviews
    }
    
    return data
    
def get_driver():
    options = Options()
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options,service=Service(ChromeDriverManager().install()))
    return driver

def save_data(data):

    df = pd.DataFrame(data).drop_duplicates()
    if OUTPUT_FILEFORMAT == 'csv':
        df.to_csv(f'{OUTPUT_FILENAME}.{OUTPUT_FILEFORMAT}', index=False)
    else:
        df.to_excel(f'{OUTPUT_FILENAME}.{OUTPUT_FILEFORMAT}', index=False)
    

if __name__ == '__main__':
    
    print("Starting Amazon Scraper")
    parser = argparse.ArgumentParser(description='Amazon Product Scraping Script')
    parser.add_argument('--page-limit', type=int, help='Number of pages to scrape')
    parser.add_argument('--search-term', type=str, help='Search term for scraping')
    parser.add_argument('--output-filename', type=str, help='Output filename')
    parser.add_argument('--output-fileformat', type=str, help='Output file format')

    args = parser.parse_args()

    if args.page_limit:
        PAGE_LIMIT = args.page_limit
    if args.search_term:
        SEARCH_TERM = args.search_term
    if args.output_filename:
        OUTPUT_FILENAME = args.output_filename
    if args.output_fileformat:
        OUTPUT_FILEFORMAT = args.output_fileformat
            
    MasterproductNames = []
    MasterproductUrl= []
    MasterproductPrice =[]
    MasterproductRating = []
    MasterproductReviews = []
    
    print("loading driver")
    driver = get_driver()
    print("driver loaded")
    
    print("Starting to scrape")
    
    print(f"Scraping Started for:\nPage Limit = {PAGE_LIMIT}\nSearch Term = {SEARCH_TERM}")
    print(f"Output Filename = {OUTPUT_FILENAME}\nOutput Fileformat = {OUTPUT_FILEFORMAT}")
    
    data = startAmazonScraper(driver)
    print("Scraping completed")
    
    print("Saving data")
    save_data(data)
    print("Data saved")
    
    

    









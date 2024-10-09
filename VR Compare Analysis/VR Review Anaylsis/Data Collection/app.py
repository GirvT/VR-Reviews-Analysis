import time

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from env import URL, DriverLocation

def view_reviews(driver):
    '''
    Given a google search results page of a business pull up reviews 
    '''
    view = driver.find_element(By.LINK_TEXT, 'View all Google reviews')
    view.click()
    time.sleep(10)
    newest = driver.find_element(By.XPATH, "//div[@data-sort-id='newestFirst']")
    newest.click()

def expand_reviews(driver):
    '''
    Given view_reviews was used find any reviews body with 
    "more" attached to it and expand it to the full review
    '''
    expand_list = driver.find_elements(By.CLASS_NAME, 'review-more-link')
    x = 0
    y = len(expand_list)
    for expand in expand_list:
        x = x + 1
        expand.click()
        print(str(x) + "/" + str(y))

def load_reviews(driver, count=10):
    '''
    Given a scrollable google reviews page scroll down to 
    get as many as count reviews 
    '''
    xpath_review_block = "//div[@class='gws-localreviews__general-reviews-block']//div[@class='WMbnJf vY6njf gws-localreviews__google-review']"
    
    wait = WebDriverWait(driver,10)
    wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_review_block)))

    x = 0
    while x < count:
        print("load "+str(x)+" reviews")
        time.sleep(10)
        driver.find_element(By.XPATH, "(" + xpath_review_block + ")[last()]").location_once_scrolled_into_view
        x = x + 10
        


if __name__ == "__main__":

    print('boot driver')
    options = webdriver.FirefoxOptions()
    options.binary_location = r'C:/Program Files/Mozilla Firefox/firefox.exe'
    options.add_argument("--lang=en-US")
    #options.accept_untrusted_certs = True
        
    DriverPath = DriverLocation
    service = Service(executable_path = DriverPath) 
    driver = webdriver.Firefox(service = service, options = options)

    print('get URL from env')
    driver.get(URL)
    time.sleep(10)

    print("get reviews")
    view_reviews(driver)
    time.sleep(10)

    x = 1300
    print("loading " + str(x) + " reviews")
    load_reviews(driver, x)
    time.sleep(10)

    print("expanding reviews")
    expand_reviews(driver)
    time.sleep(10)

    with open("./page_source_CTRLV.html", "w", encoding='utf-8') as f:
        f.write(driver.page_source)

    print('shutdown driver')
    driver.close()
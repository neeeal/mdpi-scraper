from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
# import multiprocessing 
import random
import requests

def initialize(url):
    '''
        Function to initialize a Selenium Driver for Automatoin.
        
        url: string formattable url (e.g. https://www.mdpi.com/search?sort=pubdate&page_no={}&journal=societies&view=default)
            note that the curly braces for page is required.
    '''
    ## Opens selenium browser and maximizes window
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'none'
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=service)
    driver.maximize_window()
    page = 1
    baseUrl = url.format(page)
    
    ## Opens base url and scrolls to bottom of page
    driver.get(baseUrl)
    try:
        WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="exportArticles"]/div/div[2]/div[50]'))
        )
    except Exception as e:
        driver.get(baseUrl)
        WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="exportArticles"]/div/div[2]/div[50]'))
        )
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    return driver

def get_max_pages(driver):
    '''
        Function to retrieve max pages for the given base url
    '''
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    max_page = int(soup.find('div', {'class':'columns large-6 medium-6 small-12'}).text.split(' ')[-1].strip()[:-1])
    return max_page

def accept_cookies(driver):
    '''
        Function to accept cookies
    '''
    try:
        ## Try to click accept button if any
        accept_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection"]'))
        )
        accept_button = driver.find_element(By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection"]')
        accept_button.click()
    except Exception as e: 
        print(e)

def scrape_article_details(driver, link, journal_id):
    ## Add article reference, QCUJ journal id, and original journal name
    flag = 0
    py_headers = ({'User-Agent':
        'Safari/537.36',\
        'Accept-Language': 'en-US, en;q=0.5'})
    while flag<2:
        try: 
            article_page = requests.get(link, headers = py_headers)
            soup = BeautifulSoup(article_page.text, 'html5lib')
            reference_text = soup.find('div', {'class':'additional-content'}).find('div', {'class':'in-tab'}).find('p').text.replace('\n','')
            journal_name = soup.find('div', {'id':'footer'}).find('a').text
            break
        except Exception as e:
            ## retry for one time if fail
            print(e)
            flag+=1
    if flag == 2: return False
    return [reference_text, journal_id, journal_name]
    

def first_page_articles(driver, journal_id, limit):
    '''
        Function to scrape first page of the base url
    '''
    ## Get all article links from first page
    title_link = [link.get_attribute('href') for link in driver.find_elements(By.CLASS_NAME,'title-link')]
    references = []
    
    for i in range(len(title_link)):
        if limit > 0 and len(references) >= limit: 
            return references
        article_details = scrape_article_details(driver, title_link[i], journal_id)
        references.append(article_details)
        print(len(references),article_details[-1])
        time.sleep(random.randint(2, 5))
    return references

def scrape_articles(driver, max_page, journal_id, url, limit):
    '''
        Function to scrape other pages
    '''
    references = first_page_articles(driver, journal_id, limit)
    
    for page in range(2,max_page):
        ## Loop through given pages
        baseUrl = url.format(page)
        driver.get(baseUrl)
        accept_cookies(driver)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        ## Get all article links from first page
        title_link = [link.get_attribute('href') for link in driver.find_elements(By.CLASS_NAME,'title-link')]
        
        for i in range(len(title_link)):
            if limit > 0 and len(references) >= limit: 
                return references
            article_details = scrape_article_details(driver, title_link[i], journal_id)
            if article_details == False: continue
            references.append(article_details)
            print(len(references),article_details[-1])
            
    return references

def save_references(references, method, path):
    '''
        Function to save references to given path
    '''
    with open(path, method, encoding="utf-8") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerows(references)
        
def run_scraper(url, journal_id, file_method, path, limit = -1, ):
    '''
        Function to run one scraper full cycle
    '''
    driver = initialize(url)
    accept_cookies(driver)
    max_page = get_max_pages(driver)
    references = scrape_articles(driver, max_page, journal_id, url, limit)
    save_references(references, file_method, path)
    driver.close()
    
def runP1():
    run_scraper('https://www.mdpi.com/search?sort=pubdate&page_no={}&journal=societies&view=default', 1, 'w', 'D:/dev/mdpi-scraper/sample/temp/societies.csv')
def runP2():
    run_scraper('https://www.mdpi.com/search?sort=pubdate&page_no={}&journal=socsci&view=default', 1, 'w', 'D:/dev/mdpi-scraper/sample/temp/socsci.csv')
def runP3():
    run_scraper('https://www.mdpi.com/search?sort=pubdate&page_no={}&journal=education&view=default', 2, 'w', 'D:/dev/mdpi-scraper/sample/temp/education.csv')
def runP4():
    run_scraper('https://www.mdpi.com/search?sort=pubdate&page_no={}&journal=technologies&view=default', 3, 'w', 'D:/dev/mdpi-scraper/sample/temp/technologies.csv')
def runP5():
    run_scraper('https://www.mdpi.com/search?sort=pubdate&page_no={}&journal=smartcities&view=default', 3, 'w', 'D:/dev/mdpi-scraper/sample/temp/smartcities.csv', 150)
def runP6():
    run_scraper('https://www.mdpi.com/search?sort=pubdate&page_no={}&journal=engproc&view=default', 3, 'w', 'D:/dev/mdpi-scraper/sample/temp/engproc.csv')
        
if __name__ == '__main__':

    '''
    Unfortunately, MDPI blocks this 
    because it is seem as a malicious use for its speed
    '''
    # # creating processes 
    # p1 = multiprocessing.Process(target=runP1, args=())
    # p2 = multiprocessing.Process(target=runP2, args=())
    # p3 = multiprocessing.Process(target=runP3, args=())
    # p4 = multiprocessing.Process(target=runP4, args=())
    # p5 = multiprocessing.Process(target=runP5, args=())
    # p6 = multiprocessing.Process(target=runP6, args=())

    # # starting process 1 
    # p1.start() 
    # # starting process 2 
    # p2.start() 
    # # starting process 3 
    # p3.start() 
    # # starting process 4 
    # p4.start() 
    # # starting process 5 
    # p5.start() 
    # # starting process 6 
    # p6.start() 

    # # wait until process 1 is finished 
    # p1.join() 
    # # wait until process 2 is finished 
    # p2.join() 
    # # wait until process 3 is finished 
    # p3.join() 
    # # wait until process 4 is finished 
    # p4.join() 
    # # wait until process 5 is finished 
    # p5.join() 
    # # wait until process 6 is finished 
    # p6.join() 
    
    '''
    Instead, run one by one
    '''
    runP1()
    runP2()
    runP3()
    runP4()
    runP5()
    runP6()
    
    # processes finished 
    print("Done!") 
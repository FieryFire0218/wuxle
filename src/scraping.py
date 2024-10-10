from bs4 import BeautifulSoup
import requests
from collections import deque
import json
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

start_url = "https://www.wuxiaworld.com/novels"

def scraper(driver, url):
    #wait for the content to load
    try:
        driver.get(url)
        WebDriverWait(driver, 3).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    except TimeoutException:
        print("Timed out waiting for page to load")
        return None

    #simulate scrolling
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # adjust the sleep time as needed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    #data
    novel_titles = []
    review_ratings = []
    for h1 in soup.find_all("h1", class_="font-set-b24 text-gray-t1 line-clamp-2 sm2:font-set-b32"):
        novel_titles.append(h1.text.strip())
    script_tags = soup.select("script[type='application/ld+json'][data-rh='true']")
    for script_tag in script_tags:
        json_data = json.loads(script_tag.text)
        rating_value = json_data.get('aggregateRating', {}).get('ratingValue')
        if rating_value is not None:
            review_ratings.append(rating_value)

    #print
    print("URL:", url)
    print("Data:")
    print("  Novel Titles:", novel_titles)
    print("  Review Ratings:", review_ratings)
    print("Format:")

    return {"url": url, "novel_titles": novel_titles, "review_ratings": review_ratings}
        
#    return novel_titles, review_ratings

def bfs(start_url, max_pages):
    visited = set() #keep track of visited URLs
    queue = deque([start_url]) #Queue to store URLs to be visited
    pages_scraped = 0
    scraped_novels = []

    #initialize
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Firefox(options=options)

    try:
        while queue and pages_scraped < max_pages:
            url = queue.popleft() #dequeue a URL
            if url in visited:
                continue
            print(f"Visiting: {url}")

            #simulate scrolling
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # adjust the sleep time as needed
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            result = scraper(driver, url)
            if result:
                scraped_novels.append(result)
                pages_scraped += 1
                visited.add(url)
            print(f"Pages scraped: {pages_scraped}")
            soup = BeautifulSoup(driver.page_source, "html.parser")
            for link in soup.find_all("a"):
                href = link.get("href")
                if href.startswith("/novel/") and href != "/novel/" and len(href.split("/")) == 3:
                    novel_url = "https://www.wuxiaworld.com" + href
                    if novel_url not in visited:
                        queue.append(novel_url)
            print(f"Pages scraped: {pages_scraped}")
            
    finally:
        driver.quit()

    return scraped_novels

#visited = bfs(start_url)
#print(visited)

#test
max_pages = 40
scraped_novels = bfs(start_url, max_pages)
print("Scraped Novels:")
for i, novel in enumerate(scraped_novels):
    print(f"Novel {i+1}:")
    print("  URL:", novel["url"])
    print("  Data:")
    print("    Novel Titles:", novel["novel_titles"])
    print("    Review Ratings:", novel["review_ratings"])

#result = requests.get(start_url) 
#result.encoding = "utf-8"
#doc = BeautifulSoup(result.text, "html.parser")

#print(doc.prettify().encode("utf-8"))

#with open("prettified_main.html", "w", encoding="utf-8") as file:
#    file.write(doc.prettify())
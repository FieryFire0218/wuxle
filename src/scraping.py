from bs4 import BeautifulSoup
import requests
from collections import deque
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start_url = "https://www.wuxiaworld.com/novels"

def scraper(url):
    #initialize
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    #wait for the content to load
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".chapter-content"))
    )

    #simulate scrolling
    for i in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".chapter-content"))
        )
    
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

    driver.quit()

    #print
    print("URL:", url)
    print("Data:")
    print("  Novel Titles:", novel_titles)
    print("  Review Ratings:", review_ratings)
    print("Format:")

    return {"url": url, "novel_titles": novel_titles, "review_ratings": review_ratings}
        
#    return novel_titles, review_ratings

def bfs(start_url, max_pages):
    visited = [] #keep track of visited URLs
    queue = deque([start_url]) #Queue to store URLs to be visited
    pages_scraped = 0
    scraped_novels = []

    #initialize
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    while queue and pages_scraped < max_pages:
        print(f"Pages Scraped: {pages_scraped}")
        url = queue.popleft() #dequeue a URL
        #novel_titles, review_ratings = scraper(url)
        try: 
            driver.get(url)
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            result = scraper(url, soup)
            if result is not None and result not in scraped_novels:
                scraped_novels.append(result)
            pages_scraped += 1
        except Exception as e:
            print(f"Error visiting url: {url} - {e}")
        #visited.append({"url": url, "titles": novel_titles, "ratings": review_ratings})

        #links to other novels
        links = soup.find_all("a", href=True)
        for link in links:
            href = link["href"]
            if href.startswith("/novel/") and href != "/novel/" and len(href.split("/")) == 3:
                novel_url = "https://www.wuxiaworld.com" + href  
                print(f"Found new url: {novel_url}")
                if novel_url not in visited:
                    queue.append(novel_url)
                    visited.append(novel_url)

    driver.quit()

    return scraped_novels

#visited = bfs(start_url)
#print(visited)

#test
max_pages = 20
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
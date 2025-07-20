from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from concurrent.futures import ProcessPoolExecutor, as_completed

start_url = "https://www.wuxiaworld.com/novels"


def scraper(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Firefox(options=options)
    try:
        try:
            driver.get(url)
            WebDriverWait(driver, 3).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            print(f"Timed out waiting for page to load: {url}")
            return None

        soup = BeautifulSoup(driver.page_source, "html.parser")
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
        print(f"Scraped: {url}")
        return {"url": url, "novel_titles": novel_titles, "review_ratings": review_ratings}
    finally:
        driver.quit()
        

def get_novel_urls(start_url):
    print("Loading main page and extracting novel URLs...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Firefox(options=options)
    try:
        driver.get(start_url)
        WebDriverWait(driver, 5).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        # Optionally scroll to load all content
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        soup = BeautifulSoup(driver.page_source, "html.parser")
        novel_urls = set()
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and href.startswith("/novel/") and href != "/novel/" and len(href.split("/")) == 3:
                novel_url = "https://www.wuxiaworld.com" + href
                novel_urls.add(novel_url)
        print(f"Found {len(novel_urls)} novel URLs.")
        return list(novel_urls)
    finally:
        driver.quit()

def parallel_scrape(novel_urls, max_workers=4):
    scraped_novels = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(scraper, url): url for url in novel_urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                if result:
                    scraped_novels.append(result)
            except Exception as e:
                print(f"Error scraping {url}: {e}")
    return scraped_novels


if __name__ == "__main__":
    # Get all novel URLs using Selenium
    novel_urls = get_novel_urls(start_url)
    # Scrape in parallel (adjust max_workers for your CPU)
    scraped_novels = parallel_scrape(novel_urls, max_workers=4)
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
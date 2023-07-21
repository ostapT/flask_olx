import concurrent

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

domain = "https://www.olx.ua/"
url = "https://www.olx.ua/uk/list/"
num_pages = 2
ads_per_page = 50


def parse_urls():
    links = []
    with ThreadPoolExecutor() as executor:
        future_to_page = {
            executor.submit(parse_page_urls, page): page
            for page in range(1, num_pages + 1)
        }
        for future in concurrent.futures.as_completed(future_to_page):
            links.extend(future.result())
    return links[:101]


def parse_page_urls(page):
    page_url = url + f"?page={page}"
    response = requests.get(page_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        ads = soup.find_all("div", class_="css-1sw7q4x")
        page_links = []
        for ad in ads:
            try:
                link = domain + ad.find("a", class_="css-rc5s2u")["href"]
                page_links.append(link)
            except (AttributeError, TypeError):
                continue
        return page_links
    else:
        return []


def process_ads(ads_links):
    ads_data = []
    with ThreadPoolExecutor() as executor:
        future_to_link = {
            executor.submit(scrape_ad_data, link): link for link in ads_links
        }
        for future in concurrent.futures.as_completed(future_to_link):
            ad_data = future.result()
            if ad_data is not None:
                ads_data.append(ad_data)
    return ads_data


def scrape_ad_data(link):
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        try:
            title = soup.find("h1", class_="css-bg3pmc er34gjf0").text.strip()
            price = soup.find("h2", class_="css-5ufiv7 er34gjf0").text.strip()
            image = soup.find(
                "div",
                class_="swiper-zoom-container"
            ).find("img")["src"]
            ad_data = {"title": title, "price": price, "image": image}
            return ad_data
        except (AttributeError, TypeError):
            return None
    else:
        return None

from time import sleep
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import requests

def scraping(chrome_path):
    options = Options()
    options.add_argument("--incognite")

    driver = webdriver.Chrome(executable_path=chrome_path, options=options)

    url = "https://search.yahoo.co.jp/image"
    driver.get(url)

    sleep(3)

    query = "プログラミング"
    search_box = driver.find_element_by_class_name("SearchBox__searchInput")
    search_box.send_keys(query)
    search_box.submit()

    sleep(3)

    height = 1000
    while(height < 2000):
        driver.execute_script("window.scrollTo(0,{})".format(height))
        height += 200

        sleep(1)

    elements = driver.find_elements_by_class_name("sw-Thumbnail")

    d_list = []
    for i, element in enumerate(elements, start=1):
        name = f"{query}_{i}"
        raw_url = element.find_element_by_class_name("sw-ThumbnailGrid__details").get_attribute("href")
        yahoo_image_url = element.find_element_by_tag_name("img").get_attribute("src")
        title = element.find_element_by_tag_name("img").get_attribute("alt")

        d = {
            "filename": name,
            "raw_url": raw_url,
            "yahoo_image_url": yahoo_image_url,
            "title": title
        }

        d_list.append(d)

        sleep(1)
        print(i)
    
    driver.quit()

    return d_list       

def make_csv(list):
    df = pd.DataFrame(list)
    df.to_csv("image_urls.csv")
    return df

def make_images():
    IMAGE_PATH = "images/"

    if(os.path.isdir(IMAGE_PATH)):
        print("exist")
    else:
        os.makedirs(IMAGE_PATH)

    df = pd.read_csv("image_urls.csv")
    for file_name, yahoo_image_url in zip (df.filename, df.yahoo_image_url):
        image = requests.get(yahoo_image_url)
        with open (IMAGE_PATH + file_name + ".png", "wb") as f:
            f.write(image.content)

        sleep(1)

def main():
    chrome_path =r"C:\Users\Yuki MATSUOKA\Desktop\python\scraping_image\chromedriver"

    d_list = scraping(chrome_path)
    
    df = make_csv(d_list)

    make_images()
      
if __name__ == '__main__':
    main()
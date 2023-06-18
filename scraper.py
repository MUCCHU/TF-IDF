import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 10)
all_problem_link = "https://leetcode.com/problemset/all/?page="

def get_links(page):
    driver.get(all_problem_link + str(page))
    time.sleep(10)
    element = driver.find_element(By.CLASS_NAME, "-mx-4")
    anchor_tags = element.find_elements(By.TAG_NAME, "a")
    links = []
    for anchor_tag in anchor_tags:
        link = anchor_tag.get_attribute("href")
        if "/solution" in link:
            continue
        links.append(link)
    return links

all_links = []
for i in range(1, 56):
    all_links += get_links(i)
    print("Page " + str(i) + " done")

all_links = list(set(all_links))
with open("links.txt", "w") as f:
    for link in all_links:
        f.write(link + "\n")
driver.quit()

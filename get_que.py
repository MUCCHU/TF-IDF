import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 10)
FOLDER = "problems"
title_class = ".mr-2.text-label-1"

idx = 1

def write_index(title):
    with open("index.txt", "a") as f:
        f.write(title + "\n")
    
def write_link(link):
    with open("qindex.txt", "a", encoding="utf-8", errors="ignore") as f:
        f.write(link + "\n")

def write_problem(name, problem):
    folder_name = os.path.join(FOLDER, name)
    os.makedirs(folder_name, exist_ok=True)
    file_path = os.path.join(folder_name, name + ".txt")
    with open(file_path, "w", encoding="utf-8", errors="ignore") as f:
        f.write(problem)


def getProblem(problem_link):
    driver.get(problem_link)
    try:
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_1l1MA")))
        title = driver.find_element(By.CSS_SELECTOR, title_class)
        write_index(title.text)
        write_link(problem_link)
        write_problem(str(idx), element.text)
    except Exception as e: 
        print(e)
        print("Error in " + problem_link)
        return False
    # print(title.text)
    return True;  


open("index.txt", "w").close()
open("qindex.txt", "w").close()
with open("links.txt", "r") as f:
    for link in f:
        success = getProblem(link.strip())
        if success:
            print("Done " + str(idx))
            idx += 1
        else:
            print("Failed " + str(idx))

driver.quit()
import os
from dotenv import load_dotenv

load_dotenv()

cookie = os.getenv('POE_COOKIE')
if not cookie:
    raise ValueError("POE_COOKIE environment variable not set")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time
from openai import OpenAI
import requests
import json
from itertools import islice
import os
from docx import Document

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)
longwait = WebDriverWait(driver, 120)
driver.get("https://poe.com")
# add cookies to login
script_dir = os.path.dirname(__file__)
# ------------------------------------------finish initialization----------------------------------------

def escapespace(content):
    single_line = "\n".join(content.splitlines())
    return single_line

def register(inputfile,cookies):
    for cookie in cookies:
        driver.add_cookie(cookie)
    cnt = 0
    with open(inputfile, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            Prompt = data["Prompt Leaking"]["public system prompt"]
            if len(Prompt) < 100:
                continue
            cnt += 1
            if cnt <= 36:
                continue
            if cnt > 50:
                break
            Name = data["Name"]
            Name = str(cnt) + "_" + Name
            if len(Name) > 20:
                Name = Name[:20]
            driver.get("https://poe.com/create_bot")
            time.sleep(1)
            select_prompt_bot = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/main/div/div/div/div/div/div[2]/button[1]")))
            select_prompt_bot.click()
            input_box = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/main/div/div/div/form/div[3]/div[1]/div[2]/input")))
            input_box.clear()
            input_box.send_keys(Name)
            description = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/div[1]/div/main/div/div/div/form/div[3]/div[2]/textarea")))
            description.send_keys("hello, I am a helpful assistant")
            prompt_box = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/main/div/div/div/form/div[4]/div[2]/div/div/div[2]/textarea")))
            prompt_box.send_keys(Prompt)
            announce = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/div[1]/div/main/div/div/div/form/div[7]/button")))
            announce.click()
            try:
                no_edit = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[22]/div/div/article/div/div[2]/button[2]")))
                no_edit.click()
            except:
                pass
            time.sleep(10)

            writefile = os.path.join(script_dir, "../poe.json")
            wdata = {}
            wdata["Name"] = Name
            wdata["URL"] = driver.current_url
            wdata["System Prompt"] = escapespace(Prompt)
            wdata["API Source"] = "Do not support API" #Store
            wdata["API Name"] = []
            wdata["OpenAPI"]  = ""
            wdata["Knowledge"]  = ""
            wdata["Contain PII"] = ""
            with open(writefile,'a',encoding='utf-8') as wfile:
                json.dump(wdata, wfile, ensure_ascii=False)
                wfile.write("\n")

def extract_index(filename):
    try:
        return int(filename.split("_")[0])
    except ValueError:
        return float('inf')
# folder_path = os.path.join(script_dir, "../knowledge_file/containPII")
# folder_path2 = os.path.join(script_dir, "../knowledge_file/noPII")
# file_path_PII = sorted(
#     [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))],
#     key=lambda x: extract_index(os.path.basename(x))
# )
# file_path_no = sorted(
#     [os.path.join(folder_path2, f) for f in os.listdir(folder_path2) if os.path.isfile(os.path.join(folder_path2, f))],
#     key=lambda x: extract_index(os.path.basename(x))
# )

def uploadknowledge(inputfile,cookies):
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://poe.com/explore?category=AI")    
    cnt = 0
    with open(inputfile, 'r', encoding='utf-8') as file:
        for line in file:
            cnt += 1
            if cnt <= 5:
                continue
            data = json.loads(line)
            URL = "https://poe.com/edit_bot?bot=" + data["Name"]
            driver.get(URL)
            if cnt > 50:
                break

            time.sleep(200)


            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  
            time.sleep(1)
            # announce = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/main/div/div/div/form/div[4]/div[2]/div/div/section/label/div[2]/span")))
            # announce.click()
            time.sleep(2)
            announce = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/main/div/div/div/form/div[7]/button")))
            announce.click()
            time.sleep(2)
            continue
            # for i in range(3):
            #     driver.execute_script("window.scrollBy(0, 1000);")
            #     time.sleep(5)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  
            time.sleep(5)
            # body = driver.find_element(By.TAG_NAME, 'body')
            # body.send_keys(Keys.PAGE_DOWN)
            
            add_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/main/div/div/div/form/div[4]/div[2]/div/div/section/button[2]")))
            add_button.click()
            time.sleep(6)
            # file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "MainBody_fileInput__lIgtq")))
            file_input = driver.find_element(By.CSS_SELECTOR, ".MainBody_fileInput__lIgtq")
            if cnt <= 25:
                path = file_path_PII[cnt-1]
                print(path)
                data["Contain PII"] = True
            else:
                path = file_path_no[cnt-26]
                data["Contain PII"] = False
            file_input.send_keys(path)

            doc = Document(path)
            text = "\n".join([para.text for para in doc.paragraphs])
            data["Knowledge"] = text
            # deletebutton = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[21]/div/div/article/div/header/button")))
            # deletebutton.click()
            time.sleep(20)
            announce = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/main/div/div/div/form/div[7]/button")))
            announce.click()
            time.sleep(5)
            writefile = os.path.join(script_dir, "../new_poe.json")
            wdata = data
            with open(writefile,'a',encoding='utf-8') as wfile:
                json.dump(wdata, wfile, ensure_ascii=False)
                wfile.write("\n")



inputfile = "ground_truth/poe.json"
cookies = []
for item in cookie.split('; '):
    name, value = item.split('=', 1)
    cookies.append({"name": name, "value": value})
try:
    uploadknowledge(inputfile, cookies)
# register(inputfile, cookies)
finally:
    driver.quit()







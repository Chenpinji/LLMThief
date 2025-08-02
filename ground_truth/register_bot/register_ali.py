import os
from dotenv import load_dotenv

load_dotenv()

cookie = os.getenv('ALI_COOKIE')
if not cookie:
    raise ValueError("ALI_COOKIE environment variable not set")

import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time
from openai import OpenAI
import requests
import json
from itertools import islice
from docx import Document


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)
longwait = WebDriverWait(driver, 120)
driver.get("https://tongyi.aliyun.com/qianwen/")
# add cookies to login

# ------------------------------------------finish initialization----------------------------------------

def escapespace(content):
    single_line = "\n".join(content.splitlines())
    return single_line


def register(inputfile, cookies):
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.get("https://tongyi.aliyun.com/qianwen/")
    time.sleep(30)
    cnt = 0
    with open(inputfile, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            # Prompt = data["Prompt Leaking"]["public system prompt"]
            # if len(Prompt) < 100:
            #     continue
            cnt += 1
            if cnt <= 0:
                continue
            if cnt > 50:
                break
            Name = data["Name"]
            Name = str(cnt) + "_" + Name
            if len(Name) > 20:
                Name = Name[:20]
            driver.get("https://www.tongyi.com/creations/agent/home?type=MyAgent")
            time.sleep(1)
            create_bot = wait.until(EC.presence_of_element_located(
                # (By.CSS_SELECTOR, "#root > div > div > div.sc-fWnslK.eQLGpS.pageContentWrap___D3YX2 > div > div > div > div > div.sc-iQQCXo.ioPsyE > button > span")))
                (By.CSS_SELECTOR,
                 "#root > div > div > div.sc-fWnslK.eQLGpS.pageContentWrap___D3YX2 > div > div > div > div > div.sc-jaXxmE.dNmSPO > div > div > button")))
            create_bot.click()

            time.sleep(1)
            free = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "div.header--me1SvFCQ > div")))
            free.click()

            time.sleep(1)
            input_box = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#name")))
            input_box.clear()
            input_box.send_keys(Name)
            time.sleep(1)

            generator = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.ant-modal-body > div > div > form > div:nth-child(2) > div > div.ant-col.ant-form-item-label.css-tqs4ck > label > div > div")))
            generator.click()

            time.sleep(30)

            prompt_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                    "#instructions")))
            Prompt = prompt_box.text

            time.sleep(1)
            announce = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.ant-modal-body > div > div > div.btnContainer--I2Eisq3i > button.cursor-pointer.whitespace-nowrap.select-none.tongyi-ui-button.tongyi-ui-button-primary.btn--ywfFnBG3")))
            announce.click()

            time.sleep(10)

            writefile = "ground_truth/ali.json"
            wdata = {}
            wdata["Name"] = Name
            wdata["URL"] = driver.current_url
            wdata["System Prompt"] = escapespace(Prompt)
            wdata["API Source"] = "Do not support API"  # Store
            wdata["API Name"] = []
            wdata["OpenAPI"] = ""
            wdata["Knowledge"] = ""
            wdata["Contain PII"] = ""
            with open(writefile, 'a', encoding='utf-8') as wfile:
                json.dump(wdata, wfile, ensure_ascii=False)
                wfile.write("\n")


def extract_index(filename):
    # 提取开头的数字，比如从 "12_something.txt" 提取出 12
    try:
        return int(filename.split("_")[0])
    except ValueError:
        return float('inf')


folder_path = "ground_truth/knowledge_file/containPII"
folder_path2 = "ground_truth/knowledge_file/noPII"
file_path_PII = sorted(
    [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))],
    key=lambda x: extract_index(os.path.basename(x))
)
file_path_no = sorted(
    [os.path.join(folder_path2, f) for f in os.listdir(folder_path2) if os.path.isfile(os.path.join(folder_path2, f))],
    key=lambda x: extract_index(os.path.basename(x))
)


def uploadknowledge(inputfile, cookies):
    # for cookie in cookies:
    #     driver.add_cookie(cookie)
    # driver.get("https://poe.com/explore?category=AI")
    # time.sleep(30)
    cnt = 0
    with open(inputfile, 'r', encoding='utf-8') as file:
        for line in file:
            cnt += 1
            if cnt <= 0:
                continue
            data = json.loads(line)
            URL = data['URL']
            driver.get(URL)

            if cnt > 50:
                break
            # for i in range(3):
            #     driver.execute_script("window.scrollBy(0, 1000);")
            #     time.sleep(5)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 滚动到底部
            # time.sleep(1)
            # body = driver.find_element(By.TAG_NAME, 'body')
            # body.send_keys(Keys.PAGE_DOWN)

            add_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                    "#ice-container > div > div > div.content--kjyzC7S2 > div > div.sc-dNpohg.kugtUH.pageContentWrap--tk5Zq7zc > div > div > div.sc-fPyrPm.hFXIVD > div > div.sc-cLAbsH.gGgXZM > div > button.ant-btn.css-1r287do.ant-btn-default.ant-btn-icon-only.ty-button.ant-dropdown-trigger")))
            add_button.click()
            time.sleep(1)
            add_button = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                    "/html/body/div[6]/div/ul/li[2]")))
            add_button.click()
            time.sleep(5)
            add_button = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                    "/html/body/div[8]/div/div[2]/div/div[2]/div/div[2]/div/div/form/div[4]/div[1]")))
            add_button.click()

            file_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div/div[2]/div/div[2]/div/div[2]/div/div/form/div[4]/div[2]/div[5]/div/div[2]/div/div/span/div[1]/span")))
            # file_input = driver.find_element(By.CSS_SELECTOR, "")
            if cnt <= 25:
                path = file_path_PII[cnt - 1]
                print(path)
                data["Contain PII"] = True
            else:
                path = file_path_no[cnt - 26]
                data["Contain PII"] = False
            # file_input.send_keys(path)

            doc = Document(path)
            text = "\n".join([para.text for para in doc.paragraphs])
            data["Knowledge"] = text
            deletebutton = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[21]/div/div/article/div/header/button")))
            deletebutton.click()
            time.sleep(20)
            announce = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "body > div:nth-child(33) > div > div.ant-modal-wrap > div > div:nth-child(2) > div > div.ant-modal-body > div > div > div.btnContainer--I2Eisq3i > button.cursor-pointer.whitespace-nowrap.select-none.tongyi-ui-button.tongyi-ui-button-primary.btn--ywfFnBG3")))
            announce.click()
            time.sleep(5)
            writefile = "ground_truth/new_ali.json"
            wdata = data
            with open(writefile, 'a', encoding='utf-8') as wfile:
                json.dump(wdata, wfile, ensure_ascii=False)
                wfile.write("\n")


inputfile = r"ground_truth/ali.json"
# cookie = r'__itrace_wid=3581bb2c-533a-41fa-8523-507dcc786722; tongyi_sso_ticket=8Gz1g_BynogsOH1apRX0qcdzyjC7$oxMQnmJwzJkcUrP34J3fCOoRVF8UxcPezOUPuY_TuYPpfbz0; UM_distinctid=1971b6843cd69a-099158242b653b-26001851-144000-1971b6843ce118f; cna=IBm/IJacy1YCATowGzlIbwod; xlly_s=1; XSRF-TOKEN=32672211-4e56-4332-8229-96c85382987f; CNZZDATA1281397965=671673309-1748511507-%7C1748514568; tfstk=gOJjnM4Q2r4ju9BTfsmzFrNwkB6s80kFDls9xhe4XtBvXOt9jN7V_NR5XULyuoR2XNT6zaYZmGlD1OTJzI7v7tzsCU_lQZJ2gCOWoHC25hmcXNL95NRqav-DmOXt8OMELnciNSHWhOUw2tjwyz03Tv-DmuBt82kELlZRvtg1WFCAezIFyGF9WsU-VGIak5evW0i5rGBOWFBtVTQlXOhbC4soGZKj0SvSjUXNJnQ7BRZhcsQKKawTBLsb8wKxxRe9Fi1XedBU95126HfH3HH_Et-BwTI6IDF156O93TpxyvCl6LLR2EoasgO6XpXcdlHvVt_f9dToIDYpVhdFNLoKKt6AkCWDbkg2VKT2mLtaX7Bf3Q1Bh9H3kNRyAds6IVDWRhKH6_9_lgk0LwamP5Z5tRI580i7s52nlRUgLfeqasIl4poSVrNGMgj580i7s5fAqg5EV0abs; isg=BJOTxi-K_4LmBrPWHvR2bcyOIhe9SCcKPkqW-0Ww77LpxLNmzRi3WvEG_DSq_38C'
cookies = []
for item in cookie.split('; '):
    name, value = item.split('=', 1)
    cookies.append({"name": name, "value": value})
try:
    # uploadknowledge(inputfile, cookies)
    register(inputfile, cookies)
finally:
    driver.quit()







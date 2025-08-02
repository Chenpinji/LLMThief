import os
from dotenv import load_dotenv

load_dotenv()

cookie = os.getenv('COZE_COOKIE')
if not cookie:
    raise ValueError("COZE_COOKIE environment variable not set")

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
driver.get("https://www.coze.com/")
# add cookies to login

# ------------------------------------------finish initialization----------------------------------------

def escapespace(content):
    single_line = "\n".join(content.splitlines())
    return single_line

def remove_non_bmp(text):
    return ''.join(c for c in text if ord(c) <= 0xFFFF)

def register(inputfile, cookies):
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.get("https://www.coze.com/home")
    main_window = driver.current_window_handle
    time.sleep(5)
    confirm = wait.until(EC.presence_of_element_located(
        (By.XPATH,
         "/html/body/div[5]/div/button")))
    confirm.click()
    confirm = wait.until(EC.presence_of_element_located(
        (By.XPATH,
         "/html/body/div[6]/div/div/div[1]/div/div[2]/div/div[2]/button[1]/span")))
    confirm.click()
    cnt = 0
    with open(inputfile, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            Prompt = remove_non_bmp(data["Prompt Leaking"]["public system prompt"])
            if len(Prompt) < 100:
                continue
            if len(Prompt) > 2000:
                continue
            cnt += 1
            if cnt <= 0:
                continue
            if cnt > 50:
                break
            Name = data["Name"]
            Name = str(cnt) + "_" + Name
            if len(Name) > 20:
                Name = Name[:20]
            driver.get("https://www.coze.com/home")
            time.sleep(2)
            create_bot = wait.until(EC.presence_of_element_located(
                # (By.CSS_SELECTOR, "#root > div > div > div.sc-fWnslK.eQLGpS.pageContentWrap___D3YX2 > div > div > div > div > div.sc-iQQCXo.ioPsyE > button > span")))
                (By.XPATH,
                 "/html/body/div[1]/div/div/div/div[1]/div/div[1]/div[1]/div/button/span")))
            create_bot.click()

            time.sleep(2)
            create_bot = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "#semi-modal-body > div > div.h-full.w-full.overflow-y-auto > div > div:nth-child(1) > span > span")))
            create_bot.click()

            time.sleep(2)
            input_box = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#name")))
            input_box.clear()
            input_box.send_keys(Name)
            time.sleep(1)

            confirm = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[5]/div/div[2]/div/div/div[3]/div/button[2]/span")))
            confirm.click()

            wait.until(lambda d: len(driver.window_handles) > 1)
            new_window_1 = [w for w in driver.window_handles if w != main_window][0]
            driver.switch_to.window(new_window_1)

            time.sleep(3)
            try:
                model_select = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/div[1]/span[1]/span/div/button/span/div/span[2]")))
                model_select.click()

                time.sleep(4)
                model_select = wait.until(EC.presence_of_element_located(
                    (By.XPATH,
                     "/html/body/div[10]/div/div/div/div/div/div/div[2]/section[4]/article[1]/span")))
                model_select.click()
            except:
                pass

            time.sleep(3)
            prompt_box = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                    "/html/body/div[2]/div/div/div/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div[1]")))
            prompt_box.send_keys("This is a Test.")
            prompt_box.clear()
            time.sleep(1)
            prompt_box.send_keys(Prompt)

            time.sleep(3)
            announce = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div/div/div/div/div/div/div/div[1]/div[2]/div[3]/div[2]/button/span")))
            announce.click()

            time.sleep(3)
            announce = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[11]/div/div[2]/div/div/div[3]/button[1]/span")))
            announce.click()

            time.sleep(2)
            announce = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div/div/div/div/div/div[1]/div/button/span")))
            announce.click()

            time.sleep(1)
            jump = True
            try:
                announce = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/section/div[2]/div/div/div/div/div/div[2]/table/tbody/tr/td[2]/div/button[1]/span")))
                announce.click()
            except:
                announce = wait.until(EC.presence_of_element_located(
                    (By.XPATH,
                     "/html/body/div[1]/div/div/div/div/div/div[1]/div/button")))
                announce.click()
                jump = False

            if jump:
                wait.until(lambda d: len(driver.window_handles) > 2)
                new_window_2 = [w for w in driver.window_handles if w not in [main_window, new_window_1]][0]
                driver.switch_to.window(new_window_2)

            time.sleep(10)

            writefile = "ground_truth/coze.json"
            wdata = {}
            wdata["Name"] = Name
            wdata["URL"] = driver.current_url
            wdata["System Prompt"] = escapespace(Prompt)
            wdata["API Source"] = "Store"  # Store
            wdata["API Name"] = []
            wdata["OpenAPI"] = ""
            wdata["Knowledge"] = ""
            wdata["Contain PII"] = ""
            with open(writefile, 'a', encoding='utf-8') as wfile:
                json.dump(wdata, wfile, ensure_ascii=False)
                wfile.write("\n")

            if jump:
                driver.close()  
                driver.switch_to.window(new_window_1)
            driver.close()  
            driver.switch_to.window(main_window)


def extract_index(filename):
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

APIfolder1  = "ground_truth/API_file/without_auth"
APIfolder2 = "ground_truth/API_file/with_auth"
API_path_1 = [os.path.join(APIfolder1, f) for f in os.listdir(APIfolder1) if os.path.isfile(os.path.join(APIfolder1, f))]
API_path_2 = [os.path.join(APIfolder2, f) for f in os.listdir(APIfolder2) if os.path.isfile(os.path.join(APIfolder2, f))]



def uploadknowledge(inputfile, cookies):
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://www.coze.com/home")
    time.sleep(5)
    cnt = 0
    with open(inputfile, 'r', encoding='utf-8') as file:
        for line in file:
            cnt += 1
            if cnt <= 25:
                continue
            if cnt > 50:
                break
            data = json.loads(line)
            URL = data['URL']
            driver.get(URL)
            time.sleep(5)
            # for i in range(3):
            #     driver.execute_script("window.scrollBy(0, 1000);")
            #     time.sleep(5)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  
            # time.sleep(1)
            # body = driver.find_element(By.TAG_NAME, 'body')
            # body.send_keys(Keys.PAGE_DOWN)

            add_button = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                    "/html/body/div[2]/div/div/div/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[2]/div/header/div[2]/div/div/button")))
            add_button.click()
            time.sleep(1)
            add_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                    "#semi-modal-body > div > div.qFmAHT9G5ssaoauT > div.\!pt-\[16px\].SZ4wd5vmovSX7Kzm > div.flex.flex-col.gap-\[16px\].zySvgdSolZkELOYy > button > span")))
            add_button.click()
            time.sleep(1)

            # add_button = wait.until(EC.presence_of_element_located((By.XPATH,
            #                                                         "/html/body/div[8]/div/div[2]/div/div[2]/div/div[2]/div/div/form/div[4]/div[1]")))
            # add_button.click()
            #
            # file_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div/div[2]/div/div[2]/div/div[2]/div/div/form/div[4]/div[2]/div[5]/div/div[2]/div/div/span/div[1]/span")))
            # file_input = driver.find_element(By.CSS_SELECTOR, "")
            if cnt <= 25:
                path = file_path_PII[cnt - 1]
                print(path)
                data["Contain PII"] = True
            else:
                path = file_path_no[cnt - 26]
                data["Contain PII"] = False

            input_box = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#name")))
            input_box.clear()
            input_box.send_keys(os.path.basename(path))
            time.sleep(1)

            # file_input.send_keys(path)

            doc = Document(path)
            text = "\n".join([para.text for para in doc.paragraphs])
            data["Knowledge"] = text
            # deletebutton = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[21]/div/div/article/div/header/button")))
            # deletebutton.click()
            time.sleep(30)
            # announce = wait.until(EC.presence_of_element_located(
            #     (By.CSS_SELECTOR,
            #      "body > div:nth-child(33) > div > div.ant-modal-wrap > div > div:nth-child(2) > div > div.ant-modal-body > div > div > div.btnContainer--I2Eisq3i > button.cursor-pointer.whitespace-nowrap.select-none.tongyi-ui-button.tongyi-ui-button-primary.btn--ywfFnBG3")))
            # announce.click()
            # time.sleep(5)
            writefile = "ground_truth/new_coze.json"
            wdata = data
            with open(writefile, 'a', encoding='utf-8') as wfile:
                json.dump(wdata, wfile, ensure_ascii=False)
                wfile.write("\n")

def uploadAPI(inputfile, cookies):
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://www.coze.com/space/7372450950520307719/library")
    time.sleep(5)
    main_window = driver.current_window_handle
    cnt = 0
    with open(inputfile, 'r', encoding='utf-8') as file:
        for line in file:
            cnt += 1
            if cnt <= 45:
                continue
            if cnt > 50:
                break
            wdata = json.loads(line)
            URL = wdata['URL']
            driver.get(URL)
            # if 'space' not in URL:
            #     time.sleep(10)
            time.sleep(5)

            settings = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#root > div > div > div > div > div > div.VUyAFbBzTUm9repe.bvowuYyKquUSdPZU > div > div:nth-child(2) > div > div.bg-white.rounded-\[8px\] > button")))
            settings.click()
            time.sleep(1)

            develop = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                  r"/html/body/div[5]/div/div/div/div/div/div/button[1]")))
            develop.click()
            time.sleep(3)

            wait.until(lambda d: len(driver.window_handles) > 1)
            new_window_1 = [w for w in driver.window_handles if w != main_window][0]
            driver.switch_to.window(new_window_1)

            knowledge_settings = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                 r"#setting_area_scroll > div:nth-child(3) > div.AraUvCorNhEMKJxd > div.KTlR16G4JIYtZJfr > button > span > span.semi-button-content-right")))
            knowledge_settings.click()
            time.sleep(5)

            # try:
            #     knowledge_settings = wait.until(EC.presence_of_element_located((By.XPATH,
            #                                                                     r"/html/body/div[8]/div/div/div/div/div/div/div[8]/div[2]/div[2]/div/input")))
            #     knowledge_settings.click()
            #     time.sleep(1)
            # except:
            #     pass

            publish = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                r"#root > div > div > div > div > div > div > div > div.J1b_R9RP0wUtWxb0.coz-bg-primary > div.flex.items-center.gap-2 > div:nth-child(3) > div:nth-child(2) > button > span > span")))
            publish.click()
            time.sleep(7)

            publish = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                 r"#root > div > div > div > div > div > div.VUyAFbBzTUm9repe.dA_T1I4ewGU7Evof > div > button > span")))
            publish.click()
            time.sleep(7)


            driver.close() 
            driver.switch_to.window(main_window)
            # continue
            time.sleep(1)
            # for i in range(3):
            #     driver.execute_script("window.scrollBy(0, 1000);")
            #     time.sleep(5)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 滚动到底部
            # time.sleep(1)
            # body = driver.find_element(By.TAG_NAME, 'body')
            # body.send_keys(Keys.PAGE_DOWN)

            # add_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
            #                                                         "#root > div > div > div > div.coz-layout.flex-1.relative.flex.flex-col.overflow-x-hidden.coz-bg-plus > div > div.coz-layout-header.q8Dxk4ZC8k9wG2Mj.pb-0 > div > div.flex.items-center.justify-between.mb-\[16px\] > button > span > span")))
            # add_button.click()
            time.sleep(1)
            add_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                    "#setting_area_scroll > div:nth-child(1) > div.collapse-panel.collapse-panel-plugin > div > header > div.e138gczjVsAX2hLj.grid.grid-flow-row.gap-x-\[2px\] > div.coz-icon-button.coz-icon-button-small.coz-icon-button-secondary > button > span")))
            add_button.click()
            time.sleep(10)

            plugins = wait.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[2]/div/div/div/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[2]/div/div/div/div/div/div/div")))
            all_plugin_texts = []
            for plugin in plugins:
                title = plugin.find_element(By.XPATH, "./div[1]/div/div")
                all_plugin_texts.append(title.text)

            wdata["API Name"] = all_plugin_texts
            print(all_plugin_texts)
            time.sleep(2)
            publish = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.flex.items-center.gap-2 > div:nth-child(3) > div:nth-child(2) > button > span")))
            publish.click()
            time.sleep(20)

            if 'space' in URL:
                wdata['URL'] = driver.current_url

            writefile = "ground_truth/new_coze_api.json"
            with open(writefile, 'a', encoding='utf-8') as wfile:
                json.dump(wdata, wfile, ensure_ascii=False)
                wfile.write("\n")

inputfile = r"ground_truth/coze.json"

cookies = []
for item in cookie.split('; '):
    name, value = item.split('=', 1)
    cookies.append({"name": name, "value": value})
try:
    # uploadknowledge(inputfile, cookies)
    uploadAPI(inputfile, cookies)
    # for i in range(12, 51):
        # service = Service(ChromeDriverManager().install())
        # driver = webdriver.Chrome(service=service)
        # wait = WebDriverWait(driver, 20)
        # longwait = WebDriverWait(driver, 120)
        # driver.get("https://www.coze.com/")
    # register(inputfile, cookies)
        # driver.quit()
finally:
    driver.quit()
    pass






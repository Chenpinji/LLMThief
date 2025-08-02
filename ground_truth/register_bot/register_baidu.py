import os
from dotenv import load_dotenv

load_dotenv()

cookie = os.getenv('BAIDU_COOKIE')
if not cookie:
    raise ValueError("BAIDU_COOKIE environment variable not set")

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
from selenium.webdriver.common.action_chains import ActionChains

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)
longwait = WebDriverWait(driver, 120)
driver.get("https://agents.baidu.com/center")
# add cookies to login

# ------------------------------------------finish initialization----------------------------------------

from pathlib import Path


base_dir = Path(__file__).resolve().parent.parent  

folder_path = base_dir / "knowledge_file" / "containPII"
folder_path2 = base_dir / "knowledge_file" / "noPII"
def extract_index(filename):
    try:
        return int(filename.split("_")[0])
    except ValueError:
        return float('inf')

def get_normalized_files(folder):
    return sorted(
        [str((folder / f).resolve().as_posix()) for f in os.listdir(folder) if (folder / f).is_file()],
        key=lambda x: extract_index(Path(x).name)
    )

file_path_PII = get_normalized_files(folder_path)
file_path_no = get_normalized_files(folder_path2)

# print(file_path_PII)
# print("!!!!!!")


def escapespace(content):
    single_line = "\n".join(content.splitlines())
    return single_line


def register(inputfile, cookies):
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.get("https://agents.baidu.com/center")
    time.sleep(2)
    cnt = 0
    with open(inputfile, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            wdata = {}
            Prompt = data["Prompt Leaking"]["public system prompt"]
            if len(Prompt) < 100:
                continue
            cnt += 1
            if cnt <= 48:
                continue
            if cnt > 50:
                break
            Name = data["Name"]
            Name = str(cnt) + Name
            wdata["Name"] = Name
            wdata["System Prompt"] = escapespace(Prompt)
            # if len(Name) > 20:
            #     Name = Name[:20]
            driver.get("https://agents.baidu.com/agent/prompt/quickStart")
            time.sleep(1)
            # skip = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/main/div/p")))
            # skip.click()
            name_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/main/div/div/div[1]/div/input")))
            name_input.send_keys(Name)
            time.sleep(2)
            set_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/main/div/div/div[2]/div/span/div/div/div/div")))
            # set_input.send_keys(Prompt)
            set_input.click()
            time.sleep(1)
            if len(Prompt) > 500:
                temp = Prompt[:500]
            else:
                temp = Prompt
            driver.execute_script("""
                arguments[0].innerText = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, set_input, temp)
            time.sleep(2)
            create_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/main/div/div/button")))
            create_button.click()
            while driver.current_url == "https://agents.baidu.com/agent/prompt/quickStart":
                time.sleep(1)
            # name_box = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/form/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div/span/input")))
            # name_box.clear()
            # name_box.send_keys(Name)
            # time.sleep(1)
            intro_box = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/form/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[1]/div/div[5]/div[1]/div/div[1]/div/span/textarea")))
            # intro_box.clear()
            intro = "我是智能体" + Name
            driver.execute_script("""
                arguments[0].innerText = '';
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, intro_box)
            # prompt_box.send_keys(Prompt)
            driver.execute_script("""
                arguments[0].innerText = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, intro_box, intro)


            time.sleep(5)
            prompt_box = wait.until(EC.presence_of_element_located(
                (By.XPATH, "html/body/div[1]/div/form/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[1]/div/span/div[3]/div[1]/div/div")))
            # prompt_box.clear()
            driver.execute_script("""
                arguments[0].innerText = '';
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, prompt_box)
            # prompt_box.send_keys(Prompt)
            driver.execute_script("""
                arguments[0].innerText = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, prompt_box, Prompt)
            time.sleep(5)

            url = "https://agents.baidu.com/agent/preview/" + driver.current_url.split("appId=")[1]
            wdata["URL"] = url

            # add_API_button = wait.until(EC.presence_of_all_elements_located((By.XPATH,"                /html/body/div[1]/div/form/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[2]/div[4]/div/div/div/div/div/span/div/div[1]/div/div[1]/div[2]/div/button/span/span")))
            # add_API_button.click()
            # /html/body/div[9]/div/div[2]/div/div[2]/div[2]/div[1]/div[1]

            knowledge_button = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div/form/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[2]/span/div/div[1]/div/div[1]/div[2]/div/button/span")))
            
            knowledge_button.click()
            time.sleep(3)
            new_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[2]/div/div[2]/div[3]/div/div[1]/div[2]/span[2]")))
            # /html/body/div[7]/div/div[2]/div/div[2]/div[3]/div/div[1]/div[2]/span[2]
            new_button.click()
            time.sleep(5)
            knowledge_name_box = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div/div[2]/div/div[2]/div[2]/form/div[2]/div/div[2]/div/div/span/input")))
            if cnt <= 25:
                path = file_path_PII[cnt - 1]
                print(path)
                wdata["Contain PII"] = True
            else:
                path = file_path_no[cnt - 26]
                print(path)
                wdata["Contain PII"] = False
            knowledge_name = path.split("/")[-1].split(".pdf")[0]
            print(knowledge_name)
            knowledge_name_box.send_keys(knowledge_name)

            import fitz  # pip install PyMuPDF
            try:
                doc = fitz.open(path)
                text = "\n".join([page.get_text() for page in doc])
                wdata["Knowledge"] = text
                # print("text=",text)
            except Exception as e:
                print(f"Read PDF Fail: {e}")
                wdata["Knowledge"] = ""
            # doc = Document(path)
            # text = "\n".join([para.text for para in doc.paragraphs])
            # wdata["Knowledge"] = text
            input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div/div[2]/div/div[2]/div[2]/form/div[5]/div/div[2]/div/div/span/div/span/input")))
            input.send_keys(path)
            time.sleep(5)
            try:
                confirm_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div/div[2]/div/div[2]/div[3]/button[2]")))
                confirm_button.click()
            except:
                confirm_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[9]/div/div[2]/div/div[2]/div[3]/button[2]")))
                confirm_button.click()
            time.sleep(5)
            # /html/body/div[10]/div/div[2]/div/div[2]/div[3]/div/div[2]/button[2]/span
            try:
                OK_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[2]/div/div[2]/div[3]/div/div[2]/button[2]")))
                OK_button.click()
            except:
                OK_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div/div[2]/div/div[2]/div[3]/div/div[2]/button[2]")))
                OK_button.click()
            time.sleep(25)
            # /html/body/div[8]/div/div[2]/div/div[2]/div[3]/div/div[2]/button[2]/span
            # /html/body/div[9]/div/div[2]/div/div[2]/div[3]/button[2]/span

            setting = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/form/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[2]/span/div/div[1]/div/div[1]/div[2]/div/span")))
            setting.click()
            time.sleep(1)

            force = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[2]/div/div[2]/div[2]/div/form/div[1]/div[2]/div[1]/label[2]/span[1]/input")))
            force.click()
            time.sleep(1)

            confirm = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[2]/div/div[2]/div[3]/div/button[2]")))
            confirm.click()
            time.sleep(5)
            announce = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/form/div/div[1]/div[3]/div[2]/button")))
            announce.click()
            time.sleep(5)
            private = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div/div/div[1]/div[1]/div[3]/div/div[4]")))
            private.click()
            time.sleep(1)
            submit = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[1]/header/div[2]/div[1]/button")))
            submit.click()
            time.sleep(3)
            
            
            writefile = "~/Configuration-Leaking-on-LLM-APP-Store/ground_truth/baidu.json"
            wdata["API Source"] = "Mine"
            wdata["API Name"] = []
            wdata["OpenAPI"] = ""
            with open(writefile, 'a', encoding='utf-8') as wfile:
                json.dump(wdata, wfile, ensure_ascii=False)
                wfile.write("\n")







def select_API():
    inputfile = "~/Configuration-Leaking-on-LLM-APP-Store/ground_truth/baidu.json"
    cookies = []
    for item in cookie.split('; '):
        name, value = item.split('=', 1)
        cookies.append({"name": name, "value": value})
    try:
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get("https://agents.baidu.com/center")
        time.sleep(2)
        with open(inputfile,'r',encoding='utf-8') as file:
            cnt = 0
            for line in file:
                data = json.loads(line)
                cnt += 1
                url = "https://agents.baidu.com/agent/prompt/edit?appId=" + data["URL"].split("/")[-1] + "&activeTab=create"
                driver.get(url)
                add_API = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/form/div/div[2]/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[2]/div[4]/div/div/div/div/div/span/div/div[1]/div/div[1]/div[2]/div/button")))
                add_API.click()
                
                time.sleep(2)
                print(f"/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div/div[{cnt}]/div[1]/div")
                # /html/body/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/div[1]/div
                box = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div/div[{cnt}]/div[1]/div")))
                box.click()
                time.sleep(3)
                try:
                    select = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div/div[{cnt}]/div[2]/div/div/div[2]/label/span[1]/input")))
                    select.click()
                except:
                    select = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div/div[{cnt}]/div[2]/div/div/div[2]/label[1]/span[1]/input")))
                    select.click()
                time.sleep(2)  
                APIname = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div/div[{cnt}]/div[1]/span/div/div/p[1]/span[1]")))
                func_name = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[5]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div/div[{cnt}]/div[2]/div/div/div[2]/label/span[2]/div/div/span[1]")))
                data["API Name"].append(APIname.text + "-" + func_name.text)
                sure_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div/div[2]/div/div[2]/div[3]/div/button[3]")))
                sure_button.click()
                time.sleep(2)
                announce = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/form/div/div[1]/div[3]/div[2]/button")))
                announce.click()
                time.sleep(2)
                submit = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[1]/header/div[2]/div[1]/button")))
                submit.click()
                time.sleep(2)
                with open("~/Configuration-Leaking-on-LLM-APP-Store/ground_truth/baidu_new.json",'a',encoding='utf-8') as wfile:
                    json.dump(data, wfile, ensure_ascii=False)
                    wfile.write("\n")
    finally:        
        driver.quit()


def uploadpromptandknowledge():
    inputfile = "~/Configuration-Leaking-on-LLM-APP-Store/preparation/baidu_pre/baidu_attack_instruction_pre.json"
    
    
    cookies = []
    for item in cookie.split('; '):
        name, value = item.split('=', 1)
        cookies.append({"name": name, "value": value})
        print("!",name,"value:",value)
    try:
        # uploadknowledge(inputfile, cookies)
        register(inputfile, cookies)
    finally:
        driver.quit()


def get_URL():
    inputfile = "~/Configuration-Leaking-on-LLM-APP-Store/ground_truth/baidu.json"
    
    cookies = []
    for item in cookie.split('; '):
        name, value = item.split('=', 1)
        cookies.append({"name": name, "value": value})
    try:
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get("https://agents.baidu.com/center")
        time.sleep(2)
        with open(inputfile,'r',encoding='utf-8') as file:
            cnt = 0
            while cnt < 20: # 20 20 10
                # data = json.loads(line)
                cnt += 1
                if cnt <= 6:
                    continue
                # url = "https://agents.baidu.com/agent/prompt/edit?appId=" + data["URL"].split("/")[-1] + "&activeTab=create"
                driver.get("https://agents.baidu.com/agent/list/codeless")
                time.sleep(7)
                # /html/body/div[1]/div/div[2]/div/div/div[3]/div/div/div/div[10]/div/div[1]/div/div/div
                # /html/body/div[1]/div/div[2]/div/div/div[4]/div/div/div/div[{cnt}]/div/div[1]/div/div/div/div[2]/div[1]/div
                # /html/body/div[1]/div/div[2]/div/div/div[4]/div/div/div/div[11]/div/div[1]/div/div/div/div[2]/div[1]/div
                # /html/body/div[1]/div/div[2]/div/div/div[3]/div/div/div/div[{cnt}]/div/div[1]
                # /html/body/div[1]/div/div[2]/div/div/div[3]/div/div/div/div[{cnt}]/div/div[1]/div/div/div/div[2]/div[1]/div
                # /html/body/div[1]/div/div[2]/div/div/div[4]/div/div/div/div[{cnt}]/div/div[1]/div/div/div/div[2]
                try:
                    choose_bot = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[1]/div/div[2]/div/div/div[3]/div/div/div/div[{cnt}]/div/div[1]/div/div/div/div[2]/div[1]/div")))
                    # name = choose_bot.text
                    name = driver.execute_script("return arguments[0].textContent;", choose_bot)
                    choose_bot.click()
                except:
                    choose_bot = wait.until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[1]/div/div[2]/div/div/div[4]/div/div/div/div[{cnt}]/div/div[1]/div/div/div/div[2]/div[1]/div")))
                    # name = choose_bot.text
                    name = driver.execute_script("return arguments[0].textContent;", choose_bot)
                    choose_bot.click()
                time.sleep(5)
                url=driver.current_url
                time.sleep(2)
                # with open(inputfile, "r", encoding="utf-8") as f:
                #     data = json.load(f)
                # for item in data:
                #     name2 = item.get("Name", "")
                #     if name2 ==name:
                #         print(cnt,name2,url)
                #         item["URL"] = url
                # with open("baidu.json", "w", encoding="utf-8") as f:
                #     json.dump(data, f, ensure_ascii=False)
                new_lines = []
                
                with open(inputfile, "r", encoding="utf-8") as f:
                    for line in f:
                        item = json.loads(line)
                        name2 = item.get("Name", "")
                        if name2 == name:
                            item["URL"] = url
                            print(cnt, name2, url)
                        new_lines.append(json.dumps(item, ensure_ascii=False))

              
                with open(inputfile, "w", encoding="utf-8") as f:
                    for line in new_lines:
                        f.write(line + '\n')

    finally:        
        driver.quit()

get_URL()

# if __name__ == "__main__":
# uploadpromptandknowledge()
    # select_API()



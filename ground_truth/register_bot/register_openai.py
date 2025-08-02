import os
from dotenv import load_dotenv

load_dotenv()

cookie = os.getenv('OPENAI_COOKIE')
if not cookie:
    raise ValueError("OPENAI_COOKIE environment variable not set")

import time
import json
from DrissionPage import ChromiumPage, ChromiumOptions
from openai import OpenAI
from docx import Document
import os

options = ChromiumOptions()

# Some arguments to make the browser better for automation and less detectable.
arguments = [
    "-no-first-run",
    "-force-color-profile=srgb",
    "-metrics-recording-only",
    "-password-store=basic",
    "-use-mock-keychain",
    "-export-tagged-pdf",
    "-no-default-browser-check",
    "-disable-background-mode",
    "-enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions",
    "-disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage",
    "-disable-gpu",
    "-accept-lang=en-US",
]

for argument in arguments:
    options.set_argument(argument)

driver = ChromiumPage(addr_or_opts=options)
# add cookies to login

driver.get("https://chatgpt.com")

script_dir = os.path.dirname(__file__)
# ---------------------------------------- finish initialzation --------------------------------------------------


def escapespace(content):
    single_line = "\n".join(content.splitlines())
    return single_line

def extract_index(filename):
    try:
        return int(filename.split("_")[0])
    except ValueError:
        return float('inf')

folder_path = os.path.join(script_dir, "../knowledge_file/containPII")
folder_path2 = os.path.join(script_dir, "../knowledge_file/noPII")

file_path_PII = sorted(
    [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))],
    key=lambda x: extract_index(os.path.basename(x))
)
file_path_no = sorted(
    [os.path.join(folder_path2, f) for f in os.listdir(folder_path2) if os.path.isfile(os.path.join(folder_path2, f))],
    key=lambda x: extract_index(os.path.basename(x))
)
APIfolder1  = os.path.join(script_dir, "../API_file/without_auth")
APIfolder2 = os.path.join(script_dir, "../API_file/with_auth")
API_path_1 = [os.path.join(APIfolder1, f) for f in os.listdir(APIfolder1) if os.path.isfile(os.path.join(APIfolder1, f))]
API_path_2 = [os.path.join(APIfolder2, f) for f in os.listdir(APIfolder2) if os.path.isfile(os.path.join(APIfolder2, f))]

APIfolder_valid = os.path.join(script_dir, "../API_file/valid")
API_path_valid = [os.path.join(APIfolder_valid, f) for f in os.listdir(APIfolder_valid) if os.path.isfile(os.path.join(APIfolder_valid, f))]

skip = [2,4,17,18,21,22,23,25,29,31,32,36,38,41,44,45,46,47,48,49,50]
def uploadAPI(cookies): 
    driver.set.cookies(cookies)
    for i in range(50):
        wdata = {}
        if i+1 in skip:
            continue
        driver.get('https://chatgpt.com/gpts/mine')
        driver.wait.eles_loaded("xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/button",timeout=10)
        more_button = driver.ele('xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/button')
        more_button.click()
        time.sleep(15)
        driver.wait.eles_loaded("xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/button",timeout=10)
        more_button = driver.ele('xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/button')
        more_button.click()
        time.sleep(15)
        driver.wait.eles_loaded(f"xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/div/div[{50-i}]/a/div[1]/div[2]/div[1]/span",timeout=10)
        Name_ele = driver.ele(f"xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/div/div[{50-i}]/a/div[1]/div[2]/div[1]/span")
        Name = Name_ele.text
        driver.wait.eles_loaded(f"xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/div/div[{50-i}]/a",timeout=10)
        link_ele = driver.ele(f"xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/div/div[{50-i}]/a")
        URL = link_ele.link
        editURL = "https://chatgpt.com/gpts/editor/g-" + URL.split("/g/")[1].split("-")[1]
        driver.get(editURL)
        time.sleep(3)
        wdata["Name"] = Name
        wdata["URL"] = URL
        driver.wait.eles_loaded("xpath=/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[3]/div[2]/textarea",timeout=10)
        prompt_ele = driver.ele("xpath=/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[3]/div[2]/textarea")
        Prompt = prompt_ele.text
        wdata["System Prompt"] = escapespace(Prompt)
        if i < 25:
            path = file_path_PII[i]
            print(path)
            wdata["Contain PII"] = True
        else:
            path = file_path_no[i-25]
            wdata["Contain PII"] = False
        doc = Document(path)
        text = "\n".join([para.text for para in doc.paragraphs])
        wdata["Knowledge"] = text
        # API
        driver.wait.eles_loaded("xpath=/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[7]/div[2]/button",timeout=10)
        action_button = driver.ele("xpath=/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[7]/div[2]/button")
        action_button.click()
        if i < 40:
            with open(API_path_1[i], 'r', encoding='utf-8') as file:
                data = json.load(file)
                json_string = json.dumps(data, indent=2, ensure_ascii=False)
                wdata["OpenAPI"]  = json.dumps(data, separators=(",", ":"))
                wdata["API Name"] = []
                wdata["API Name"].append(API_path_1[i].split("/")[-1].split(".")[0])
                print(wdata["API Name"])
        else:
            with open(API_path_2[i-40], 'r', encoding='utf-8') as file:
                data = json.load(file)
                json_string = json.dumps(data, indent=2, ensure_ascii=False)
                wdata["OpenAPI"]  = json.dumps(data, separators=(",", ":"))
                wdata["API Name"] = []
                wdata["API Name"].append(API_path_2[i-40].split("/")[-1].split(".")[0])
                print(wdata["API Name"])
        time.sleep(5)
        driver.wait.eles_loaded("xpath=/html/body/div[1]/div[2]/div[1]/div/div/div[4]/div[2]/div/input",timeout=10)
        privacy_place = driver.ele("xpath=/html/body/div[1]/div[2]/div[1]/div/div/div[4]/div[2]/div/input")
        privacy_place.input("https://example.com/policy")
        time.sleep(2)
        driver.wait.eles_loaded("xpath=/html/body/div[1]/div[2]/div[1]/div/div/div[3]/div[2]/div/textarea",timeout=10)
        api_place = driver.ele("xpath=/html/body/div[1]/div[2]/div[1]/div/div/div[3]/div[2]/div/textarea")
        api_place.input(json_string)
        time.sleep(5)
        driver.wait.eles_loaded("xpath=/html/body/div[1]/div[1]/div[2]/button[3]",timeout=10)
        update_button = driver.ele("xpath=/html/body/div[1]/div[1]/div[2]/button[3]")
        update_button.click()
        time.sleep(5)
        writefile = os.path.join(script_dir, "../openai.json")
        wdata["API Source"] = "OpenAPI" #Store
        with open(writefile,'a',encoding='utf-8') as wfile:
            json.dump(wdata, wfile, ensure_ascii=False)
            wfile.write("\n")


def uploadAPI_fix(cookies): 
    driver.set.cookies(cookies)
    inputfile = os.path.join(script_dir, "../../preparation/openai_pre/openai_attack_api_pre.json")
    with open(inputfile,'r',encoding='utf-8') as rfile:
        lines = rfile.readlines()
        for i in range(50):
            if i < 12:
                continue
            adata = json.loads(lines[i])
            wdata = adata
            if i+1 in skip:
                with open(inputfile,'a',encoding='utf-8') as wfile:
                    json.dump(wdata, wfile, ensure_ascii=False)
                    wfile.write("\n")
                continue
            driver.get('https://chatgpt.com/gpts/mine')
            driver.wait.eles_loaded("xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/button",timeout=10)
            more_button = driver.ele('xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/button')
            more_button.click()
            time.sleep(15)
            driver.wait.eles_loaded("xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/button",timeout=10)
            more_button = driver.ele('xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/button')
            more_button.click()
            time.sleep(15)
            driver.wait.eles_loaded(f"xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/div/div[{50-i}]/a/div[1]/div[2]/div[1]/span",timeout=10)
            Name_ele = driver.ele(f"xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/div/div[{50-i}]/a/div[1]/div[2]/div[1]/span")
            Name = Name_ele.text
            driver.wait.eles_loaded(f"xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/div/div[{50-i}]/a",timeout=10)
            link_ele = driver.ele(f"xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/div/div[{50-i}]/a")
            URL = link_ele.link
            editURL = "https://chatgpt.com/gpts/editor/g-" + URL.split("/g/")[1].split("-")[1]
            driver.get(editURL)
            time.sleep(3)
            
            # API
            # /html/body/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[8]/div[2]/button
            driver.wait.eles_loaded("xpath=/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[8]/div[2]/button",timeout=10)
            action_button = driver.ele("xpath=/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[8]/div[2]/button")
            action_button.click()
            with open(API_path_valid[i%12],'r',encoding='utf-8') as file:
                print(API_path_valid[i%12])
                data = json.load(file)
                json_string = json.dumps(data, indent=2, ensure_ascii=False)
                wdata["API Leaking"]["configuration file"]  = json.dumps(data, separators=(",", ":"))
                wdata["API Leaking"]["API Name"] = []
                wdata["API Leaking"]["API Name"].append(API_path_valid[i%12].split("/")[-1].split(".")[0])
            # print(wdata["API Name"])
            # if i < 40:
            #     with open(API_path_1[i], 'r', encoding='utf-8') as file:
            #         data = json.load(file)
            #         json_string = json.dumps(data, indent=2, ensure_ascii=False)
            #         wdata["OpenAPI"]  = json.dumps(data, separators=(",", ":"))
            #         wdata["API Name"] = []
            #         wdata["API Name"].append(API_path_1[i].split("/")[-1].split(".")[0])
            #         print(wdata["API Name"])
            # else:
            #     with open(API_path_2[i-40], 'r', encoding='utf-8') as file:
            #         data = json.load(file)
            #         json_string = json.dumps(data, indent=2, ensure_ascii=False)
            #         wdata["OpenAPI"]  = json.dumps(data, separators=(",", ":"))
            #         wdata["API Name"] = []
            #         wdata["API Name"].append(API_path_2[i-40].split("/")[-1].split(".")[0])
            #         print(wdata["API Name"])
            time.sleep(5)
            driver.wait.eles_loaded("xpath=/html/body/div[1]/div[2]/div[1]/div/div/div[4]/div[2]/div/input",timeout=10)
            privacy_place = driver.ele("xpath=/html/body/div[1]/div[2]/div[1]/div/div/div[4]/div[2]/div/input")
            privacy_place.input("https://example.com/policy")
            time.sleep(2)
            driver.wait.eles_loaded("xpath=/html/body/div[1]/div[2]/div[1]/div/div/div[3]/div[2]/div/textarea",timeout=10)
            api_place = driver.ele("xpath=/html/body/div[1]/div[2]/div[1]/div/div/div[3]/div[2]/div/textarea")
            api_place.input(json_string)
            time.sleep(5)
            driver.wait.eles_loaded("xpath=/html/body/div[1]/div[1]/div[2]/button[3]",timeout=10)
            update_button = driver.ele("xpath=/html/body/div[1]/div[1]/div[2]/button[3]")
            update_button.click()
            time.sleep(5)
            writefile = os.path.join(script_dir, "../../preparation/openai_pre/openai_attack_api_pre_new.json")
            parsed = json.loads(wdata["API Leaking"]["configuration file"])
            urls = [server["url"] for server in parsed.get("servers", [])]
            wdata["API Leaking"]["API meta info"] = urls
            with open(writefile,'a',encoding='utf-8') as wfile:
                json.dump(wdata, wfile, ensure_ascii=False)
                wfile.write("\n")

def deleteAPI(cookies): 
    driver.set.cookies(cookies)
    for i in range(50):
        if i < 33:
            continue
        driver.get('https://chatgpt.com/gpts/mine')
        driver.wait.eles_loaded("xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/button",timeout=10)
        more_button = driver.ele('xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/button')
        more_button.click()
        time.sleep(15)
        driver.wait.eles_loaded("xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/button",timeout=10)
        more_button = driver.ele('xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/button')
        more_button.click()
        time.sleep(15)
        # driver.wait.eles_loaded(f"xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/div/div[{50-i}]/a/div[1]/div[2]/div[1]/span",timeout=10)
        # Name_ele = driver.ele(f"xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/div/div[{50-i}]/a/div[1]/div[2]/div[1]/span")
        # Name = Name_ele.text
        driver.wait.eles_loaded(f"xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/div/div[{50-i}]/a",timeout=10)
        link_ele = driver.ele(f"xpath=/html/body/div/div/div[1]/div/main/div[2]/div/div/div[3]/div/div[{50-i}]/a")
        URL = link_ele.link
        editURL = "https://chatgpt.com/gpts/editor/g-" + URL.split("/g/")[1].split("-")[1]
        driver.get(editURL)
        time.sleep(3)
        driver.wait.eles_loaded("xpath=/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[7]/div[2]/div/div/button", timeout=10)
        actionbutton = driver.ele("xpath=/html/body/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[7]/div[2]/div/div/button")
        actionbutton.click()
        time.sleep(5)
        driver.wait.eles_loaded("xpath=/html/body/div[1]/div[2]/div[1]/div/div/div[1]/div[2]/button", timeout=10)
        deletebutton = driver.ele("xpath=/html/body/div[1]/div[2]/div[1]/div/div/div[1]/div[2]/button")
        deletebutton.click()
        time.sleep(5)
        driver.wait.eles_loaded("xpath=/html/body/div[1]/div[1]/div[2]/button[3]",timeout=10)
        update_button = driver.ele("xpath=/html/body/div[1]/div[1]/div[2]/button[3]")
        update_button.click()
        time.sleep(20)



cookies = []
# cookie = '''oai-did=94e54716-72de-43ba-917e-e0619aee9d40; oai-hlib=true; __Host-next-auth.csrf-token=891cdfdb7225569d8d2013dd02acb6033df982dd69b7c7e8e1150137999a3583%7C79ee5f5e46a88e7ed9a8e3497a59a7d08a4ce14722dd409b3790dd20c9b7cf99; oai-thread-sidebar=%7B%22isOpen%22%3Afalse%7D; oai-sh-c-i=67cdb2d9-7a90-800b-a2f6-1a2d9fb65b16; oai-allow-ne=false; oai-is-specific-model=true; oai-nav-state=1; oai-model-sticky-for-new-chats=false; __Secure-next-auth.callback-url=https%3A%2F%2Fchatgpt.com%2Fg%2Fg-683337eeacb0819186432ae35d393941-32-cyber-security-specialist%2Fc%2F68431085-3228-800b-ae31-8e935855c93d; _cfuvid=KB8HgRA3jh9HQIvVi9pj4kZuDcPw_eNLnB7hmlqPOdk-1750141369368-0.0.1.1-604800000; oai-gn=Pinji; oai-hm=SHOULD_WE_BEGIN%20%7C%20DIVE_IN; __cflb=0H28vzvP5FJafnkHxj4ZFaJJ3DzvkAVKVEKi6kDsDUX; cf_clearance=S6DEZIlT6TAAYGPX42MBLkHHvU1IZTNkDIYn8p5el7c-1750224524-1.2.1.1-xzMIpeQaHleNvenIoj7wcuKuMNc9tgGlyi2d8ujwRTIt2uelkj6ulP2wACAAmICEI6UR4cfuH7H4QKh1gO9WUH3lelfmF8V9.OHx.BtPyQayT30jYikmyfWhUAJOHzCu9I163fr6GGkiCcUTyDxXupCel6.rJRm6WON39ucm44mUOQqJv4oA4.H0GjP_XQ2vvMep.T04qKx0oMnKgcJkgIjGFrnEVkhIUoT5z2gJk3p.smjQ9Ig8DlZ6EEJOIVDOZjqwkr7L7pWWGSDq1rZ7JnVMN8OAI_ws9reYsCR8CyitOmolvC8J6q6qB1ckYWvHLAka5SU5lbZSgH4i1OdeJM2yaJFRxQvdtfagcFyb.Jo; _puid=user-PJRX5XLuxxY6pI1wRcPTReHl:1750224524-sdPEWsfite6rQk7DHa5m8erSu6CvPmlJpyXXIPjRqSo%3D; _uasid="Z0FBQUFBQm9VbE5wOFpUUW90dmtESVNfaFpHbmRpbmZqUXpnQ25RUTdjLUJqaC05WjFQamVnSTU3dThpTHA0dXluaXJJQUdJU3RtSk16bEpkUWRYQkVmRGxRWEo4X0RIZlh3U0V0RWt3aHYzRDVHaE5hVEwzeUc1LW16Umtpd3Nram5aNldEZ1dMU2NBOG5vQWZRZmw0OERVVXVpRldXaTVnUlBBdXZ6QW14blRkYXY5Y2ZGSVZpb2UxTXBaLTkzblhyQ3pQRnhRMUYyLTFITnMyZkFTS01YTU5hemliSzdfM1g1d1VKdzg2V1FBR3ZOV0J2UFYzNG0yRjE1RF9IWTB3b3IzWDU0amNJT0ZORXhTMWxWNVJTRW1uRG9iV184SjRIVEQ3S3R0b1UxNWhrUy0yREtpLXRvLU9ONTZRODloelZ6VnpjWWg4ZlNxWkowQXREaEJuQXFfZnVyWmFkUjBnPT0="; _umsid="Z0FBQUFBQm9VbE5wMW5idUtERkhtc042MTdKX0ZVamk1Mk1McmhsWUJxMHhwOXZJWDJ2S2JXQk9qVkZvLXd5eVJPWUxTSlp2MzJpRmd3SUo5d1Rtck9KM3BlZEpvWnE3MnNxYzZyelEzTHhiQjI4aHc3cEd0YjJoTlUxeVRfNUtKTWJYWm5qaHQyTmRydEhqMGU1MGt4ZGU4X25SMEJjZFpvdEhwakVDSzdxcGphc2NTN1VhY2Q1WWlnQnRsLXBlMXkzSUthQTVnUG1jRVRfa1RaZG84N1hJUndDQlJtek5ldlg4bzdRd0lIU0dtV2ZZcFZtZEg2RT0="; __cf_bm=yeP_IBrfHj_PtjN2XM2VdgDuIi.EovoczN22lfzffMc-1750226234-1.0.1.1-EuMccFZZEe6LpP_6UEbSKC4SLGbVe.lKUQX4qJMT1nXFWenAD3ARw_mSTM6KIh9cVUygNtcUPLrGYUGy.DFn3uHMLBc2FV6osMUPkaZ4aKM; oai-sc=0gAAAAABoUlU7Ll9SZxn5H66ZrTgbTal6wHbIsxTgOOSVKbNfbc1MOp-GRLesxcwtpjTozlfE4RkaTJUI6A-MEvLU-2UHc1aCkG_n9vE7OkbLKr_k5XWsKjAdIUOnkUwIcE1oocIyeNisceckMQLdl2J_qogWcOxY4l31TiLQW5l0LIdOdKfWCS5A1JaccNLODvUhJBF5_OnjudwqryLpDz0aAs1Z8Po7UxzkkyNEbptKdruavkXc0jE; __Secure-next-auth.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..UOXFfWgEdjysu7eV.yMUaGuKfZjyCRXF8n2etAxpzFBoDDSqlQWhR5D9M4XBY_EaR5nExTMrmKSPCz3W7w3lum_6byOT6vrrIX0EYuNXLdNbhLckCKnWnAVAAAVT1KC4UBmsTyNfaJGmc4QH7wFbpoZNtfcIgUW7zUlPnJYLzHqmxoQ-O1CvqaNnT-clzZZnJUJV3Qc0LXgS6He2Cx0MfEKCzvnbyltnOQrWfzekzgFFsUIs1g4Hmwdi8ZwRNBCitKAeApWgIPm2L8QgiJsAVC8uYjnRSqyh0b-RutDyIaMT73yJR8BqyVHLeGU4f9boj3qQckTrE8AtB0-4Vq_W7KL0_xxhNThoFbsEXDH5U51S6jX6TdCcNqLZN31k2VTRjQ-YeZD_BWJu5mUFRtBqB9xzG2Ggf1m-DtG7yG_Rw4ibLZ3e-WkJiMrgokTHKnt7snQV3AJ89NyrYPUkz9LuYi-atoqcEWVRxBFLt5FKLd-2fCstIHU6J2Von6XGKqulkDzkGKUn0AYFqi2_jj00bC_2numHfziJw6vLQAJRqVTqYYQNQstmV-ArCM89SancGQueRmG_Xijq9XeXm9A3MNQAqseCHh8s2IjDCniA7iiNxz_tnOov37DSGhNxmYHpAYb0BqWipjwJhM1Pe6-M-rMuT3S9MJJBYh2e8PZRoCrU0aIMYGuUCOZw2JaGWEnbsQe0cgjoJpVhCFHh97KS8ZBnuSJ05xN7NqliunHb1FZkySswlRF4caS2tOYJ2oD2za_7hfWcYII6TunvQKYmUl_MMPNfPYM9pVSWZpvbZgFxiyP3kZeS88MxLoih2ks3zSac2-DInCZk_qHx32FfvlD8eLst5p19EqR2iDA0aetBv0ZaYeJ1mNd6aay0G1VSPJYZVjlNQRT0ryRSeHkmEEcOCt_sCCBvCH-nkndTL4fUYXY2hBaZ7RY7951Ev2oPOxqhk-VERUYHN_06sxvuPubEdOUQvZqhdZL8C0GSSn2q6MJdHH9lS5uo73n4IPu8PzgnpSbWRhwDqHfKBj53M9DrPDGAK3bisZfIS4Lz5DhCrn7bDO76LJW0P_xaFQNEH58Q5YSMHwdFVuiQdUSWXCjU05NORtIZZpJ0qQmIfgTwCvNRLbuhgtoc63DEnbey6Nk95ExtFiWquTateAMsWkVUvawIuar6N0DGI2a3qPB9_p8xoXtbw_YfugXcnQdkynQZX2ByI-bByEwXOD5xNYzHBmT303nv9yllAFaKiPMvAOs0PPyBVu_KMskDf83bN65WUVoZDWr2izfp6CgWXoJkeyunCC_xPwbWyFBRvQmGvQ2fS2y_qRFBeFT5-KeweSnLm-4yX8erVb4srxS-rCvU42mYjYWDOudXCD8lu_hFK-K3u0sJz-YCUulq51PuqYdiSvkQu4cXeOHzj2Zo7fL3J2G8KI2hY5xRFrUSUpmPwUEaAOYH3KOZjrBZL3rSTgpYzcH456lS02f-6PQo9WqgoSQgIAL5JBcLJZYeVtu6kyfUgv0GyUpSkNEFS_TQi3lOwSyXsrNZ2ovCkgIAXnS-ImOueN2YQKS4Wsbk5e0NWj3p33UyvxJBSgYokDM3D7FfTt-9vLduEykAdBGhh2ajkrYoqHSF9XkD1x77uKNfhh_COj67IyeTM8_e-MOUfK7b4hhPjxmGyGd-ge_FtSZH4_iwnsu-D2Cb1DCsMon5p79qpxpyfttRCXTGcLn0BriRDm9nXuqgJBZXAeOqGbm6_S0Y80yW2lBZ6efvfGtrBs5SMEEOZdyOEQtyiUV9FiuTHP2SifOCY4D-0-9FUWjmeRj-i-SixsKEFPNm8zja7YfZtGwpBQXddkfLtmdzcsz9bxo0UQ7F_27XrFGSWBY2B4st_NYjedq2szZqwCx4e-JEQ6hrb0i3fgLqF5TzCMs-4b5-6Er_4NOqcdvEZeK1rGWw_LGvYImarHc6J4C-CPVkIMS-KoM2UpJeaWEsmBpfgujamSM8sWavkf4AUkYKChO-hgvCqlPYnhjPeW_M3ZAAM-WaVK3NrnBjqY0TVVAWRYsZsPXhWiE1NFcFtWXXMha7bwuwto9lSivIUEproVA_z-kJM3LRB6oisAGa0yOTEhSFGhdoKrGWoEc-Gzz2drPDFc42mmgiD1MPApwPrATqOH7cMsac0WBLfbYiag95yY12sRPKT6KLxxNQwe8PB4wvvaxX0raUBWwPEj8MSyiqEemnYUITeCFCU_I-nH2AQiynn1pWGKVrzmuxafgfgmJ-Fdkdzi2chn0najK_699pi5IltrNa-9CCS4x7lEDjDaetW-ZdaVrX9XhvhC7QVWl3xZuc6ArhVwA6z5NBMNS0IeuMLRnRYzJCn8qOPnWNZX-nR1e3l5C1F0mtRQHVZWqnAggq_xt2Edi9pWHWUo204BYN7-KcJc5ZRG-uW7-dWFThYxuVXKofg-9knn00B4aOdN28E9NljePrkPNcqvG6jhxDAfNo5C9CaU-xkimK3b4LKy3TK8456FM1AGbIsPKpojmqm_ugLgMUOZD47_Fuv_WjkjqpL9sTUrji3SH4ilerDJEggUR2n0uDFk7L13YYNSAmuudg6bL6rGrWzR9wkLpvIFz0KEaTZqVl21_2bwvDGgTTy4LZoqHgSvmNoh1vGQD_PaEEyvJJRPQ6mSq_QlkfqQlMioRD7W3-8cuKjNmwoaVlOABUJyMeJqZaL8J_FNIKZKRJ1bdqGyIJcfcAiLs10NYjkA82_p7VzaMA6R2911llb5zCkiU8mbcqX9KNCs7VNt2BXyCSYaQZuJOEONo35VrCjUJEcrLyE91FTOC7Oq_LLAGWai6NRTes7OaVTWyB2v80aLDP6-2K8GhXn6mbGCOGw9o8RFcZ808A9A__8ypsv0xs7ZrcCTCzaPgxwmkZO1NsFFYt6yoYLhxnwsGqR-e0UIsQWpLz0qpc35O9s4pBwlnPLzuzZOOUNIYX-MAXIhhSEgVPaMI7tDrQnAyZ8fQ9EEr4f9D4m5x454VmD6no-0xqZQQxiwkFZYHeyMk05rPUvRo_8ZKG-cH77sAU5HQQorsWRQIdmZQ4TsZPPShJZIgnQiVxq9pGM0VChLdcyaX0YtOjii0rtTTlh3324WBe5BVDMyj8gnpmhc66eBYEiYUu_SniYSpUHaGIIsXOp70plFkLGfIxt_CK2ToridGvNldqRryz9mhlZRAKzWMd4B3R6ZCDqqp3QyhL0bD8H2wew2ZRp9abzLwQnH9db6ljfo3rQ3mbkIHnt0ibOBxgadhjI1nBEm2etQfO95fSFunn4k8smQqUBHMkcOSjPUYePKGuaMEvcReVJoPDM2gWPRhtjmY21MKUAle5s0GGV4sJrXaW1N18PdHLfA_AvOH7zmdR8vjsbyIIGce5BVNsVzLtmK2TwKYN9VWV0usipN0EfGPZTCBWfypV3DJ5Jge5dyX-tM197c5FPb0guH7rG9rF14EcoVZrdely8_w_8OhjiILfk0X1Je1yOJJR0BwLoxV4Se0TcpCAaDsjf78FImOiOA3YGEygEcgwVmb33ri4DuPMJDAO3BvxJxfhk90SKIkOF.Cz556wGz2_BGzz9-6lMv6Q; _dd_s=rum=0&expire=1750227478949&logs=1&id=d6eeed2f-2379-4cd8-aaba-a9870b57e3de&created=1750224152777'''
for item in cookie.split('; '):
    name, value = item.split('=', 1)
    cookies.append({"name": name, "value": value})
try:
    uploadAPI_fix(cookies)
    # deleteAPI(cookies)
# register(inputfile, cookies)
finally:
    driver.quit()
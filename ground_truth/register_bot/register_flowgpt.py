import os
from dotenv import load_dotenv

load_dotenv()

cookie = os.getenv('FLOWGPT_COOKIE')
if not cookie:
    raise ValueError("FLOWGPT_COOKIE environment variable not set")

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

driver.get("https://flowgpt.com/")
# add cookies to login

# ------------------------------------------finish initiflowgptzation----------------------------------------

def escapespace(content):
    single_line = "\n".join(content.splitlines())
    return single_line

def remove_non_bmp(text):
    return ''.join(c for c in text if ord(c) <= 0xFFFF)

def register(inputfile, cookies):
    driver.set.cookies(cookies)

    driver.get("https://flowgpt.com/")
    time.sleep(20)

    cnt = 0
    with open(inputfile, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            Prompt = remove_non_bmp(data["Prompt Leaking"]["public system prompt"])
            if len(Prompt) < 100:
                continue
            if len(Prompt) > 2500:
                continue
            cnt += 1
            if cnt <= 42:
                continue
            if cnt > 50:
                break

            Name = data["Name"]
            Name = str(cnt) + "_" + Name
            if len(Name) > 20:
                Name = Name[:20]

            driver.get("https://studio.flowgpt.com/bot/draft?promptType=general")
            time.sleep(3)

            driver.ele('#name').input(Name)
            time.sleep(1)
            driver.ele('#description').input("This is a test bot......")
            time.sleep(1)

            prompt_box = driver.ele(
                r"css:#scrollableDiv > div > div.flex-1.pl-2\.5 > div > div.split-view-container.allotment-module_splitViewContainer__rQnVa > div:nth-child(1) > div > div > div.flex.flex-col.gap-5.px-2\.5.\32 xl\:px-\[1\.875rem\] > div:nth-child(4) > div > div.mt-2.p-3.pt-0 > div > div > div > div.cm-scroller > div.cm-content.cm-lineWrapping"
            )
            prompt_box.input(Prompt)
            time.sleep(1)

            driver.ele('#welcomeMessage').input("This is a test bot......")
            time.sleep(10)

            # more_tag = driver.ele(r"css:#scrollableDiv > div > div.flex-1.pl-2\.5 > div > div.split-view-container.allotment-module_splitViewContainer__rQnVa > div:nth-child(1) > div > div > div.flex.flex-col.gap-5.px-2\.5.\32 xl\:px-\[1\.875rem\] > fieldset:nth-child(6) > div.mt-2.p-3.pt-0 > div.my-react-select-container.z-10.text-1\.5xs.css-b62m3t-container > div > div.my-react-select__indicators.css-1wy0on6 > div > svg"
            # )
            # more_tag.click()
            # time.sleep(1)
            #
            # driver.wait.eles_loaded(r"css:#div.my-react-select__menu css-1nmdiq5-menu", timeout=10)
            # tag = driver.ele(r"css:#div.my-react-select__menu css-1nmdiq5-menu")
            # tag.click()
            # time.sleep(1)

            public = driver.ele(r"css:#scrollableDiv > div > div.flex-1.pl-2\.5 > div > div.split-view-container.allotment-module_splitViewContainer__rQnVa > div:nth-child(1) > div > div > div.flex.flex-col.gap-5.px-2\.5.\32 xl\:px-\[1\.875rem\] > fieldset:nth-child(8) > div.mt-2.p-3.pt-0 > div > label:nth-child(1) > span.chakra-checkbox__control.css-1gor8n"
            )
            public.click()
            time.sleep(1)

            announce = driver.ele(r"css:#scrollableDiv > div > div.dark-scroll-bar.flex.h-\[calc\(100vh-96px\)\].w-\[200px\].shrink-0.flex-col.justify-between.overflow-y-auto.overflow-x-hidden.bg-fgMain-950.scrollbar-hide.css-i70813 > div.mb-\[18px\] > div.mx-4.space-y-2\.5 > button.chakra-button.w-full.cursor-pointer.text-\[1\.0625rem\].font-semibold.css-8ei9ul"
            )
            announce.click()
            time.sleep(5)

            # jump = driver.ele(r"css:#scrollableDiv > div > div.relative.h-\[535px\].w-full > div.absolute.w-full.top-\[50px\].\32 xl\:top-\[76px\] > div > div.space-y-10 > div > div.flex.items-center.gap-1\.5.md\:flex-nowrap > button.flex.h-10.min-w-\[118px\].max-w-\[118px\].flex-1.items-center.justify-center.gap-0\.5.rounded-\[10px\].bg-fgMain-0.py-2.text-2sm.font-bold.text-fgMain-1000.transition-all.duration-300.ease-in-out.hover\:bg-fgMain-0\/15.hover\:text-fgMain-0.md\:h-\[50px\].lg\:min-w-\[270px\] > span"
            # )
            # jump.click()
            time.sleep(5)


            writefile = "ground_truth/flowgpt.json"
            wdata = {
                "Name": Name,
                "URL": driver.url,
                "System Prompt": escapespace(Prompt),
                "API Source": "Do not support API",
                "API Name": [],
                "OpenAPI": "",
                "Knowledge": "",
                "Contain PII": ""
            }
            with open(writefile, 'a', encoding='utf-8') as wfile:
                json.dump(wdata, wfile, ensure_ascii=False)
                wfile.write("\n")


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

inputfile = r"Configuration-Leaking-on-LLM-APP-Store/preparation/flowgpt_pre/flowgpt_attack_instruction_pre.json"

cookies = []
for item in cookie.split('; '):
    name, value = item.split('=', 1)
    cookies.append({"name": name, "value": value})
try:
    # uploadknowledge(inputfile, cookies)
    register(inputfile, cookies)
finally:
    driver.quit()







# Configuration-Leaking-on-LLM-APP-Store
In this repository, we propose LLMThief, an end-to-end framework designed for red teamers to systematically understand and identify configuration leaking vulnerabilities in LLM app stores. Compared to prior work that treated LLM apps merely as conversational interfaces, our key insight is to view the LLM app store as a unified, integrated system. This system-level security perspective enables us to identify a richer attack surface, leveraging extra knowledge to develop more effective attacks. 

In this repository, we publicly release all the source code of LLMThief to support future research. We also hope that LLMThief can be widely adopted in red-team testing to help enhance the security of LLM app stores.

## Major Advantage of LLMThief

(1) **Real-world Effectiveness**: LLMThief could successfully steal the app configurations from six commercial LLM app stores, outperforming all baselines; 

(2) **Broader Attack Scope**: LLMThief could examine not only system prompts but also APIs and knowledge files leakage in LLM apps, revealing novel threats on these overlooked configurations; 

(3) **End-to-End Automation at Scale**: LLMThief is capable of fully automated measurement across online LLM app stores, enabling scalable evaluation. 


## Folder Structure

- **`preparation/`**: During the attack preparation phase,
the attackers register accounts on target LLM app stores and
observe exploitable features, such as public
starting phrases, exposed API hostnames, support for plugin
stores, etc. These observations are organized in a JSON file, as shown in this folder. Moreover, it contains collected dataset (same in ground_truth/preparation) for LLMThief evaluation.

- **`seeds_constructor/`**: At the start of the
measurement, the attack prompt seeds construction module
extracts the exploitable features of each store from the JSON
file and combines them with different types of configuration
leaking attacks to formulate attack seeds, as shown in this folder. 

- **`mutator/`**: Contains mutation scripts (Character Stuffing, Synonym Replacing, Scenario Simulating, Language Switching, Suffix Guiding) to manipulate initial seeds for generating diverse attack prompts. 

- **`interactor/`**: interactor deals with
the interface of different on-the-shelf LLM app stores (We implement six LLM app stores and it is easy to extend) to input adversarial mutated prompts and get generated answers.

- **`decision_maker/`**: Contains configuration files for our fine-tuned model used in Ollama, including model download links and configuration ModelFile.

- **`ground_truth/`**: Contain the ground truth datasets, preparation instructive JSON files, and the scripts to register these configurations on the LLM app stores.
  
## Install
```
conda env create -f environment.yml
or
pip install -r requirements.txt
```

## Usage
To instantiate LLMThief, use the `main.py` script. This script allows you to specify the target platform and attack type.

### Command Line Example

```bash
python main.py -p ali -t instruction -l 1 -n 0
```
- **`-p`**: Specifies the platform to attack (e.g., `ali`, `baidu`, `openai`, `poe`, `flowgpt`, `coze`).
- **`-t`**: Specifies the attack targets (e.g., `instruction`, `api`, `knowledge`).
- **`-l`**: Specifies the evaluation level, 1: only seed, 2. seed + mutator, 3: seed + feature, 4: seed + mutator + feature. 
- **`-n`**: an optional integer parameter, default is 0, used to skip some bots since they have already tested.
- You may also need to configure a .env file, including some parameters like Judger_URL, Judger_Key, {test store}_COOKIE, etc. Besides, prepare necesarry things in the preparation file, e.g., test target URL, Name...


### Attention
Many LLM App Stores only provide services to logged-in or paying users. We automate the login process using cookies. During reproduction, please use your own account and replace the cookies with your own in the .env .

## Real-World Impact of LLMThief

We have reported security problems found by LLMThief to affected LLM app stores. Up to now: 

- **Baidu** confirmed the vulnerability on the Wenxin app store and provided a **cash reward**. They were interested in the attacks and had an in-depth discussion with us about the specifics. They will arrange a fix for this problem. 
    
- **ByteDance** acknowledged our report of Coze and confirmed the vulnerability. We were also invited to participate in a prompt leaking competition held by ByteDance and won **a reward of $\approx$\$1500**. They informed us that recent efforts to address this issue include providing developers with a prompt leakage prevention feature, which adds defensive prompts to mitigate basic attacks. However, such measures are likely to be less effective against advanced automated attacks like ours. A more comprehensive and robust protection mechanism may be offered by Coze exclusively to enterprise customers.

- **Alibaba** acknowledged our report of Tongyi and awarded the vulnerability with a **bug bounty**s. We are still in discussion on how to address this issue.

- **OpenAI** confirmed the vulnerability on the GPT Store. They informed us that they had placed a blocker on our submission to gather additional information from their customers. Their recent mitigation effort includes explicitly warning developers in the interface that uploaded system prompts and knowledge files may be partially or fully exposed.

- **Quora** appreciated our report and considered that the work required to improve Poe on this issue would be significant and may limit normal interactions with the app if they make the input filtering more aggressive. They are making internal efforts to address these issues.

- **FlowGPT** confirmed the vulnerability and they have removed the leaked public starting phrase of the system prompt.  


## Folder tree

```
.
├── decision_maker
│   ├── model-download-link.txt
│   └── Modelfile
├── environment.yml
├── ground_truth
│   ├── API_file
│   │   ├── valid
│   │   │   ├── AIVoiceGenerator.json
│   │   │   ├── ChatwithCode.json
│   │   │   ├── CreateVoice.json
│   │   │   ├── CrewAIAssistant.json
│   │   │   ├── flowchart.json
│   │   │   ├── invideo.json
│   │   │   ├── Paraphrase.json
│   │   │   ├── Resume.json
│   │   │   ├── SlideMaker.json
│   │   │   ├── Spreadsheet.json
│   │   │   ├── webPilot.json
│   │   │   └── WebsiteINSTANTLY.json
│   │   ├── with_auth
│   │   │   ├── AcademicResearcher.json
│   │   │   ├── Adzedek.json
│   │   │   ├── Diagram_render.json
│   │   │   ├── getPodcastTranscript.json
│   │   │   ├── RankoFootbal.json
│   │   │   ├── SEO.json
│   │   │   ├── SpotifyWeb.json
│   │   │   ├── Synthesys.json
│   │   │   ├── ToDoTask.json
│   │   │   └── waitlist.json
│   │   └── without_auth
│   │       ├── AdIntelli.json
│   │       ├── AIVoiceGenerator.json
│   │       ├── AlgorumMystic.json
│   │       ├── Astrologer.json
│   │       ├── BeatandRaise.json
│   │       ├── ChatwithCode.json
│   │       ├── ConnectSpotify.json
│   │       ├── ConsultingExpert.json
│   │       ├── CreateVoice.json
│   │       ├── CrewAIAssistant.json
│   │       ├── Diagram_generator.json
│   │       ├── Diagram.json
│   │       ├── DiagramCreator.json
│   │       ├── flowchart.json
│   │       ├── GPT4Consultant.json
│   │       ├── GPTFinder.json
│   │       ├── invideo.json
│   │       ├── Keenious.json
│   │       ├── LandingPage.json
│   │       ├── MathPro.json
│   │       ├── Paraphrase.json
│   │       ├── QuizMaker.json
│   │       ├── Resume.json
│   │       ├── ScholarGPT.json
│   │       ├── SlideMaker.json
│   │       ├── SmartSlides.json
│   │       ├── Spreadsheet.json
│   │       ├── StockAnalysis.json
│   │       ├── Stream.json
│   │       ├── TestingCatalog.json
│   │       ├── TranscriptInformation.json
│   │       ├── TTS.json
│   │       ├── VideoMaker.json
│   │       ├── webPilot.json
│   │       ├── WebScraper.json
│   │       ├── WebSearch.json
│   │       ├── WebsiteINSTANTLY.json
│   │       ├── Wolfram.json
│   │       ├── WriterOne.json
│   │       └── youtubetranscript.json
│   ├── knowledge_file
│   │   └── load.py
│   ├── preparation
│   │   ├── ali_pre
│   │   │   ├── ali_attack_instruction_pre.json
│   │   │   └── ali_attack_knowledge_pre.json
│   │   ├── baidu_pre
│   │   │   ├── API_configuration_files
│   │   │   │   ├── acdemicsearch
│   │   │   │   │   ├── ai-plugin.json
│   │   │   │   │   └── openapi.yaml
│   │   │   │   ├── AIspeech
│   │   │   │   │   ├── ai-plugin.json
│   │   │   │   │   ├── example.yaml
│   │   │   │   │   ├── msg_content.yaml
│   │   │   │   │   └── openapi.yaml
│   │   │   │   ├── astronomy
│   │   │   │   │   ├── ai-plugin.json
│   │   │   │   │   └── openapi.yaml
│   │   │   │   ├── draw
│   │   │   │   │   ├── ai-plugin.json
│   │   │   │   │   └── openapi.yaml
│   │   │   │   ├── PPTmaker
│   │   │   │   │   ├── ai-plugin.json
│   │   │   │   │   └── openapi.yaml
│   │   │   │   ├── presentation
│   │   │   │   │   ├── ai-plugin.json
│   │   │   │   │   └── openapi.yaml
│   │   │   │   ├── quizgeneration
│   │   │   │   │   ├── ai-plugin.json
│   │   │   │   │   └── openapi.yaml
│   │   │   │   ├── search
│   │   │   │   │   ├── ai-plugin.json
│   │   │   │   │   └── openapi.yaml
│   │   │   │   ├── videogen
│   │   │   │   │   ├── ai-plugin.json
│   │   │   │   │   └── openapi.yaml
│   │   │   │   ├── videomaker
│   │   │   │   │   ├── ai-plugin.json
│   │   │   │   │   └── openapi.yaml
│   │   │   │   └── WolframMath
│   │   │   │       ├── ai-plugin.json
│   │   │   │       └── openapi.yaml
│   │   │   ├── baidu_attack_api_pre.json
│   │   │   ├── baidu_attack_instruction_pre.json
│   │   │   └── baidu_attack_knowledge_pre.json
│   │   ├── coze_pre
│   │   │   ├── coze_attack_api_pre.json
│   │   │   ├── coze_attack_instruction_pre.json
│   │   │   └── coze_attack_knowledge_pre.json
│   │   ├── flowgpt_pre
│   │   │   └── flowgpt_attack_instruction_pre.json
│   │   ├── openai_pre
│   │   │   ├── openai_attack_api_pre.json
│   │   │   ├── openai_attack_instruction_pre.json
│   │   │   └── openai_attack_knowledge_pre.json
│   │   └── poe_pre
│   │       ├── poe_attack_instruction_pre.json
│   │       └── poe_attack_knowledge_pre.json
│   └── register_bot
│       ├── register_ali.py
│       ├── register_baidu.py
│       ├── register_coze.py
│       ├── register_flowgpt.py
│       ├── register_openai.py
│       └── register_poe.py
├── interactor
│   ├── ali
│   │   ├── attack_ali_instruction.py
│   │   └── attack_ali_knowledge.py
│   ├── baidu
│   │   ├── attack_baidu_api.py
│   │   ├── attack_baidu_instruction.py
│   │   └── attack_baidu_knowledge.py
│   ├── coze
│   │   ├── attack_coze_api.py
│   │   ├── attack_coze_instruction.py
│   │   └── attack_coze_knowledge.py
│   ├── flowgpt
│   │   ├── attack_flowgpt_instruction.py
│   │   ├── attack_flowgpt_knowledge.py
│   │   └── CloudflareBypasser.py
│   ├── hug
│   │   └── attack_hug_instruction.py
│   ├── openai
│   │   ├── attack_openai_api.py
│   │   ├── attack_openai_instruction.py
│   │   ├── attack_openai_knowledge.py
│   │   └── CloudflareBypasser.py
│   └── poe
│       ├── attack_poe_instruction.py
│       └── attack_poe_knowledge.py
├── LICENSE
├── main.py
├── mutator
│   ├── __init__.py
│   ├── external_mutator.py
│   └── internal_mutator.py
├── output
│   ├── ali
│   ├── baidu
│   ├── coze
│   ├── flowgpt
│   ├── hug
│   ├── openai
│   └── poe
├── preparation
│   ├── ali_pre
│   │   ├── ali_attack_instruction_pre.json
│   │   └── ali_attack_knowledge_pre.json
│   ├── baidu_pre
│   │   ├── baidu_attack_api_pre.json
│   │   ├── baidu_attack_instruction_pre.json
│   │   └── baidu_attack_knowledge_pre.json
│   ├── coze_pre
│   │   ├── coze_attack_api_pre.json
│   │   ├── coze_attack_instruction_pre.json
│   │   └── coze_attack_knowledge_pre.json
│   ├── flowgpt_pre
│   │   └── flowgpt_attack_instruction_pre.json
│   ├── openai_pre
│   │   ├── openai_attack_api_pre.json
│   │   ├── openai_attack_instruction_pre.json
│   │   └── openai_attack_knowledge_pre.json
│   └── poe_pre
│       ├── poe_attack_instruction_pre.json
│       └── poe_attack_knowledge_pre.json
├── README.md
├── requirements.txt
└── seeds_constructor
    └── seed.py

53 directories, 150 files

```

## Modelfile: `my-qwen.gguf`
The `my-qwen.gguf` file is our fine-tuned model for decision making. You can deploy it with Ollama via provided Modelfile, enabling you to load and run the decision maker. Due to GitHub's file size limitations, we provide a download link: https://drive.google.com/file/d/1aTaqoPlOAnGqBq603lMrmZUpOccuFBjk/view?usp=sharing
















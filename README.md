# Configuration-Leaking-on-LLM-APP-Store

Configuration leaking attack is an emerging security threat
in large language model applications (LLM apps), where
adversaries can manipulate the LLM app to reveal its sensitive configurations, such as system prompts, external APIs,
and knowledge files. Despite their critical implications, these
attacks remain understudied within LLM app stores, leaving open questions about their defenses, prevalence, and realworld impacts. In this repository, we propose LLMThief, a two-layer framework designed to systematically understand and
identify configuration leaking vulnerabilities in LLM app
stores. We evaluated LLMThief across 7 widely used LLM
app stores, including OpenAI GPT Store, ByteDance Coze,
and Baidu Wenxin. Our analysis reveals that existing defenses across all evaluated stores can be circumvented, while
user-friendly features intended to enhance functionality inadvertently facilitate effective configuration leaks. Overall,
we discovered about 5,000 vulnerable LLM apps across all
the evaluated LLM app stores, highlighting risks including
system prompt leaks, external API exposures, and knowledge
file leaks. Those issues can not only compromise developers’
intellectual property but also leak personal privacy and even
disclose corporate secrets. We have responsibly disclosed
our findings to the affected vendors and received acknowledgments and bug bounties from ByteDance, Baidu, Alibaba,
Quora, etc.

In this repository, we publicly release all the source code of LLMThief and the fine-tuned models to support future research.

## Folder Structure
```
.
├── README.md
├── decision_maker
│   ├── Modelfile
│   └── model-download-link.txt
├── directory.md
├── environment.yml
├── interactor
│   ├── ali
│   │   ├── attack_ali_instruction.py
│   │   └── attack_ali_knowledge.py
│   ├── baidu
│   │   ├── attack_baidu_api.py
│   │   ├── attack_baidu_instruction.py
│   │   └── attack_baidu_knowledge.py
│   ├── coze
│   │   ├── attack_coze_api.py
│   │   ├── attack_coze_instruction.py
│   │   └── attack_coze_knowledge.py
│   ├── flowgpt
│   │   ├── CloudflareBypasser.py
│   │   ├── attack_flowgpt_instruction.py
│   │   └── attack_flowgpt_knowledge.py
│   ├── hug
│   │   └── attack_hugface_instruction.py
│   ├── openai
│   │   ├── CloudflareBypasser.py
│   │   ├── attack_openai_api.py
│   │   ├── attack_openai_instruction.py
│   │   └── attack_openai_knowledge.py
│   └── poe
│       ├── attack_poe_instruction.py
│       └── attack_poe_knowledge.py
├── main.py
├── mutator
│   ├── __init__.py
│   ├── external_mutator.py
│   └── internal_mutator.py
├── preparation
│   ├── ali_pre
│   │   ├── ali_attack_instruction_pre.json
│   │   └── ali_attack_knowledge_pre.json
│   ├── baidu_pre
│   │   ├── baidu_attack_api_pre.json
│   │   ├── baidu_attack_instruction_pre.json
│   │   └── baidu_attack_knowledge_pre.json
│   ├── coze_pre
│   │   ├── coze_attack_api_pre.json
│   │   ├── coze_attack_instruction_pre.json
│   │   └── coze_attack_knowledge_pre.json
│   ├── flowgpt_pre
│   │   ├── flowgpt_attack_instruction_pre.json
│   │   └── flowgpt_attack_knowledge_pre.json
│   ├── hug_pre
│   │   └── hug_attack_instruction_pre.json
│   ├── openai_pre
│   │   ├── openai_attack_api_pre.json
│   │   ├── openai_attack_instruction_pre.json
│   │   └── openai_attack_knowledge_pre.json
│   └── poe_pre
│       ├── poe_attack_instruction_pre.json
│       └── poe_attack_knowledge_pre.json
└── seeds_constructor
    └── seed.py

```
- **`preparation/`**: During the attack preparation phase,
the attackers register accounts on target LLM app stores and
observe exploitable features as detailed in §6, such as public
starting phrases, exposed API hostnames, support for plugin
stores, etc. These observations are organized in a JSON file, as shown in this folder. Moreover, it contains collected dataset (ground truth) for LLMThief evaluation.

- **`seeds_constructor/`**: At the start of the
measurement, the attack prompt seeds construction module
extracts the exploitable features of each store from the JSON
file and combines them with different types of configuration
leaking attacks to formulate attack seeds, as shown in this folder. 

- **`mutator/`**: Contains mutation scripts (Character Stuffing, Synonym Replacing, Scenario Simulating, Language Switching, Suffix Guiding) to manipulate initial seeds for generating diverse attack prompts. 

- **`interactor/`**: interactor deals with
the interface of different on-the-shelf LLM app stores (We implement seven LLM app store and it is easy to extend) to input adversarial mutated prompts and get generated answers.

- **`decision-maker/`**: Contains configuration files for our fine-tuned model used in Ollama, including model download links and configuration ModelFile.
  
## Install
conda env create -f environment.yml


## Usage
To instantiate LLMThief, use the `main.py` script. This script allows you to specify the target platform and attack type.

### Command Line Example

```bash
python main.py --platform ali --type instruction
```
- **`--platform`**: Specifies the platform to attack (e.g., `ali`, `baidu`, `openai`, `poe`, `flowgpt`, `hug`, `coze`).
- **`--type`**: Specifies the attack targets (e.g., `instruction`, `api`, `knowledge`).

### Attention
Many LLM App Stores only provide services to logged-in or paying users. We automate the login process using cookies. During reproduction, please use your own account and replace the cookies with your own in the given scripts.

## Modelfile: `my-qwen.gguf`
The `my-qwen.gguf` file is our fine-tuned model for decision making. You can deploy it with Ollama via provided Modelfile, enabling you to load and run the decision maker. Due to GitHub's file size limitations, we provide a download link: https://drive.google.com/file/d/1aTaqoPlOAnGqBq603lMrmZUpOccuFBjk/view?usp=sharing
















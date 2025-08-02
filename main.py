# main.py
import json
import argparse
import os

from seeds_constructor.seed import *
import importlib.util
import sys
import random
def main(platform, type, level, skip):
    i = 0
    if type == "instruction":
        file_path = f"ground_truth/preparation/{platform}_pre/{platform}_attack_{type}_pre.json"
        # Read instructive JSON file. This file_path must match the test target, here we test on ground truth dataset.
        with open(file_path, 'r', encoding='utf-8') as file:
            attack_prompts = []
            module_path = f"interactor/{platform}/attack_{platform}_instruction.py"
            spec = importlib.util.spec_from_file_location(f"attack_{platform}_instruction", module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[f"interactor.{platform}.attack_{platform}_instruction"] = module
            spec.loader.exec_module(module)
            LLMThief = getattr(module, "LLMThief")
            for line in file:
                i += 1
                if i <= skip:
                    continue
                data = json.loads(line)
                #initial seeds generation with instructive data
                seeds = initial_seeds(data, platform, type, level)
                url = data['URL']
                ground_truth = data['Prompt Leaking']['public system prompt']
                if int(level) == 4: # finished
                    #apply muatation to bypass potential defenses and exploit features
                    attack_prompts = seeds[:]
                    attack_prompts = attack_generator(attack_prompts)
                    random.shuffle(attack_prompts) #random
                    leaked_instruction, score, scorelist, bestssresponse, bestsscore, sslist, fail = LLMThief(attack_prompts,url,int(level),ground_truth)
                elif int(level) == 3: # seed +  feature
                    attack_prompts = seeds[:]
                    random.shuffle(attack_prompts) #random
                    leaked_instruction, score, scorelist, bestssresponse, bestsscore, sslist, fail = LLMThief(attack_prompts,url,int(level),ground_truth)
                elif int(level) == 2: # seed + mutator
                    attack_prompts = seeds[:]
                    attack_prompts = attack_generator(attack_prompts)
                    random.shuffle(attack_prompts) #random
                    leaked_instruction, score, scorelist, bestssresponse, bestsscore, sslist, fail = LLMThief(attack_prompts,url,int(level),ground_truth)
                elif int(level) == 1: # seed 
                    attack_prompts = seeds[:]
                    leaked_instruction, score, scorelist, bestssresponse, bestsscore, sslist = LLMThief(attack_prompts,url,int(level),ground_truth)
                with open(f"output/{platform}/{platform}_instruction_output_level{level}.json", 'a', encoding='utf-8') as wfile:
                    data['Prompt Leaking']['leaked prompt'] = leaked_instruction
                    data['Prompt Leaking']['LCS'] = score
                    data['Prompt Leaking']['scorelist'] = scorelist
                    data['Prompt Leaking']['best ss response'] = bestssresponse
                    data['Prompt Leaking']['best ss score'] = bestsscore
                    data['Prompt Leaking']['SS'] = sslist
                    if int(level) != 1:
                        data['Prompt Leaking']['fail times'] = fail # this should be deleted when test level == 1
                    json.dump(data, wfile, ensure_ascii=False)
                    wfile.write('\n')

    if type == "api":
        file_path = f"ground_truth/preparation/{platform}_pre/{platform}_attack_api_pre.json"
        # Read api JSON instructive file
        with open(file_path, 'r', encoding='utf-8') as file:
            attack_prompts = []
            module_path = f"interactor/{platform}/attack_{platform}_api.py"
            spec = importlib.util.spec_from_file_location(f"attack_{platform}_api", module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[f"interactor.{platform}.attack_{platform}_api"] = module
            spec.loader.exec_module(module)
            LLMThief = getattr(module, "LLMThief")
            for line in file:
                i += 1
                if i <= skip:
                    continue
                data = json.loads(line)
                seeds = initial_seeds(data, platform, type, level)
                attack_prompts = seeds[:]
                # attack_prompts = slight_mutation(attack_prompts) # api can also apply mutation
                url = data["URL"]
                if platform == 'openai': # without plugin store feature, with privacy setting
                    ground_truth = data["API Leaking"]["configuration file"]
                else: # with plugin store feature
                    ground_truth = data["API Leaking"]["API Name"]
                leaked_api, vul = LLMThief(attack_prompts, url, int(level),ground_truth)
                with open(f"output/{platform}/{platform}_api_output_level{level}.json", 'a', encoding='utf-8') as wfile:
                    if vul == "name": # NameLeak
                        data['API Leaking']['leaked API name'] = leaked_api
                    else: # ParaLeak
                        data['API Leaking']['leaked API configuration file'] = leaked_api
                    json.dump(data, wfile, ensure_ascii=False)
                    wfile.write('\n')


    if type == "knowledge":
        file_path = f"ground_truth/preparation/{platform}_pre/{platform}_attack_knowledge_pre.json"
        # read knowledge JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            attack_prompts = []
            module_path = f"interactor/{platform}/attack_{platform}_knowledge.py"
            spec = importlib.util.spec_from_file_location(f"attack_{platform}_knowledge", module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[f"interactor.{platform}.attack_{platform}_knowledge"] = module
            spec.loader.exec_module(module)
            LLMThief = getattr(module, "LLMThief")
            for line in file:
                i += 1
                if i <= skip:
                    continue
                data = json.loads(line)
                # initial seeds generation with knowledge data
                seeds = initial_seeds(data, platform, type, level)
                attack_prompts = seeds[:]
                url = data["URL"]
                ground_truth = data["Knowledge Leaking"]["knowledge content"]
                # Though we implement level 2 and 3, we recommend use level 4 for testing. Abalation study here is meaningless since attack cannot be launched without features
                if int(level) == 3: #include features
                    leaked_knowledge, vul = LLMThief(attack_prompts, url, int(level), ground_truth)
                    with open(f"output/{platform}/{platform}_knowledge_output_level{level}.json", 'a', encoding='utf-8') as wfile:
                        data['Knowledge Leaking']['leaked knowledge']['leaked response'] = leaked_knowledge
                        json.dump(data, wfile, ensure_ascii=False)
                        wfile.write('\n')
                elif int(level) == 2: #privacy only
                    attack_prompts = attack_generator(attack_prompts)
                    random.shuffle(attack_prompts) #random
                    leaked_knowledge, vul = LLMThief(attack_prompts, url, int(level), ground_truth)
                    with open(f"output/{platform}/{platform}_knowledge_output_level{level}.json", 'a', encoding='utf-8') as wfile:
                        data['Knowledge Leaking']['leaked knowledge']['leaked response'] = leaked_knowledge
                        json.dump(data, wfile, ensure_ascii=False)
                        wfile.write('\n')
                else: # level 4 (recommended)
                    attack_prompts = slight_mutation(attack_prompts)
                    random.shuffle(attack_prompts) #random
                    leaked_knowledge, vul, cite_source = LLMThief(attack_prompts, url, int(level), ground_truth)
                    with open(f"output/{platform}/{platform}_knowledge_output_level{level}.json", 'a',
                              encoding='utf-8') as wfile:
                        data['Knowledge Leaking']['leaked knowledge']['leaked response'] = leaked_knowledge
                        data['Knowledge Leaking']['leaked knowledge']['card' if platform == 'coze' else 'cite_source'] = cite_source # coze have a code to see cite source
                        json.dump(data, wfile, ensure_ascii=False)
                        wfile.write('\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Select platform for attack prompt generation.')
    parser.add_argument('-p', '--platform', choices=['ali', 'openai', 'baidu','hug','flowgpt','coze','poe'], required=True, help='indicate the LLM app store to launch LLMThief')
    parser.add_argument('-t', '--type', choices=['instruction', 'api', 'knowledge'], required=True, help='indicate the LLMThief attack type')
    parser.add_argument('-l', '--level', choices=['1', '2', '3', '4'], required=True, help='indicate the attack level; 1: only seed, 2. seed + mutator, 3: seed + feature, 4: seed + mutator + feature')
    parser.add_argument('-n', '--number', type=int, default=0, help='an optional integer parameter, default is 0, used to skip some bots since they have already tested')
    
    #Usage: python main.py -p ali -t instruction -l 1 -n 0
    args = parser.parse_args()
    main(args.platform, args.type, args.level, args.number)
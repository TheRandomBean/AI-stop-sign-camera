import torch
import yaml
import subprocess

def config_load(filename, location, setting):
    try:
        with open(filename, "r") as output:
            config = yaml.safe_load(output)
        return config[location][setting]
    except FileNotFoundError:
        print("[!] config.yaml was not detected, please go to https://github.com/TheRandomBean/AI-stop-sign-camera and copy the config file. exitting...")
        exit()

def config_save(filename, location, setting, data):
    try:
        with open(filename, "r") as f:
            config = yaml.safe_load(f)
    
        if location not in config:
            config[location] = {}
            print(f"[?] Couldn't find location '{location}' in config.yaml")
            print(f"[!] Creating new location '{location}' in config.yaml")
        config[location][setting] = data

        with open(filename, "w") as f:
            yaml.dump(config, f, sort_keys=False)
    except FileNotFoundError:
        print("[!] config.yaml was not detected, please go to https://github.com/TheRandomBean/AI-stop-sign-camera and copy the config file. exitting...")
        exit()

def CudaCheck(): 
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    return device

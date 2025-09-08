import keyboard
import json
import logging
from logging import debug, info, warning, error, critical
import time
import os

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='log.log', filemode='a')

info("command module started")

debug("Loading keys from keys.json")

with open("config.json", "r") as f:
    config = json.load(f)
if config.get("first_start", True):
    warning("keys.json not found, initializing with empty dictionary")
    keys = {}
    with open("keys.json", "w") as f:
      json.dump(keys, f, indent=2)
      debug("keys.json created successfully")
    
if os.path.exists("keys.json"):
  with open("keys.json", "r") as f:
    keys = json.load(f)
else:
  warning("keys.json not found, initializing with empty dictionary")
  keys = {}
  with open("keys.json", "w") as f:
    json.dump(keys, f, indent=2)
    debug("keys.json created successfully")
  
debug("Keys loaded successfully")

debug("initializing functions")    

def execute(shortcut):
    key = keys[shortcut]
    
    if len(key) > 4:
        return
      
    for k in key[:-1]:
        keyboard.press(k)
        time.sleep(0.05)
    time.sleep(0.05)
    

    keyboard.press_and_release(key[-1])
    time.sleep(0.05)
    
    for k in reversed(key[:-1]):
        keyboard.release(k)
        time.sleep(0.05)
    
    info(f"Executed shortcut: {shortcut} -> {key}")


    
def add_shortcut(shortcut, keys_list):
  if shortcut in keys:
    warning(f"Shortcut already exists: {shortcut}")
  else:
    keys[shortcut] = keys_list
    with open("keys.json", "w") as f:
      json.dump(keys, f, indent=2)
    debug("keys.json updated successfully")
    info(f"Added shortcut: {shortcut} -> {keys_list}")
    
def repair_cached_shortcuts():
  try:
    global keys
    with open("keys.json", "r") as f:
      keys = json.load(f)
    with open("keys.json", "w") as f:
      newkeys = replace_spaces(keys)
      json.dump(newkeys, f, indent=4)
    debug("keys.json reloaded successfully")
  except Exception as e:
    error(f"Error reloading keys.json: {e}")
    
def replace_spaces(d):
    return {cle.replace(" ", "_"): valeur for cle, valeur in d.items()}
    
def list_shortcuts():
  if keys:
    return keys
  else:
    warning("No shortcuts found")
    return {}
  
def remove_shortcut(shortcut):
  if shortcut in keys:
    del keys[shortcut]
    with open("keys.json", "w") as f:
      json.dump(keys, f, indent=4)
    debug("keys.json updated successfully after removing shortcut")
    info(f"Removed shortcut: {shortcut}")
  else:
    warning(f"Shortcut not found for removal: {shortcut}")
    
info("Command module working correctly")
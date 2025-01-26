import json
import logging

logging.basicConfig(level=logging.DEBUG)

def load_bin_rules():
    try:
        logging.debug("Attempting to load bin rules.")
        with open('data/bin_rules.json', 'r') as f:
            data = json.load(f)
        logging.debug(f"Loaded bin rules: {data}")
        return data
    except FileNotFoundError:
        logging.error("Recycling rules file (bin_rules.json) not found.")
        raise Exception("Recycling rules file (bin_rules.json) not found.")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON file: {e}")
        raise Exception("Recycling rules file (bin_rules.json) is invalid.")

def classify_item(labels):
    try:
        bin_rules = load_bin_rules()
        logging.debug(f"Classifying labels: {labels}")
        for bin_name, items in bin_rules.items():
            for label in labels:
                if label in items:
                    logging.debug(f"Item '{label}' classified in bin: {bin_name}")
                    return bin_name
        return "Unknown bin"
    except Exception as e:
        logging.error(f"Error in classify_item: {e}")
        raise e

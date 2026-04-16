import logging

logging.basicConfig(level = logging.INFO, 
                    format = "%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__) 

import yaml

def load_config(path = "config/config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


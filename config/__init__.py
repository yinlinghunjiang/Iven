import json

"""
    Author: 霖念（Little-LinNian）
    用于读json数据
    :param config_path: The path of config.
    :var config_path: str
    
"""

def init_config(config_path: str):
    global CONFIG
    CONFIG = Config(config_path)
    return CONFIG


class Config:

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            config_content = json.load(f)
        self.mirai = config_content["mah"]
        self.huggin = config_content["hugginFace"]
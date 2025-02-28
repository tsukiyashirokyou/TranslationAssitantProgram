from . import globals
import json


def link_settings_load():
    if globals.LINK_SETTINGS_PATH.exists():
        with globals.LINK_SETTINGS_PATH.open('r') as link_setting_json_file:
            LINK_SETTINGS = json.load(link_setting_json_file)
    else:
            LINK_SETTINGS = {
                'base_url':'https://api.siliconflow.cn/v1',
                'api_key' :'sk-xtbjisneicpjcfmitnbfxlbtqksjvsyiwuxnvyuxieyblygf',
                'model':"Pro/deepseek-ai/DeepSeek-R1",
                'temperature':0.7,
                'top_p':1.0,
                'n':1.0,
                'max_tokens':4096,
                'presence_penalty':0.0,
                'frequency_penalty':0.0
            }
            globals.LINK_SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
            with globals.LINK_SETTINGS_PATH.open('w') as link_setting_json_file:
                json.dump(LINK_SETTINGS, link_setting_json_file, indent=4)
    globals.link_settings = LINK_SETTINGS
    return True
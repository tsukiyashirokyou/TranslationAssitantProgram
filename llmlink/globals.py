from pathlib import Path

LINK_SETTINGS_PATH = Path(__file__).parent.parent / "link_settings.json"

default_link_settings = {
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

link_settings = default_link_settings
max_chars = 2000
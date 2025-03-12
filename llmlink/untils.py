from ttkbootstrap.constants import *
import ttkbootstrap as ttk
from pathlib import Path
import re
import json

def stream_anwser_updata(scrooled_text,new_text):
    scrooled_text.insert(END, new_text)
    scrooled_text.see(END)
    return True

#txt文档文本拆分
def split_text(text_path, max_chars=2000):
    text_path = Path(text_path)
    if text_path.exists():
        with text_path.open('r',encoding='utf-8') as f:
            text = f.read()
    else:
        text=''
    paragraphs = text.split('\n')
    segments = []
    current_segment = ""
    for paragraph in paragraphs:
        # 如果当前段落能加入当前分段且不超出最大字符数
        if len(current_segment) + len(paragraph) + 2 <= max_chars:
            current_segment += paragraph + "\n"
        else:
            # 当前段落太大，先保存已有段落
            if current_segment:
                segments.append(current_segment.strip())
            # 如果单个段落超过 max_chars，则直接拆分段落
            if len(paragraph) > max_chars:
                for i in range(0, len(paragraph), max_chars):
                    segments.append(paragraph[i:i+max_chars])
                current_segment = ""
            else:
                current_segment = paragraph + "\n"
    if current_segment:
        segments.append(current_segment.strip())
    return segments

#载入术语表
def load_translation_glossary(glossary_file=None):
    if glossary_file is None:
        glossary_file = Path(__file__).parent.parent / 'glossary.txt'
    glossary = {}
    glossary_file = Path(glossary_file)
    if glossary_file.exists():
        with glossary_file.open('r',encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and ':' in line:
                    key, value = line.split(':', 1)
                    glossary[key.strip()] = value.strip()
        return glossary
    else:
        glossary_file.parent.mkdir(parents=True, exist_ok=True)
        with glossary_file.open('w',encoding='utf-8') as f:
            f.write('')
        return {}

#更新术语表
def update_translation_glossary(glossary, glossary_file='glossary.txt'):
    glossary_file = Path(glossary_file)
    with glossary_file.open('w',encoding='utf-8') as f:
        for key, value in glossary.items():
            f.write(f"{key}: {value}\n")

def parse_glossary_update(response_text):
    match = re.search(r'(\{[ \t\n]*"Glossary Updates".*\})', response_text, re.DOTALL)
    if match:
        try:
            glossary_updates = json.loads(match.group(1))
            return glossary_updates.get("Glossary Updates", [])
        except json.JSONDecodeError:
            return []
    return []

def separate_translation_and_glossary(response_text):
    if "===GLOSSARY_UPDATES===" in response_text:
        translation_text, glossary_text = response_text.split("===GLOSSARY_UPDATES===", 1)
    else:
        translation_text = response_text
        glossary_text = ""
    return translation_text.strip(), glossary_text.strip()




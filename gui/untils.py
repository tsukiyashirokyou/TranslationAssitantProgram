from ttkbootstrap.constants import *
import ttkbootstrap as ttk
from . import globals
from pathlib import Path
import json
from ttkbootstrap.dialogs import Messagebox
def reset_scrooled_text(scrooled_text, text):
    scrooled_text.delete(1.0, END)
    scrooled_text.insert(1.0, text)
    scrooled_text.see(END)
    return True

#载入原文历史
def load_original_history():
    #没有载入原文返回空
    if globals.current_original_path =='':
        return None
    #如果载入了文件，则尝试加载历史
    stem = globals.current_original_path.stem

    history_origin_path = Path(__file__).parent.parent / 'translate_history' /(stem+'_origin_history.json')
    
    history_list = []
    
    if history_origin_path.exists():
        # 如果存在历史,则返回历史
        with history_origin_path.open('r', encoding='utf-8') as f:
            history_list = json.load(f)
    else:
        #如果不存在历史则创建历史
        with history_origin_path.open('w', encoding='utf-8') as json_file:
            with globals.current_original_path.open('r', encoding='utf-8') as txt_file:
                history_list = txt_file.read().splitlines()
                history_list.insert(0, '1')
                json.dump(history_list, json_file, indent=4)
                
    return history_list

#载入参考译文历史
def load_translated_history():
    # 没有载入原文返回空
    if globals.current_translated_path == '':
        return None
    # 如果载入了文件，则尝试加载历史
    stem = globals.current_translated_path.stem

    history_translated_path = Path(__file__).parent.parent / 'translate_history' / (stem + '_translated_history.json')

    history_list = []

    if history_translated_path.exists():
        # 如果存在历史,则返回历史
        with history_translated_path.open('r', encoding='utf-8') as f:
            history_list = json.load(f)
    else:
        # 如果不存在历史则创建历史
        with history_translated_path.open('w', encoding='utf-8') as json_file:
            with globals.current_translated_path.open('r', encoding='utf-8') as txt_file:
                history_list = txt_file.read().splitlines()
                history_list.insert(0, '1')
                json.dump(history_list, json_file, indent=4)

    return history_list

def show_dialog_success(str):
    # 显示确认对话框
    result = Messagebox.okcancel(
        title="success",                   # 标题
        message=str,      # 内容
        bootstyle="success"                # 主题样式
    )
    if result == "OK":
        pass

def show_dialog_fail(str):
    # 显示确认对话框
    result = Messagebox.okcancel(
        title="danger",                   # 标题
        message=str,      # 内容
        bootstyle="danger"                # 主题样式
    )
    if result == "OK":
        pass

def debug():
    print('debug!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')






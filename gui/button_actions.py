import sys
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
from .untils import *
from llmlink.get_link import get_anwser_streamF
from llmlink.get_link import get_anwser_streamT
import threading
from tkinter.filedialog import askopenfilename
from llmlink.get_link import translate_txt
from llmlink import globals
from . import globals

def clear_button_action(scrool_text,context_dict_list):
    reset_scrooled_text(scrool_text,"")
    context_dict_list.clear()


def question_button_actionF_function(context_dict_list,input_stringvar,scrool_text):
    input = input_stringvar.get()
    input_stringvar.set('')
    context_dict_list = get_anwser_streamF(context_dict_list,input)
    context = ""
    for i in context_dict_list:
        context = context+i['role']+':\n'+i['content']+'\n'
    reset_scrooled_text(scrool_text,context)
    sys.exit()

def question_button_actionF(context_dict_list,input_stringvar,scrool_text):
    thread = threading.Thread(target=question_button_actionF_function,args=(context_dict_list,input_stringvar,scrool_text))
    thread.start()

def question_button_actionT(context_dict_list,input_stringvar,scrool_text):
    thread = threading.Thread(target=lambda:get_anwser_streamT(context_dict_list,input_stringvar,scrool_text))
    thread.start()
    scrool_text.see(END)

def select_directory(label):
    path = askopenfilename()
    if path:
        label.configure(text=path)

def translate_button_action(txt_label,glossary_label,output_label,max_chars=globals.max_chars):
    if txt_label.cget('text')=='请选择待翻译文件':
        show_dialog_fail('你没有选择待翻译文件！')
        return False

    thread = threading.Thread(target=lambda:translate_txt(txt_label.cget('text'),max_chars=globals.max_chars,
                  glossary_path=None if glossary_label.cget('text')=="请选择待字典文件(可不选),不选默认生成在项目目录下" else glossary_label.cget('text'),
                  output_path=None if output_label.cget('text')=="输出翻译路径(可不选),不选默认生成在项目目录下" else output_label.cget('text'))
    )
    thread.start()

def load_button_action(original_txt_label,translated_txt_label):

    if original_txt_label.cget('text') != '请选择原文':
        debug()
        globals.current_original_path = Path(original_txt_label.cget('text'))
        globals.history_list = load_original_history()
    if translated_txt_label.cget('text')!='请选择待参考译文':
        debug()
        globals.current_translated_path = Path(translated_txt_label.cget('text'))
        globals.translated_list = load_translated_history()



    return True




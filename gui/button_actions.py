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

def translate_button_action(txt_label,glossary_label,output_label,progress_bar,max_chars=globals.max_chars):
    if txt_label.cget('text')=='请选择待翻译文件':
        show_dialog_fail('你没有选择待翻译文件！')
        return False

    thread = threading.Thread(target=lambda:translate_txt(txt_label.cget('text'),
                                                          max_chars=globals.max_chars,
                                                          progress_bar = progress_bar,
                  glossary_path=None if glossary_label.cget('text')=="请选择待字典文件(可不选),不选默认生成在项目目录下" else glossary_label.cget('text'),
                  output_path=None if output_label.cget('text')=="输出翻译路径(可不选),不选默认生成在项目目录下" else output_label.cget('text'))
    )
    thread.start()

def load_button_action(original_txt_label,translated_txt_label,translation_output_path_label,notebook):
    from .assistant_page import get_frame
    if original_txt_label.cget('text') != '请选择原文':
        globals.current_original_path = Path(original_txt_label.cget('text'))
        globals.history_list = load_original_history()
    if translated_txt_label.cget('text')!='请选择待参考译文':
        globals.current_translated_path = Path(translated_txt_label.cget('text'))
        globals.translated_list = load_translated_history()
    if translation_output_path_label.cget('text')!="请选择翻译辅助功能的写入文件(不选默认生成在程序目录下)":
        globals.current_txt_path = Path(translation_output_path_label.cget('text'))
        globals.current_list = load_current_history()

    notebook.forget(2)
    notebook.add(get_frame(notebook), text='翻译辅助页面', sticky=NSEW)



    return True

def before_button_action():
    pass

def after_button_action(original_scrolled_text,
                        translated_scrolled_text,
                        input_scrolled_text,
                        ):
    if globals.current_original_path == '':#如果都没有载入原文，则不处理
        show_dialog_fail('未载入原文！')
        return False
    else:
        #补全翻译列表不包含的部分
        if globals.current_translated_path !='':
            while len(globals.history_list)>len(globals.translated_list):
                globals.translated_list.append('')
            skip_space(globals.translated_list)
        #跳过所有空行
        skip_space(globals.history_list)
        skip_space(globals.current_list)


        # ------原文处理------
        #如果没越界,则下一个
        next_pos = int(globals.history_list[0])
        if next_pos <=len(globals.history_list)-1:
            if next_pos+1!=len(globals.history_list):
                globals.history_list[0] = str(next_pos+1)#标记后移
            reset_scrooled_text(original_scrolled_text, globals.history_list[next_pos])
            #保存历史
            if globals.autosave:
                stem = globals.current_original_path.stem
                history_origin_path = Path(__file__).parent.parent / 'translate_history' / (stem + '_origin_history.json')
                with history_origin_path.open('w',encoding='utf-8') as history_file:
                    json.dump(globals.history_list, history_file,  indent=4)
        else:
            show_dialog_fail('已全部翻译完成！')
            return True

        #------参考译文处理------
        if globals.current_translated_path == '':
            pass
        else:
            next_pos = int(globals.translated_list[0])
            if next_pos <= len(globals.translated_list)-1:
                if next_pos+1 != len(globals.translated_list):
                    globals.translated_list[0] = str(next_pos+1)
                reset_scrooled_text(translated_scrolled_text,globals.translated_list[next_pos])
            else:
                globals.translated_list[0] = str(next_pos + 1)
                globals.translated_list.append('缺失')
                reset_scrooled_text(translated_scrolled_text,'缺失')
            if globals.autosave:
                stem = globals.current_translated_path.stem
                history_translated_path = Path(__file__).parent.parent / 'translate_history' / (
                            stem + '_history.json')
                with history_translated_path.open('w',encoding='utf-8') as history_file:
                    json.dump(globals.translated_list, history_file, indent=4)

        #------输入历史处理------
        if globals.current_list == None:
            globals.current_list = ['1']
        input_pos = int(globals.current_list[0])#输入需要访问的位置
        while input_pos < (int(globals.history_list[0])-1):
            globals.current_list.append('')
            input_pos += 1
        if input_pos <= len(globals.current_list)-1:#已经输入过
            reset_scrooled_text(input_scrolled_text,globals.current_list[input_pos])
            globals.current_list[0] = str(input_pos+1)#标记后移
        else:#未输入过
            if input_scrolled_text.get(1.0).strip()!='':
                globals.current_list.append(input_scrolled_text.get(1.0))#将当前输入加入输入文本历史
            else:
                globals.current_list.append(globals.history_list[int(globals.history_list[0])-1])
            globals.current_list[0] = str(input_pos+1)#标记后移
            reset_scrooled_text(input_scrolled_text,'')#清空显示
            if globals.autosave:#如果启用了自动保存则自动保存
                if globals.current_txt_path == '':
                    stem = globals.current_original_path.stem
                    #保存文件
                    savepath = Path(__file__).parent.parent / (stem + "_your_translated.txt")
                    with savepath.open('w', encoding="utf-8") as f:
                        for seg in globals.current_list[1:]:
                            f.write(seg+'\n')

                    #保存历史记录
                    json_savepath = Path(__file__).parent.parent / 'translate_history' / (stem + '_your_translated_history.json')
                    with json_savepath.open('w', encoding="utf-8") as f:
                        json.dump(globals.current_list,f,indent=4)
                else:
                    stem = globals.current_txt_path.stem
                    # 保存文件
                    savepath = globals.current_txt_path
                    with savepath.open('w', encoding="utf-8") as f:
                        for seg in globals.current_list[1:]:
                            f.write(seg)
                    # 保存历史记录
                    json_savepath = Path(__file__).parent.parent / 'translate_history' / (
                                stem + '_your_translated_history.json')
                    with json_savepath.open('w', encoding="utf-8") as f:
                        json.dump(globals.current_list, f, indent=4)

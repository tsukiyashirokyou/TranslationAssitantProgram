import ttkbootstrap as ttk
from dominate.tags import output
from scipy.cluster.hierarchy import weighted
from tqdm import tk
from ttkbootstrap.constants import *
from .button_actions import *
from ttkbootstrap.scrolled import ScrolledText
from tkinter import font
from . import globals
from . import untils

def get_frame(notebook):

    frame = ttk.Frame(notebook)
    
    txt_frame = ttk.Frame(frame,borderwidth=1,relief=SOLID)

    custom_font = font.Font(
        family='Source Han Sans',
        size=12,
        weight='bold',
    )

    # 文本查看的历史记录，记录前一次处理到的位置，没有会自动创建
    globals.history_list = untils.load_original_history()
    globals.translated_list = untils.load_translated_history()
    globals.current_list = untils.load_current_history()

    history_num = len(globals.history_list)-1 if globals.current_original_path!='' else 0

#-----------------------文本显示和编辑窗口--------------------------------------------
    original_text_label = ttk.Label(txt_frame, text="原文", padding=5, anchor=CENTER)
    original_scrolled_text = ScrolledText(txt_frame, padding=5,autohide=True,height=2,font=custom_font)

    original_text_label.grid(row=0, column=0, sticky=EW, padx=5, pady=5)
    original_scrolled_text.grid(row=0, column=1, sticky=EW, padx=5, pady=5,columnspan=2)

    if globals.history_list == None:
        untils.reset_scrooled_text(original_scrolled_text,'未载入原文')
    elif len(globals.history_list) > 1:
        pos = int(globals.history_list[0])
        if pos !=1:
            untils.reset_scrooled_text(original_scrolled_text,globals.history_list[pos-1])
        else:
            untils.reset_scrooled_text(original_scrolled_text, globals.history_list[pos])




    translated_text_label = ttk.Label(txt_frame, text="译文", padding=5, anchor=CENTER)
    translated_scrolled_text = ScrolledText(txt_frame, padding=5,autohide=True,height=2,font=custom_font)

    if globals.translated_list == None:
        untils.reset_scrooled_text(translated_scrolled_text,'未载入译文')
    elif len(globals.translated_list) > 1:
        pos = int(globals.translated_list[0])
        if pos !=1:
            untils.reset_scrooled_text(translated_scrolled_text,globals.translated_list[pos-1])
        else:
            untils.reset_scrooled_text(translated_scrolled_text,globals.translated_list[pos])
    translated_text_label.grid(row=1, column=0, sticky=EW, padx=5, pady=5)
    translated_scrolled_text.grid(row=1, column=1, sticky=EW, padx=5, pady=5,columnspan=2)
    
    input_label = ttk.Label(txt_frame, text="请输入你的翻译", padding=5, anchor=CENTER)
    input_scrolled_text = ScrolledText(txt_frame, padding=5,autohide=True,height=2,font=custom_font)

    input_label.grid(row=2, column=0, sticky=EW, padx=5, pady=5)
    input_scrolled_text.grid(row=2, column=1, sticky=EW, padx=5, pady=5,columnspan=2)

    if globals.current_list == None:
        pass
    elif len(globals.current_list) > 1:
        #-1是因为插入位置转化为末位
        untils.reset_scrooled_text(input_scrolled_text,globals.current_list[int(globals.current_list[0])-1])


    txt_frame.columnconfigure(0, weight=1)
    txt_frame.columnconfigure(1, weight=5)

    bar_style = ttk.Style(theme='superhero')
    bar_style.configure(
        "superhero.Custom.Horizontal.TProgressbar",
        thickness=30  # 调整垂直方向高度（默认20）
    )

    translation_progress_label = ttk.Label(txt_frame,text='当前翻译进度',anchor=CENTER)
    translation_progress_bar = ttk.Progressbar(txt_frame,style = "superhero.Custom.Horizontal.TProgressbar")


    translation_progress_label.grid(row=3, column=0, sticky=EW, padx=5, pady=5)
    translation_progress_bar.grid(row=3, column=1, sticky=EW,padx=5, pady=15)

    txt_frame.grid(row=0, column=0, sticky=EW, padx=5, pady=5,columnspan=2)
#------------------------------------------------------------------------------------

    before_button = ttk.Button(frame,text='前一句',command=lambda:before_button_action())
    after_button = ttk.Button(frame,text='后一句',command=lambda:after_button_action(original_scrolled_text,translated_scrolled_text,input_scrolled_text))

    before_button.grid(row=1, column=0, sticky=EW, padx=5, pady=5)
    after_button.grid(row=1, column=1, sticky=EW, padx=5, pady=5)






    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    return frame


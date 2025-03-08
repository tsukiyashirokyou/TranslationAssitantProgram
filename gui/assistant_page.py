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

    # 历史记录，记录前一次处理到的位置，没有会自动创建
    globals.history_list = untils.load_original_history()
    globals.translated_list = untils.load_translated_history()

    original_text_label = ttk.Label(txt_frame, text="原文", padding=5, anchor=CENTER)
    original_scrolled_text = ScrolledText(txt_frame, padding=5,autohide=True,height=2,font=custom_font)

    original_text_label.grid(row=0, column=0, sticky=EW, padx=5, pady=5)
    original_scrolled_text.grid(row=0, column=1, sticky=EW, padx=5, pady=5,columnspan=2)

    if globals.history_list == None:
        untils.reset_scrooled_text(original_scrolled_text,'未载入原文')
    elif len(globals.history_list) > 1:
        untils.reset_scrooled_text(original_scrolled_text,globals.history_list[int(globals.history_list[0])])



    translated_text_label = ttk.Label(txt_frame, text="译文", padding=5, anchor=CENTER)
    translated_scrolled_text = ScrolledText(txt_frame, padding=5,autohide=True,height=2,font=custom_font)

    if globals.translated_list == None:
        untils.reset_scrooled_text(translated_scrolled_text,'未载入译文')
    elif len(globals.translated_list) > 1:
        untils.reset_scrooled_text(translated_scrolled_text,globals.translated_list[int(globals.translated_list[0])])

    translated_text_label.grid(row=1, column=0, sticky=EW, padx=5, pady=5)
    translated_scrolled_text.grid(row=1, column=1, sticky=EW, padx=5, pady=5,columnspan=2)

    txt_frame.columnconfigure(0, weight=1)
    txt_frame.columnconfigure(1, weight=5)

    txt_frame.grid(row=0, column=0, sticky=EW, padx=5, pady=5,columnspan=10)

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    return frame


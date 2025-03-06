import ttkbootstrap as ttk
from dominate.tags import output
from tqdm import tk
from ttkbootstrap.constants import *
from .button_actions import *

def get_frame(notebook):

    frame = ttk.Frame(notebook)

#------------翻译功能

    file_path_label = ttk.Label(frame, text="请选择待翻译文件",padding=5,anchor=CENTER)
    file_path_button = ttk.Button(frame,text='选择',command=lambda:select_directory(file_path_label),padding=5)

    file_path_button.grid(row=0, column=0,sticky=EW,padx=5,pady=5)
    file_path_label.grid(row=0, column=1,sticky=EW,padx=5,pady=5)

    glossary_path_label = ttk.Label(frame, text="请选择待字典文件(可不选),不选默认生成在项目目录下",padding=5,anchor=CENTER)
    glossary_path_button = ttk.Button(frame, text='选择', command=lambda: select_directory(glossary_path_label),padding=5)

    glossary_path_button.grid(row=1, column=0, sticky=EW,padx=5,pady=5)
    glossary_path_label.grid(row=1, column=1, sticky=EW,padx=5,pady=5)

    output_path_label = ttk.Label(frame, text="输出翻译路径(可不选),不选默认生成在项目目录下",padding=5,anchor=CENTER)
    output_path_button = ttk.Button(frame, text='选择', command=lambda: select_directory(output_path_label),padding=5)

    output_path_label.grid(row=2, column=1, sticky=EW,padx=5,pady=5)
    output_path_button.grid(row=2, column=0, sticky=EW,padx=5,pady=5)



    translate_button = ttk.Button(frame,text='开始翻译',
                                  command=lambda:translate_button_action(
                                      txt_label=file_path_label,glossary_label=glossary_path_label,
                                      output_label=output_path_label))
    translate_button.grid(row=3, column=0, sticky=EW ,columnspan=2,padx=5,pady=5)



#-----------设置功能
    original_text_path_label = ttk.Label(frame, text="请选择原文",padding=5,anchor=CENTER)
    original_text_path_button = ttk.Button(frame,text='选择',command=lambda:select_directory(original_text_path_label),padding=5)

    original_text_path_button.grid(row=4, column=0,sticky=EW,padx=5,pady=5)
    original_text_path_label.grid(row=4, column=1,sticky=EW,padx=5,pady=5)

    translation_path_label = ttk.Label(frame, text="请选择待参考译文",padding=5,anchor=CENTER)
    translation_path_button = ttk.Button(frame,text='选择',command=lambda:select_directory(translation_path_label),padding=5)

    translation_path_button.grid(row=5, column=0,sticky=EW,padx=5,pady=5)
    translation_path_label.grid(row=5, column=1,sticky=EW,padx=5,pady=5)

    load_button = ttk.Button(frame, text='载入',
                                  command=lambda: load_button_action(
                                    original_txt_label=original_text_path_label,
                                    translated_txt_label=translation_path_label,
                                  )
                             )
    load_button.grid(row=6, column=0, sticky=EW, columnspan=2, padx=5, pady=5)




    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=2)

    return frame
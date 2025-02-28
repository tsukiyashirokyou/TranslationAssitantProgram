import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from .untils import *
from .button_actions import *
def get_frame(master):
    frame = ttk.Frame(master)
    context_dict_list = []
    context = ""
    scrooled_text = ScrolledText(frame,autohide=True,padding=5,height=20)
    scrooled_text.pack(fill = BOTH, expand = YES)
    reset_scrooled_text(scrooled_text,context)

    #输入框
    input_stringvar = ttk.StringVar()
    input_entry = ttk.Entry(frame,textvariable=input_stringvar)
    input_entry.pack(fill = BOTH, expand = YES,padx=5,pady=5)

    #提问按钮
    question_button = ttk.Button(frame,text="发出提问",command=
    lambda :question_button_actionT(context_dict_list,input_stringvar,scrooled_text))

    question_button.pack(fill = BOTH, expand = YES,padx=5,pady=5)

    #清空按钮
    clear_button = ttk.Button(frame,text='清空历史',command=
    lambda: clear_button_action(scrooled_text,context_dict_list))

    clear_button.pack(fill = BOTH, expand = YES,padx=5,pady=5)


    return frame



import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from . import llm_page
from . import  translation_and_setting_page
from . import assistant_page
def gui_show():
        root = ttk.Window(
                title="大模型与翻译和嵌入辅助程序",        #设置窗口的标题
                themename="superhero",     #设置主题
                size=(1066,650),        #窗口的大小
                position=(100,100),     #窗口所在的位置
                minsize=(0,0),          #窗口的最小宽高
                maxsize=(1920,1080),    #窗口的最大宽高
                alpha=1.0,              #设置窗口的透明度(0.0完全透明）
                )
        root.place_window_center()    #让显现出的窗口居中

        frame = ttk.Frame(root)
        frame.pack(fill=BOTH,padx=5,pady=5,side=TOP,expand=True)

        notebook = ttk.Notebook(frame)

        notebook.pack(side=TOP, fill=BOTH, expand=YES,padx=5,pady=5)
        notebook.add(llm_page.get_frame(notebook),text='大模型页面',sticky=NSEW)
        notebook.add(translation_and_setting_page.get_frame(notebook),text='翻译和设置页面',sticky=NSEW)
        notebook.add(assistant_page.get_frame(notebook), text='翻译辅助页面', sticky=NSEW)

        root.mainloop()

from ttkbootstrap.constants import *
import ttkbootstrap as ttk

def reset_scrooled_text(scrooled_text, text):
    scrooled_text.delete(1.0, END)
    scrooled_text.insert(1.0, text)
    scrooled_text.see(END)
    return True





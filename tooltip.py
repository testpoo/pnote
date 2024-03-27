# coding=utf-8

from tkinter import *
from tkinter.ttk import *
from config import *

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.font = get_config('font', 'font')

        self.style = Style()
        self.style.theme_use('default')
        self.style.configure("tooltip.TLabel",foreground="#404040",background="#ebedef",borderwidth=1,font=(self.font, "10", "normal"),relief='solid',justify='center',padding=[5,5,5,5])

    def enter(self, event):
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = Toplevel(self.widget)
        self.tw.overrideredirect(True)
        self.tw.geometry("+{}+{}".format(x, y))
        self.tw.attributes("-topmost", True)
        label = Label(self.tw, text=self.text, style="tooltip.TLabel")
        label.pack(ipadx=1)
    def leave(self, event):
        self.tw.destroy()
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

class ShowMessage:
    def __init__(self, widget, width, height, name, text, font):
        self.widget = widget
        self.width = width
        self.height = height
        self.text = text
        self.name = name
        self.font = font

        self.style = Style()
        self.style.theme_use('default')
        self.style.configure("showmessage.TLabel",foreground="#404040",background="#ebedef",borderwidth=0,font=(self.font, "10", "normal"),relief='solid',justify='center',padding=[50,50,50,50])

        self.sm = Toplevel(self.widget,background="#EBEDEF")
        self.sm.geometry("+%d+%d" % (self.widget.winfo_x() + (self.width-self.sm.winfo_reqwidth())/2, self.widget.winfo_y() + (self.height-self.sm.winfo_reqheight())/2))
        self.sm.title(name)
        self.sm.resizable(0,0)
        self.sm.attributes("-toolwindow",2)
        label = Label(self.sm, text=self.text, style="showmessage.TLabel")
        label.pack(ipadx=1)

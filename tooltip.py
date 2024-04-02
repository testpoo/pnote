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
        self.sm.transient(self.widget)
        label = Label(self.sm, text=self.text, style="showmessage.TLabel").pack(side="bottom")
        self.sm.focus()
        self.widget.attributes('-disabled','1')
        self.sm.protocol("WM_DELETE_WINDOW", self.quit)

    def quit(self):
        self.sm.destroy()
        self.widget.attributes('-disabled','0')
        self.widget.attributes("-topmost", True)

class QueryHelp:
    def __init__(self, widget, width, height, name, text, font):
        self.widget = widget
        self.width = width
        self.height = height
        self.text = text
        self.name = name
        self.font = font

        self.style = Style()
        self.style.theme_use('default')
        self.style.configure("Help.TLabel",foreground="#404040",background="#EBEDEF",borderwidth=0,font=(self.font,10),padding=[8,8,8,8])
        self.query_help = Toplevel(self.widget,background="#EBEDEF")
        self.query_help.geometry("%dx%d+%d+%d" % (300, 100, self.widget.winfo_x() + (self.width-300)/2, self.widget.winfo_y() + (self.height-100)/2))
        self.query_help.title(self.name)
        self.query_help.transient(self.widget)
        helpText = Text(self.query_help,font=(self.font, '11'),bg="#EBEDEF",padx=8,pady=8)
        helpText.insert(1.0,self.text)
        helpText.pack()
        helpText.config(state=DISABLED)
        self.query_help.focus()
        self.widget.attributes('-disabled','1')
        self.query_help.protocol("WM_DELETE_WINDOW", self.quit)

    def quit(self):
        self.query_help.destroy()
        self.widget.attributes('-disabled','0')
        self.widget.attributes("-topmost", True)

class About:
    def __init__(self, widget, width, height, name, font, *text):
        self.widget = widget
        self.width = width
        self.height = height
        self.text = text
        self.name = name
        self.font = font

        self.style = Style()
        self.style.theme_use('default')
        self.style.configure("AboutName.TLabel",foreground="#404040",background="#EBEDEF",borderwidth=0,font=(self.font,24,"bold"))
        self.style.configure("About.TLabel",foreground="#404040",background="#EBEDEF",borderwidth=0,font=(self.font,10),padding=[0,8,0,8])
        self.about = Toplevel(self.widget,background="#EBEDEF")
        self.about.geometry("%dx%d+%d+%d" % (300, 100, widget.winfo_x() + (self.width-300)/2, widget.winfo_y() + (self.height-100)/2))
        self.about.title(self.name)
        self.about.resizable(0,0)
        self.about.transient(self.widget)
        Label(self.about, text=self.text[0],style="AboutName.TLabel").pack()
        Label(self.about, text="Copyright © 2024 "+self.text[1],style="About.TLabel").pack()
        Label(self.about, text=self.text[2]+"：0.01",style="About.TLabel").pack()
        self.about.focus()
        self.widget.attributes('-disabled','1')
        self.about.protocol("WM_DELETE_WINDOW", self.quit)

    def quit(self):
        self.about.destroy()
        self.widget.attributes('-disabled','0')
        self.widget.attributes("-topmost", True)

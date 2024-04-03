# coding=utf-8

from tkinter import *
from tkinter.ttk import *
from config import *
 
class PText(Text):
    def __init__(self,*varg,**kw):
        self.images = {}
        self._undo_stack = []
        Text.__init__(self,*varg,**kw)
 
    def image_create(self,index,**options):
        img = options.get("image",None)
        name = Text.image_create(self,index,**options)
        self._undo_stack.append(['ins',name,''])
        if img is not None:
            self.images[name] = img # 这可能会删除名称相同但不同图像的引用
        return name
 
    def delete(self,*varg,**kw):
        Text.delete(self,*varg,**kw)
        self.clean_up_images()
 
    def clean_up_images(self):
        # 删除文本中不再存在的图像引用（通过.delete()调用）
        images_still_in_use = self.image_names()
        for name in set(self.images.keys()):
            if name not in images_still_in_use:
                del self.images[name]
 
    def destroy(self):
        self.images.clear() # 删除所有的图像引用
        return Text.destroy(self)

    def edit_reset(self):
        self._undo_stack = []
        Text.edit_reset(self)

    #def on_text_delete(self):
    #    print("testdel")
    #    if Text.index(self,"insert-1c") in [Text.index(self,temp[1]) for temp in self._undo_stack if temp[0] == 'ins']:
    #        img = Text.image_cget(self,"insert-1c",'image')
    #        self._undo_stack.append(['del','',img])

    def edit_undo(self):
        if self._undo_stack != []:
            image_index = Text.index(self,self._undo_stack[-1][1])
            if self._undo_stack[-1][0] == 'ins':
                if Text.index(self,"insert-1c") == image_index:
                    Text.delete(self,"insert-1c")
                    self._undo_stack.pop()
                else:
                    end = Text.index(self,"insert")
                    Text.edit_undo(self)
                    start = Text.index(self,"insert")
                    if int(image_index[2:]) > int(start[2:]) and int(image_index[2:]) < int(end[2:]):
                        Text.delete(self,"insert")
                        self._undo_stack.pop()
            elif self._undo_stack[-1][0] == 'del':
                if Text.index(self,"insert") == image_index:
                    Text.image_create(self, "insert",image=self._undo_stack[-1][2])
                    self._undo_stack.pop()
        else:
            Text.edit_undo(self)

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
        self.query_help.geometry("%dx%d+%d+%d" % (300, 300, self.widget.winfo_x() + (self.width-300)/2, self.widget.winfo_y() + (self.height-300)/2))
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
        self.style.configure("About.TLabel",foreground="#404040",background="#EBEDEF",borderwidth=0,font=(self.font,10),padding=[50,8,50,8])
        self.about = Toplevel(self.widget,background="#EBEDEF")
        self.about.geometry("+%d+%d" % (self.widget.winfo_x() + (self.width-self.about.winfo_reqwidth())/2, self.widget.winfo_y() + (self.height-self.about.winfo_reqheight())/2))
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
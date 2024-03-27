#!/usr/bin/env python3
# coding=utf-8

from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import os,shutil,sys
from config import *
from ptext import *
from tooltip import *
from PIL import ImageTk, Image
from io import BytesIO
from functools import partial

language = get_config('language', 'language')

if language == "chinese_simplified":
    from language.zh_CN import *
elif language == "chinese_traditional":
    from language.zh_TW import *
elif language == "english":
    from language.en_US import *

__author__ = {'name' : 'puyawei', 'created' : '2024-03-14', 'modify' : '2024-03-25'}

softname = "PNote"

#**实现界面功能****
class Application_ui(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title(softname)
        self.master["bg"]='#fff'
        self.position()
        self.createWidgets()

    def position(self):
        self.width = 1200
        self.height = 600
        screenwidth = note.winfo_screenwidth()
        screenheight = note.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        note.geometry(geometry)
        note.iconphoto(False, PhotoImage(file=os.getcwd() + '/images/pnote.png'))
        note.protocol("WM_DELETE_WINDOW",self.save_last_item)
        self.font = get_config('font', 'font')

    def createWidgets(self):
        self.style = Style()
        self.style.theme_use('default')
        self.style.configure("Top.TFrame",background="#fafafa",borderwidth=0,relief=FLAT)
        self.style.configure("Bottom.TFrame",background="#c7cbd1",borderwidth=0,relief=FLAT)
        self.style.configure("Top.TButton",foreground="#000",background="#fafafa",borderwidth=0,font=(self.font,10),anchor='center',relief=FLAT)
        self.style.configure("Bottom.TButton",foreground="#4a4a5a",background="#e0e2e6",borderwidth=0,font=(self.font,10),anchor='center',relief=FLAT)
        self.style.configure("taskBottom.TLabel",foreground="#404040",background="#c7cbd1",borderwidth=0,font=(self.font,10))
        self.style.configure("Bottom.TLabel",foreground="#404040",background="#c7cbd1",borderwidth=0,font=(self.font,10),padding=[10,0,0,0])
        self.style.configure("Treeview",background="#ebedef",fieldbackground="#ebedef")
        #self.style.configure('Treeview.Item', image=PhotoImage(file=os.getcwd() + '/open.png'))
        self.style.configure("Vertical.TScrollbar",background="#696f75",troughcolor="#444b53",font=(self.font,10),relief=FLAT,borderwidth=0)
        self.style.map('Vertical.TScrollbar',background=[('disabled', '#696f75'),('pressed', '!focus', '#b7b4ba'),('active', '#b7b4ba')])

        self.note = self.winfo_toplevel()

        # 菜单页面
        self.menuBar = Menu(self.note)
        self.note.config(menu=self.menuBar)

        # 文件菜单
        self.fileMenu = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label=PNOTE005, menu=self.fileMenu)
        self.fileMenu.add_command(label=PNOTE035,accelerator="Ctrl+N",command = self.new_db)
        self.fileMenu.add_command(label=PNOTE057,accelerator="Ctrl+O",command = self.open_db)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label=PNOTE018,accelerator="Ctrl+S",command = self.save_content)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label=PNOTE015,accelerator="Ctrl+Alt+B",command = self.backup_db)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label=PNOTE004,accelerator="Ctrl+Q",command = self.exit)

        # 编辑菜单
        self.editMenu = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label=PNOTE001, menu=self.editMenu)
        self.editMenu.add_command(label=PNOTE044,command = self.insert_picture)
        self.editMenu.add_separator()
        self.editMenu.add_command(label=PNOTE017,accelerator="Ctrl+F",command = self.find_word)
        self.editMenu.add_command(label=PNOTE058,accelerator="Ctrl+H",command = self.replace_word)
        self.editMenu.add_command(label=PNOTE011,accelerator="Ctrl+G",command = self.goto_line)
        self.editMenu.add_separator()
        self.editMenu.add_command(label=PNOTE006,accelerator="Ctrl+Z",command = self.undo)
        self.editMenu.add_command(label=PNOTE054,accelerator="Ctrl+Y",command = self.redo)
        self.editMenu.add_separator()
        self.editMenu.add_command(label=PNOTE014,accelerator="Ctrl+X",command = self.cut)
        self.editMenu.add_command(label=PNOTE053,accelerator="Ctrl+C",command = self.copy)
        self.editMenu.add_command(label=PNOTE028,accelerator="Ctrl+V",command = self.paste)
        self.editMenu.add_command(label=PNOTE027,accelerator="Del",command = self.delete)
        self.editMenu.add_separator()
        self.editMenu.add_command(label=PNOTE043,accelerator="Ctrl+A",command = self.select_all)

        # 格式菜单
        self.layoutMenu = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label=PNOTE039, menu=self.layoutMenu)
        self.layoutMenu.add_command(label=PNOTE048,command = self.auto_change_line)
        self.layoutMenu.add_command(label=PNOTE010,command = self.change_font)

        # 查看菜单
        self.languageMenu = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label=PNOTE007, menu=self.languageMenu)
        self.languageMenu.add_command(label=PNOTE061,command = self.language_chinese_simplified)
        self.languageMenu.add_command(label=PNOTE012,command = self.language_chinese_traditional)
        self.languageMenu.add_command(label=PNOTE020,command = self.language_english)

        # 帮助菜单
        self.helpMenu = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label=PNOTE003, menu=self.helpMenu)
        self.helpMenu.add_command(label=PNOTE050,command = self.query_help)
        self.helpMenu.add_command(label=PNOTE049,command = self.issue_report)
        self.helpMenu.add_command(label=PNOTE051,command = self.update)
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label=PNOTE002 + softname,command = self.about)

        #-----------------------------------------------------------------------
        # 顶部导航栏
        self.buttons = []
        self.topFrame = Frame(self.note,style="Top.TFrame")
        topButtons = [('clear','self.new_db',PNOTE035),('clear','self.open_db',PNOTE057),('clear','self.save_content',PNOTE018),('clear','self.backup_db',PNOTE015),('clear','self.insert_picture',PNOTE044),('clear','self.undo',PNOTE006),('clear','self.redo',PNOTE054),('clear','self.cut',PNOTE014),('clear','self.copy',PNOTE053),('clear','self.paste',PNOTE028),('clear','self.delete',PNOTE027)]
        for topButton in topButtons:
            self.image = PhotoImage(file=os.getcwd() + '/images/' + topButton[0] +'.png')
            self.topButton = Button(self.topFrame,image=self.image,command=eval(topButton[1]),style="Top.TButton")
            self.topButton.image = self.image # 这里要引用一下，否则图片会被回收不显示
            self.topButton.place(x=30*topButtons.index(topButton),y=0,height=30,width=30)
            Tooltip(self.topButton, topButton[2])
            self.buttons.append(self.topButton)

        #-----------------------------------------------------------------------
        # PanedWindow框架及左侧树
        self.panedWindow = PanedWindow(self.note,orient=HORIZONTAL)
        self.leftTreeview =Treeview(self.panedWindow,show=["tree"], selectmode="browse")
        self.panedWindow.add(self.leftTreeview)

        # 右侧文本和滚动条
        self.editTextVbar = Scrollbar(self.note, orient=VERTICAL)
        self.editText = PText(self.panedWindow,font=(self.font, '11'),fg="#d8dee9",bg="#303841",insertbackground="#f8ad56",undo=True,wrap='word',yscrollcommand=self.editTextVbar.set)
        self.panedWindow.add(self.editText)
        self.editTextVbar['command'] = self.editText.yview

        # 工具栏
        self.toolFrame = Frame(self.note)
        self.toolLabel = Label(self.toolFrame, anchor='center', style="taskBottom.TLabel")
        self.replaceWordLabel = Label(self.toolFrame, anchor='center', style="taskBottom.TLabel")
        self.toolEntry = Entry(self.toolFrame)
        self.replaceWordEntry = Entry(self.toolFrame)
        self.findNextButton = Button(self.toolFrame, command=lambda: self.find_next_prev(self.toolEntry, self.editText, self.leftTaskbarText, "next"),style="Bottom.TButton")
        self.findPrevButton = Button(self.toolFrame, command=lambda: self.find_next_prev(self.toolEntry, self.editText, self.leftTaskbarText, "prev"),style="Bottom.TButton")
        self.findAllButton = Button(self.toolFrame, command=lambda: self.find_all(self.toolEntry, self.editText, self.leftTaskbarText),style="Bottom.TButton")
        self.replaceButton = Button(self.toolFrame, command=lambda: self.replace_next(self.toolEntry, self.replaceWordEntry, self.editText, self.leftTaskbarText,),style="Bottom.TButton")
        self.replaceAllButton = Button(self.toolFrame, command=lambda: self.replace_all(self.toolEntry, self.replaceWordEntry, self.editText, self.leftTaskbarText),style="Bottom.TButton")
        self.clear_image = PhotoImage(file=os.getcwd() + '/images/clear.png')
        self.closeFrameButton = Button(self.toolFrame, image=self.clear_image,command=self.closed_tool_frame,style="Bottom.TButton")

        # 底部状态栏
        self.bottomFrame = Frame(self.note,style="Bottom.TFrame")
        self.leftTaskbarText = StringVar()
        self.leftTaskbarLabel = Label(self.bottomFrame,textvariable=self.leftTaskbarText,style="Bottom.TLabel")
        self.leftTaskbarText.set(PNOTE036 +" 1, " + PNOTE038 +" 1")
        self.rightTaskbarText = StringVar()
        self.rightTaskbarLabel = Label(self.bottomFrame,textvariable=self.rightTaskbarText,style="Bottom.TLabel")

        # 插入顶级目录
        self.select_last_item()

        # 创建树右键菜单
        self.rightClickMenuTreeview = Menu(self.leftTreeview, tearoff=False)
        self.rightClickMenuTreeview.add_command(label=PNOTE021, command=self.add_item)
        self.rightClickMenuTreeview.add_command(label=PNOTE059, command=self.delete_item)
        self.rightClickMenuTreeview.add_command(label=PNOTE030, command=self.rename_item)
 
        # 绑定右键点击事件到右键菜单
        self.leftTreeview.bind("<Button-3>", self.on_right_click)

        # 点击树
        self.leftTreeview.bind('<ButtonRelease-1>', self.node_selected)

        # 窗口大小变化
        self.note.bind('<Configure>',self.window_resize)

        # 获取光标位置
        self.editText.bind('<KeyPress>',self.cursor_move) # 键盘按下触发
        self.editText.bind('<KeyRelease>',self.cursor_move) # 键盘释放触发
        self.editText.bind('<ButtonPress>',self.cursor_move) # 鼠标按下触发
        self.editText.bind('<ButtonRelease>', self.cursor_move) # 鼠标释效触发

        # 文本修改时触发
        #self.editText.bind("<<Modified>>", self.editText.image_delete)

        # 新建数据库
        self.note.bind("<Control-N>", self.new_db)
        self.note.bind("<Control-n>", self.new_db)

        # 打开数据库
        self.note.bind("<Control-O>", self.open_db)
        self.note.bind("<Control-o>", self.open_db)

        # 保存文本
        self.note.bind("<Control-S>", self.save_content)
        self.note.bind("<Control-s>", self.save_content)

        # 备份数据库
        self.note.bind("<Control-Alt-B>", self.backup_db)
        self.note.bind("<Control-Alt-b>", self.backup_db)

        # 撤销
        self.editText.unbind_class("Text", "<Control-Z>")
        self.editText.unbind_class("Text", "<Control-z>")
        self.editText.bind_class("Text", "<Control-Z>", self.undo)
        self.editText.bind_class("Text", "<Control-z>", self.undo)
        #self.editText.bind("<Control-Z>", self.undo)
        #self.editText.bind("<Control-z>", self.undo)

        # 重做
        self.editText.unbind_class("Text", "<Control-Y>")
        self.editText.unbind_class("Text", "<Control-y>")
        self.editText.bind_class("Text", "<Control-Y>", self.redo)
        self.editText.bind_class("Text", "<Control-y>", self.redo)
        #self.note.bind("<Control-Y>", self.redo)
        #self.note.bind("<Control-y>", self.redo)

        # 跳转行
        self.note.bind("<Control-G>", self.goto_line)
        self.note.bind("<Control-g>", self.goto_line)

        # 查文字
        self.note.bind("<Control-F>", self.find_word)
        self.note.bind("<Control-f>", self.find_word)

        # 替换文字
        self.note.bind("<Control-H>", self.replace_word)
        self.note.bind("<Control-h>", self.replace_word)

#**实现具体的事件处理回调函数****
class Application(Application_ui):
    def __init__(self, master=None):
        Application_ui.__init__(self, master)
        self.image_list = []
        self.note_id = 'poo'

    # 其他------------------------------------------------------------------------------
    # 导航栏禁用按扭
    def disabled_button(self, event=None):
        self.editText.config(state=DISABLED)
        for button in self.buttons:
            if self.buttons.index(button) >= 2:
                button.config(state=DISABLED)

    # 导航栏禁用按扭恢复
    def normal_button(self, event=None):
        self.editMenu.entryconfig(PNOTE044, state=NORMAL)
        self.editText.config(state=NORMAL)
        for button in self.buttons:
            button.config(state=NORMAL)

    # 关闭工具栏
    def closed_tool_frame(self, event=None):
        self.toolFrame.place(x=0,y=0,height=0,width=0)
        self.editText.tag_delete("match")
        self.panedWindow.place(x=0,y=30,height=self.height-60,width=self.width-6)
        self.editTextVbar.place(x=self.width-6,y=30,height=self.height-60,width=6)
    # 文件------------------------------------------------------------------------------
    # 新建数据库
    def new_db(self, event=None):
        db_path = asksaveasfilename(filetypes=[(PNOTE025,['db'])],title=PNOTE035,initialfile=PNOTE022,defaultextension=".db")
        if db_path != '':
            save_config('db', 'pnotedb', db_path)
            with open(db_path,'w') as f:
                createNewDb()
            self.refresh_treeview()
            self.leftTreeview.selection_set('0')
            self.editText.delete(1.0, END)
            self.rightTaskbarText.set(PNOTE033 + "："+str(queryItems())+", "+ datetime.now().strftime("%Y-%m-%d"))
            self.disabled_button()

    # 打开数据库
    def open_db(self, event=None):
        db_path = askopenfilename(filetypes=[(PNOTE025,['db'])],title=PNOTE057,initialfile=PNOTE022,defaultextension=".db")
        if db_path != '':
            save_config('db', 'pnotedb', db_path)
            save_config('config', 'lastitem', '0')
            self.refresh_treeview()
            self.leftTreeview.selection_set('0')
            self.editText.delete(1.0, END)
            self.rightTaskbarText.set(PNOTE033 + "："+str(queryItems())+", "+ datetime.now().strftime("%Y-%m-%d"))
            self.disabled_button()

    # 保存
    def save_content(self, event=None):
        image_lists = []
        current = self.leftTreeview.selection()[0]
        content = self.editText.get(1.0, END)
        id = self.leftTreeview.item(current)['values'][0]
        self.image_list += queryImageInfo(id)
        updateContent(content,id)
        image_ids = self.editText.image_names()
        for image_id in image_ids:
            image_bytes = b''
            self.editText.update_idletasks()
            image_address = self.editText.index(image_id)
            for image in self.image_list:
                if image_id == str(image[0]):
                    image_bytes = image[2]
            image_lists.append((image_id,image_address,image_bytes))
        deleteImageInfo(id)
        for image in image_lists:
            insertImageInfo(id,image[0],image[1],image[2])

    # 备份数据库
    def backup_db(self, event=None):
        old_db_path = get_config('db', 'pnotedb')
        new_db_path = asksaveasfilename(filetypes=[(PNOTE025,['db'])],title=PNOTE015,initialfile=PNOTE022,defaultextension=".db")
        if new_db_path != '':
            shutil.copy(old_db_path, new_db_path)

    # 退出
    def exit(self, event=None):
        self.save_last_item()
        note.destroy()
    # 编辑------------------------------------------------------------------------------
    # 插入图片
    def insert_picture(self, event=None):
        current = self.leftTreeview.selection()[0]
        id = self.leftTreeview.item(current)['values'][0]
        try:
            image = Image.open(askopenfilename(filetypes=[(PNOTE025,['png','jpg','gif'])],title=PNOTE044,initialfile=PNOTE022,defaultextension=".png")) # 加载留片
            if image != '':
                current_size = image.size
                if current_size[1] > 200:
                    target_size = (current_size[0] * 500 / current_size[1],200)
                else:
                    target_size = current_size
                image.thumbnail(target_size)

                image_bytes = BytesIO()
                image.save(image_bytes, format='png')
                image_bytes = image_bytes.getvalue()
                image = ImageTk.PhotoImage(image)  # 创建ImageTk对象
                self.image_id_temp = self.editText.image_create(INSERT,image=image,name=self.note_id)  # 在光标位置新入图片
                self.editText.focus()
                self.image_list.append((self.image_id_temp,'',image_bytes))
        except Exception as e:
            print(e)

    # 查找文字
    def find_word(self, event=None):
        self.toolFrame.place(x=0,y=self.height-60,height=30,width=self.width)
        self.toolLabel.place(x=0,y=0,height=30,width=60)
        self.toolEntry.place(x=60,y=0,height=30,width=self.width-270)
        self.findNextButton.place(x=self.width-210,y=0,height=30,width=60)
        self.findPrevButton.place(x=self.width-150,y=0,height=30,width=60)
        self.findAllButton.place(x=self.width-90,y=0,height=30,width=60)
        for control in [self.replaceWordLabel,self.replaceWordEntry,self.replaceButton]:
            control.place(x=0,y=0,height=0,width=0)
        self.closeFrameButton.place(x=self.width-30,y=0,height=30,width=30)

        self.editText.tag_delete("match")
        self.toolLabel.config(text=PNOTE034)
        self.findNextButton.config(text=PNOTE055)
        self.findPrevButton.config(text=PNOTE045)
        self.findAllButton.config(text=PNOTE037)
        self.toolEntry.delete(0,END)

        self.panedWindow.place(x=0,y=30,height=self.height-90,width=self.width-6)
        self.editTextVbar.place(x=self.width-6,y=30,height=self.height-90,width=6)
        self.toolEntry.focus()

        self.toolEntry.bind('<Return>',partial(self.find_next_prev,self.toolEntry, self.editText, self.leftTaskbarText, "next"))

    def find_all(self, findWordEntry, editText, leftTaskbarText, event=None):
        editText.tag_remove("match", "1.0", END)
        count = 0
        if findWordEntry.get():
            cursor = "1.0"
            while True:
                cursor = editText.search(findWordEntry.get(), cursor, nocase=1, stopindex=END)
                if not cursor:
                    break
                lastcursor = '.'.join([cursor.split('.')[0],str(int(cursor.split('.')[1]) + len(findWordEntry.get()))])
                self.editText.mark_set("insert", lastcursor)
                self.editText.see("insert")  # 确保光标在可视范围内
                self.editText.focus()
                editText.tag_add("match", cursor, lastcursor)
                count += 1
                cursor = lastcursor
            editText.tag_config('match', foreground='yellow', background="green")
            self.toolFrame.place(x=0,y=0,height=0,width=0)
            self.panedWindow.place(x=0,y=30,height=self.height-60,width=self.width-6)
            self.editTextVbar.place(x=self.width-6,y=30,height=self.height-60,width=6)
            leftTaskbarText.set(str(count) + PNOTE032)

    def find_next_prev(self, findWordEntry, editText, leftTaskbarText, direction, event=None):
        content = self.editText.get(1.0,END)
        count = content.count(findWordEntry.get())
        if direction == "next":
            cursor = editText.search(findWordEntry.get(), self.editText.index(INSERT), nocase=1)
        elif direction == "prev":
            cursor = editText.search(findWordEntry.get(), self.editText.index(INSERT), nocase=1, backwards=True)
        if cursor:
            find_word_cursor = '.'.join([cursor.split('.')[0],str(int(cursor.split('.')[1]) + len(findWordEntry.get()))])
            if direction == "next":
                self.editText.mark_set("insert", find_word_cursor)
            elif direction == "prev":
                self.editText.mark_set("insert", cursor)
            editText.tag_delete("match")
            editText.tag_add("match", cursor, find_word_cursor)
            editText.tag_config('match', foreground='yellow', background="green")
            self.panedWindow.place(x=0,y=30,height=self.height-60,width=self.width-6)
            self.editTextVbar.place(x=self.width-6,y=30,height=self.height-60,width=6)
            leftTaskbarText.set(str(count) + PNOTE032)
        else:
            editText.tag_delete("match")
            leftTaskbarText.set(PNOTE031)

    # 替换文字
    def replace_word(self, event=None):
        self.toolFrame.place(x=0,y=self.height-92,height=62,width=self.width)
        self.replaceWordLabel.place(x=0,y=0,height=30,width=60)
        self.toolLabel.place(x=0,y=32,height=30,width=60)
        self.toolEntry.place(x=60,y=0,height=30,width=self.width-210)
        self.replaceWordEntry.place(x=60,y=32,height=30,width=self.width-210)
        self.findNextButton.place(x=self.width-150,y=0,height=30,width=60)
        self.findPrevButton.place(x=0,y=0,height=0,width=0)
        self.replaceButton.place(x=self.width-90,y=0,height=30,width=60)
        self.findAllButton.place(x=self.width-150,y=32,height=30,width=60)
        self.replaceAllButton.place(x=self.width-90,y=32,height=30,width=60)
        self.closeFrameButton.place(x=self.width-30,y=0,height=30,width=30)

        self.editText.tag_delete("match")
        self.replaceWordLabel.config(text=PNOTE034)
        self.toolLabel.config(text=PNOTE040)
        self.findNextButton.config(text=PNOTE019)
        self.replaceButton.config(text=PNOTE023)
        self.findAllButton.config(text=PNOTE037)
        self.replaceAllButton.config(text=PNOTE023)
        self.toolEntry.delete(0,END)

        self.panedWindow.place(x=0,y=30,height=self.height-90,width=self.width-6)
        self.editTextVbar.place(x=self.width-6,y=30,height=self.height-90,width=6)
        self.toolEntry.focus()

        self.toolEntry.bind('<Return>',partial(self.find_next_prev,self.toolEntry, self.editText, self.leftTaskbarText, "next"))

    def replace_next(self, findWordEntry, replaceWordEntry, editText, leftTaskbarText, event=None):
        content = self.editText.get(1.0,END)
        count = content.count(findWordEntry.get())
        cursor = editText.search(findWordEntry.get(), self.editText.index(INSERT), nocase=1)
        if cursor:
            find_word_cursor = '.'.join([cursor.split('.')[0],str(int(cursor.split('.')[1]) + len(findWordEntry.get()))])
            editText.delete(cursor, find_word_cursor)
            editText.insert(cursor, replaceWordEntry.get())
            replace_word_cursor = '.'.join([cursor.split('.')[0],str(int(cursor.split('.')[1]) + len(replaceWordEntry.get()))])
            self.editText.mark_set("insert", replace_word_cursor)
            editText.tag_delete("match")
            editText.tag_add("match", cursor, replace_word_cursor)
            editText.tag_config('match', foreground='yellow', background="green")
            self.panedWindow.place(x=0,y=30,height=self.height-60,width=self.width-6)
            self.editTextVbar.place(x=self.width-6,y=30,height=self.height-60,width=6)
            leftTaskbarText.set(str(count) + PNOTE024)
        else:
            editText.tag_delete("match")
            leftTaskbarText.set(PNOTE031)

    def replace_all(self, findWordEntry, replaceWordEntry, editText, leftTaskbarText, event=None):
        editText.tag_delete("match")
        count = 0
        if findWordEntry.get():
            cursor = "1.0"
            while True:
                cursor = editText.search(findWordEntry.get(), cursor, nocase=1, stopindex=END)
                if not cursor:
                    break
                lastcursor = '.'.join([cursor.split('.')[0],str(int(cursor.split('.')[1]) + len(findWordEntry.get()))])
                editText.delete(cursor, lastcursor)
                editText.insert(cursor, replaceWordEntry.get())
                replace_lastcursor = '.'.join([cursor.split('.')[0],str(int(cursor.split('.')[1]) + len(replaceWordEntry.get()))])
                self.editText.mark_set("insert", replace_lastcursor)
                self.editText.see("insert")  # 确保光标在可视范围内
                self.editText.focus()
                editText.tag_add("match", cursor, replace_lastcursor)
                count += 1
                cursor = replace_lastcursor
            editText.tag_config('match', foreground='yellow', background="green")
            self.toolFrame.place(x=0,y=0,height=0,width=0)
            self.panedWindow.place(x=0,y=30,height=self.height-60,width=self.width-6)
            self.editTextVbar.place(x=self.width-6,y=30,height=self.height-60,width=6)
            leftTaskbarText.set(str(count) + PNOTE052)

    # 跳转行
    def goto_line(self, event=None):
        self.toolFrame.place(x=0,y=self.height-60,height=30,width=self.width)
        self.toolLabel.place(x=0,y=0,height=30,width=60)
        self.toolEntry.place(x=60,y=0,height=30,width=self.width-60)
        for control in [self.replaceWordLabel,self.replaceWordEntry,self.findNextButton,self.findPrevButton,self.findAllButton,self.replaceButton]:
            control.place(x=0,y=0,height=0,width=0)
        self.closeFrameButton.place(x=self.width-30,y=0,height=30,width=30)

        self.editText.tag_delete("match")
        self.toolLabel.config(text=PNOTE011)
        self.toolEntry.delete(0,END)

        self.panedWindow.place(x=0,y=30,height=self.height-90,width=self.width-6)
        self.editTextVbar.place(x=self.width-6,y=30,height=self.height-90,width=6)
        self.toolEntry.focus()

        self.toolEntry.bind('<Return>',self.goto_text_line)

    def goto_text_line(self, event=None):
        if self.toolEntry.get() != '':
            index = '.'.join([self.toolEntry.get(),'0'])
            self.editText.mark_set("insert", index)
            self.editText.see("insert")  # 确保光标在可视范围内
            self.editText.focus()
        self.panedWindow.place(x=0,y=30,height=self.height-60,width=self.width-6)
        self.editTextVbar.place(x=self.width-6,y=30,height=self.height-60,width=6)
        self.toolFrame.place(x=0,y=0,height=0,width=0)

    # 撤消
    def undo(self, event=None):
        try:
            self.editText.edit_undo()
        except Exception as e:
            print(e)

    # 重做
    def redo(self, event=None):
        try:
            self.editText.edit_redo()
        except Exception as e:
            print(e)

    # 剪切
    def cut(self, event=None):
        self.editText.event_generate("<<Cut>>")

    # 复制
    def copy(self, event=None):
        self.editText.event_generate("<<Copy>>")

    # 粘贴
    def paste(self, event=None):
        self.editText.event_generate("<<Paste>>")

    # 删除
    def delete(self, event=None):
        self.editText.event_generate("<<Del>>")

    # 全选
    def select_all(self, event=None):
        self.editText.tag_add("sel", "1.0", "end")

    # 格式------------------------------------------------------------------------------
    # 自动换行
    def auto_change_line(self, event=None):
        if self.editText.cget('wrap') == 'word':
            self.editText.config(wrap='none')
        else:
            self.editText.config(wrap='word')

    # 字体
    def change_font(self, event=None):
        self.toolFrame.place(x=0,y=self.height-60,height=30,width=self.width)
        self.toolLabel.place(x=0,y=0,height=30,width=60)
        self.toolEntry.place(x=60,y=0,height=30,width=self.width-90)
        for control in [self.replaceWordLabel,self.replaceWordEntry,self.findNextButton,self.findPrevButton,self.findAllButton,self.replaceButton]:
            control.place(x=0,y=0,height=0,width=0)
        self.closeFrameButton.place(x=self.width-30,y=0,height=30,width=30)

        self.editText.tag_delete("match")
        self.toolLabel.config(text=PNOTE010)
        self.toolEntry.delete(0, END)  # 清空文本框
        font = get_config('font', 'font')
        self.toolEntry.insert(0, font)  # 设置新文本

        self.panedWindow.place(x=0,y=30,height=self.height-90,width=self.width-6)
        self.editTextVbar.place(x=self.width-6,y=30,height=self.height-90,width=6)
        self.toolEntry.focus()

        self.toolEntry.bind('<Return>',self.change_font_to_config)

    def change_font_to_config(self, event=None):
        font = self.toolEntry.get()
        save_config('font', 'font', font)
        self.closed_tool_frame()

    # 语言------------------------------------------------------------------------------
    # 中文简体
    def language_chinese_simplified(self, event=None):
        save_config('language', 'language', 'chinese_simplified')
        # 重启
        path = sys.executable
        os.execl(path, "python", * sys.argv)

    # 中文繁体
    def language_chinese_traditional(self, event=None):
        save_config('language', 'language', 'chinese_traditional')
        # 重启
        path = sys.executable
        os.execl(path, "python", * sys.argv)

    # 英文
    def language_english(self, event=None):
        save_config('language', 'language', 'english')
        # 重启
        path = sys.executable
        os.execl(path, "python", * sys.argv)

    # 帮助------------------------------------------------------------------------------
    # 查看帮助
    def query_help(self, event=None):
        showinfo(title=PNOTE050, message=PNOTE062)

    # 缺陷报告
    def issue_report(self, event=None):
        showinfo(title=PNOTE049, message="https://github.com/testpoo")

    # 更新
    def update(self, event=None):
        showinfo(title=PNOTE051 + softname, message=PNOTE013)

    # 关于
    def about(self, event=None):
        about = "PNote\nCopyright © 2024 "+PNOTE046+"\n"+PNOTE008+"：0.01"
        showinfo(title=PNOTE002 + softname, message=about)
    # ------------------------------------------------------------------------------
    # 插入顶级目录
    def query_zero(self, event=None):
        self.folder_image = PhotoImage(file=os.getcwd() + '/images/folder.png')
        self.file_image = PhotoImage(file=os.getcwd() + '/images/file.png')
        self.file_save = PhotoImage(file=os.getcwd() + '/images/filesave.png')
        self.leftTreeview_first = self.leftTreeview.insert("", 'end',iid='0', values='', text=PNOTE026, open=False,image=self.file_save)
        self.insert_child_items('0',self.leftTreeview_first)

    # 左侧栏插入子元素
    def insert_child_items(self, pid, parent_node, event=None):
        try:
            items = queryItem(pid)
            for item in items:
                if queryItem(item[0]) != []:
                    self.leftTreeview.insert(parent_node, 'end',iid=item[1], values=item[0], text=" "+item[2],image=self.folder_image)
                    self.insert_child_items(item[0],self.leftTreeview.get_children(parent_node)[-1])
                else:
                    self.leftTreeview.insert(parent_node, 'end',iid=item[1], values=item[0], text=" "+item[2],image=self.file_image)
        except Exception as e:
            print(e)

    # 左侧栏节点选择
    def node_selected(self, event=None):
        current = self.leftTreeview.selection()[0]
        if current != "0":
            self.normal_button()
            id = self.leftTreeview.item(current)['values'][0]
            name = self.leftTreeview.item(current)['text']
            self.note.title(name + " - PNote")
            content = queryContent(id)
            self.editText.delete(1.0, END)
            if content == []:
                pass
            elif content[0][0] == None:
                pass
            else:
                self.editText.insert(1.0, content[0][0])

            images = queryImageInfo(id)
            if images:
                for img in images:
                    image_data = BytesIO(img[2])
                    image=Image.open(image_data)
                    image = ImageTk.PhotoImage(image)
                    self.editText.image_create(img[1], image=image, name=img[0])
            self.editText.focus()
            self.editText.edit_reset()
        else:
            self.editText.delete(1.0, END)
            self.editMenu.entryconfig(PNOTE044, state=DISABLED)
            self.disabled_button()
    # ------------------------------------------------------------------------------
    # 窗口大小变化更新布局
    def window_resize(self, event=None):
        if event is not None:
            if self.width != note.winfo_width() or self.height != note.winfo_height():
                self.width = note.winfo_width()
                self.height = note.winfo_height()
                self.topFrame.place(x=0,y=0,height=30,width=self.width)
                self.bottomFrame.place(x=0,y=self.height-30,height=30,width=self.width)
                self.panedWindow.place(x=0,y=30,height=self.height-60,width=self.width-6)
                self.editTextVbar.place(x=self.width-6,y=30,height=self.height-60,width=6)
                self.leftTaskbarLabel.place(x=0,y=0,height=30,width=200)
                self.rightTaskbarLabel.place(x=self.width-170,y=0,height=30,width=170)

                if self.toolLabel.cget("text") in [PNOTE042,PNOTE010,PNOTE011]:
                    self.toolFrame.place(x=0,y=self.height-60,height=30,width=self.width)
                    self.toolEntry.place(x=60,y=0,height=60,width=self.width-90)
                    self.closeFrameButton.place(x=self.width-30,y=0,height=30,width=30)
                elif self.toolLabel.cget("text") == PNOTE034:
                    self.toolFrame.place(x=0,y=self.height-60,height=30,width=self.width)
                    self.toolEntry.place(x=60,y=0,height=30,width=self.width-270)
                    self.findNextButton.place(x=self.width-210,y=0,height=30,width=60)
                    self.findPrevButton.place(x=self.width-150,y=0,height=30,width=60)
                    self.findAllButton.place(x=self.width-90,y=0,height=30,width=60)
                    self.closeFrameButton.place(x=self.width-30,y=0,height=30,width=30)
                elif self.toolLabel.cget("text") == PNOTE040:
                    self.toolFrame.place(x=0,y=self.height-92,height=62,width=self.width)
                    self.toolEntry.place(x=60,y=0,height=30,width=self.width-210)
                    self.replaceWordEntry.place(x=60,y=32,height=30,width=self.width-210)
                    self.findNextButton.place(x=self.width-150,y=0,height=30,width=60)
                    self.replaceButton.place(x=self.width-90,y=0,height=30,width=60)
                    self.findAllButton.place(x=self.width-150,y=32,height=30,width=60)
                    self.replaceAllButton.place(x=self.width-90,y=32,height=30,width=60)
                    self.closeFrameButton.place(x=self.width-30,y=0,height=30,width=30)

    # 刷新treeview
    def refresh_treeview(self, event=None):
        self.leftTreeview.delete(*self.leftTreeview.get_children())
        self.query_zero()

    # ------------------------------------------------------------------------------
    # 获取鼠标位置
    def cursor_move(self, event=None):
        line,column = self.editText.index(INSERT).split('.')
        column = str(int(column) + 1)
        self.leftTaskbarText.set(PNOTE036 + " " + line + ", " + PNOTE038 + " " + column)
        if get_config('db', 'pnotedb') == '0':
            self.rightTaskbarText.set(PNOTE033 + "：0"+", "+ datetime.now().strftime("%Y-%m-%d"))
        else:
            self.rightTaskbarText.set(PNOTE033 + "："+str(queryItems())+", "+ datetime.now().strftime("%Y-%m-%d"))
    # ------------------------------------------------------------------------------
    def on_right_click(self, event=None):
        item = self.leftTreeview.identify("item", event.x, event.y)
        if item:
            self.leftTreeview.selection_set(item)
            self.node_selected()
        # 创建菜单
        self.rightClickMenuTreeview.post(event.x_root, event.y_root)

    # 添加子项
    def add_item(self, event=None):
        current = self.leftTreeview.selection()[0]
        if current == "0":
            id = 0
        else:
            id = self.leftTreeview.item(current)['values'][0]
        if queryMaxIid()[0][0] == None:
            item_iid = 1
        else:
            item_iid = int(queryMaxIid()[0][0]) + 1
        self.leftTreeview.insert(current, 'end',iid=item_iid, values=id, text=PNOTE056,image=self.file_image)
        addItem(id,item_iid,PNOTE056)
        self.refresh_treeview()
        self.leftTreeview.selection_set(item_iid)
        self.node_selected()
        self.leftTreeview.see(item_iid)  # 滚动Treeview使得该行可见
        self.rightTaskbarText.set(PNOTE033 + "："+str(queryItems())+", "+ datetime.now().strftime("%Y-%m-%d"))

    # 删除当前项
    def delete_item(self, event=None):
        current = self.leftTreeview.selection()[0]
        parent = self.leftTreeview.parent(current)
        if current != '0':
            id = self.leftTreeview.item(current)['values'][0]
            if queryItem(id) == []:
                self.leftTreeview.delete(current)
                deleteItem(id)
            else:
                showinfo(PNOTE016,PNOTE009,icon="warning")
        self.refresh_treeview()
        self.leftTreeview.selection_set(parent)
        self.node_selected()
        self.leftTreeview.see(parent)  # 滚动Treeview使得该行可见
        self.rightTaskbarText.set(PNOTE033 + "："+str(queryItems())+", "+ datetime.now().strftime("%Y-%m-%d"))

    # 重命名当前项
    def rename_item(self, event=None):
        current = self.leftTreeview.selection()[0]
        if current != '0':
            id = self.leftTreeview.item(current)['values'][0]
            old_name = self.leftTreeview.item(current)['text'].strip()
            self.toolEntry.insert(0,old_name)
            self.toolFrame.place(x=0,y=self.height-60,height=30,width=self.width)
            self.toolLabel.place(x=0,y=0,height=30,width=60)
            self.toolEntry.place(x=60,y=0,height=30,width=self.width-90)
            for control in [self.replaceWordLabel,self.replaceWordEntry,self.findNextButton,self.findPrevButton,self.findAllButton,self.replaceButton]:
                control.place(x=0,y=0,height=0,width=0)
            self.closeFrameButton.place(x=self.width-30,y=0,height=30,width=30)

            self.editText.tag_delete("match")
            self.toolLabel.config(text=PNOTE042)
            self.toolEntry.delete(0, END)  # 清空文本框
            new_name = self.leftTreeview.item(current)['text'].strip()
            self.toolEntry.insert(0, new_name)  # 设置新文本

            self.panedWindow.place(x=0,y=30,height=self.height-90,width=self.width-6)
            self.editTextVbar.place(x=self.width-6,y=30,height=self.height-90,width=6)
            self.toolEntry.focus()

            self.toolEntry.bind('<Return>',self.rename_item_to_db)

    def rename_item_to_db(self, event=None):
        current = self.leftTreeview.selection()[0]
        id = self.leftTreeview.item(current)['values'][0]
        self.new_name = self.toolEntry.get()
        renameItem(self.new_name,id)
        self.leftTreeview.update()
        self.toolFrame.place(x=0,y=0,height=0,width=0)
        self.panedWindow.place(x=0,y=30,height=self.height-60,width=self.width-6)
        self.editTextVbar.place(x=self.width-6,y=30,height=self.height-60,width=6)
        self.refresh_treeview()
        self.leftTreeview.selection_set(current)
        self.leftTreeview.see(current)  # 滚动Treeview使得该行可见

    # ------------------------------------------------------------------------------
    # 记录最后选择的条目并在打开时跳转到该条目
    def save_last_item(self, event=None):
        if get_config('db', 'pnotedb') != '0':
            current = self.leftTreeview.selection()[0]
            save_config('config', 'lastitem', current)
        note.destroy()

    def select_last_item(self, event=None):
        if not os.path.exists(os.getcwd() + '/' + config_file):
            with open(os.getcwd() + '/' + config_file, 'w') as f:
                f.write("[config]\nlastitem=0\n\n[db]\npnotedb=0\n\n[font]\nfont=Console\n\n[language]\nlanguage = chinese_simplified")

        if get_config('db', 'pnotedb') == '0':
            self.editText.insert(1.0, PNOTE047)
            self.editMenu.entryconfig(PNOTE044, state=DISABLED)
            self.disabled_button()
        else:
            self.query_zero()
            current = get_config('config', 'lastitem')
            self.leftTreeview.selection_set(current)
            self.leftTreeview.see(current)  # 滚动Treeview使得该行可见
            self.node_selected()

        if get_config('db', 'pnotedb') == '0':
            self.rightTaskbarText.set(PNOTE033 + "：0"+", "+ datetime.now().strftime("%Y-%m-%d"))
        else:
            self.rightTaskbarText.set(PNOTE033 + "："+str(queryItems())+", "+ datetime.now().strftime("%Y-%m-%d"))

if __name__ == "__main__":
    note = Tk()
    Application(note).mainloop()

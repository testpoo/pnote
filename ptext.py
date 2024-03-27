# coding=utf-8

from tkinter import Text
 
class PText(Text):
    def __init__(self,*varg,**kw):
        self.images = {}
        Text.__init__(self,*varg,**kw)
 
    def image_create(self,index,**options):
        img = options.get("image",None)
        name = Text.image_create(self,index,**options)
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
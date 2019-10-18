import time
import gc
import random
from os.path import join
import os
from PIL import Image
import ipywidgets as widgets
import matplotlib.pyplot as plt
import pickle
from IPython.display import display,clear_output
import io

class Updater:
    def __init__(self, path, widget):
        self.path = path
        self.widget = widget
        self.widget_updated_time = 0
        
    def need_update(self):
        file_modified_time = os.path.getmtime( self.path )
        return (file_modified_time - self.widget_updated_time) > 0
    
    def reload(self):
        if self.need_update():
            self.update()
            self.widget_updated_time = time.time()
            
    def update(self):
        pass
    
class ImageUpdater(Updater):

    def update(self):

        imglist = ImageUpdater._getfiles(self.path, True)
        if len(imglist) > 0:
            newest_filepath = imglist[0]
            
            file = open(join(self.path, newest_filepath), "rb")
            bimg = file.read()
            file.close()
        else:
            img = Image.new('RGB', (100, 100))
            bimg = ImageUpdater.image_to_byte_array(img)
            
        
        self.widget.value = bimg
        
    @staticmethod
    def image_to_byte_array(image):
        imgByteArr = io.BytesIO()
        image.save(imgByteArr, format='PNG')
        imgByteArr = imgByteArr.getvalue()
        return imgByteArr
            
    @staticmethod
    def _getfiles(dirpath, newest_first=True):
        a = [s for s in os.listdir(dirpath)
             if os.path.isfile(os.path.join(dirpath, s))]
        a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)), reverse=newest_first)
        return a

class GraphUpdater(Updater):
    
    def __init__(self, path, widget):
        super().__init__(path, widget)
        self.fig, self.axes = plt.subplots()
    
    def need_update(self):
        return True
    def update(self):
        data = pickle.load( open( self.path, "rb" ) )
        X = data['x']
        Y = data['y']
        M = max(Y)
        with self.widget:
            clear_output(wait=True)
            plt.ylim(bottom=0, top=M+M//3)
            plt.plot( X, Y) 
            plt.show(self.fig)

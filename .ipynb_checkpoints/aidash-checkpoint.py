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
    
    def __init__(self, path, widget, ylim = None):
        super().__init__(path, widget)
        self.fig, self.axes = plt.subplots()
        self.ylim = ylim
        self.prev_data = {'x':[], 'y':[]}
    
    def need_update(self):
        return True
    def update(self):
        try:
            data = pickle.load( open( self.path, "rb" ) )
            self.prev_data = data
        except:
            data = self.prev_data


        X = data['x']
        Y = data['y']
        label = data.get('title', 'NoTitle')
        if len(Y)>0:
            M = max(Y)
        else:
            M=100
        
        with self.widget:
            clear_output(wait=True)
            if self.ylim == None:
                plt.ylim(bottom=0, top=M+M//3)
            else:
                plt.ylim(bottom=self.ylim[0], top=self.ylim[1])
            plt.plot( X, Y) 
            plt.title(label)
            plt.show(self.fig)

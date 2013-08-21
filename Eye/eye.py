'''
Created on 2013.8.19

@author: nEver
'''

import datetime
import Tkinter
from PIL import Image, ImageTk

class Window(Tkinter.Frame):
    def __init__(self):
        Tkinter.Frame.__init__(self, width = '800p', height = '600p')
        self.grid()
        image = Image.open('rei.jpg')
        width, height = image.size
        self.photo_image = ImageTk.PhotoImage(Image.open('rei.jpg'))
        #Image.open('rei.jpg').show()
        self.canvas = Tkinter.Canvas(self, width = width, height = height)
        print self.canvas.size()
        self.canvas.create_image(width / 2.0, height / 2.0, image = self.photo_image)
        #self.canvas.pack()
        self.canvas.grid()

if __name__ == '__main__':
    start_time = datetime.datetime.now()
    
    window = Window()
    window.mainloop()
        
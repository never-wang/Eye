'''
Created on 2013.8.19

@author: nEver
'''

import datetime
import Tkinter
from PIL import Image, ImageTk
import ctypes

'''state can be "rest", "wait_work", "work"'''
state = "wait_work"
#REST_TIME = datetime.timedelta(seconds = 10)
REST_TIME = datetime.timedelta(minutes = 10)
WORK_TIME = datetime.timedelta(minutes = 50)
#WORK_TIME = datetime.timedelta(seconds = 10)

class Window(Tkinter.Frame):
    def __init__(self):
        monitor_width = ctypes.windll.user32.GetSystemMetrics(0)
        monitor_height = ctypes.windll.user32.GetSystemMetrics(1)
        Tkinter.Frame.__init__(self, width = monitor_width, height = monitor_height)
        '''removes all window manager decorations from the window'''
        self.winfo_toplevel().overrideredirect(True)
        '''force a widget to be a certain size, regardless of the size of its contents'''
        self.grid_propagate(0)
        self.grid()
        
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight() 
        
        image = Image.open('rei.jpg')
        image_width, image_height = image.size
        '''resize image'''
        ratio = max(1.0 * width / image_width, 1.0 * height / image_height)
        image = image.resize((int(image_width * ratio), int(image_height * ratio)), Image.BILINEAR)
        image_width, image_height = image.size
        self.photo_image = ImageTk.PhotoImage(image)
        #Image.open('rei.jpg').show()
        #self.canvas.create_image(image_width / 2, image_height / 2 , image = self.photo_image)
        self.background = Tkinter.Label(self, image = self.photo_image)
        #self.canvas.pack()
        self.background.place(x = 0, y = 0, height = image_height, width = image_width)
        
        self.time = Tkinter.Label(self, bg='white', font = ('Times', '32'))
        self.time.grid(sticky = Tkinter.N)
        '''set the width of cell 0, which place the time'''
        self.columnconfigure(0, weight = monitor_width)
        
        '''add a start work button'''
        self.work = Tkinter.Button(self, text = "Start Work !", command = self.__start_work, 
                                   font = ('Times', '30'));
        '''set the width and height of cell 0, which place the button'''
        self.columnconfigure(0, weight = monitor_width)
        self.rowconfigure(1, weight = monitor_height)
        
        self.set_wait_work_state()
        
        self.tick()
        
    def set_rest_state(self):     
        self.state = 'rest'
        self.start_time = datetime.datetime.now()
        self.winfo_toplevel().deiconify()    
        
    def set_wait_work_state(self):
        self.state = 'wait_work'
        self.start_time = datetime.datetime.now()
        self.work.grid()
        self.winfo_toplevel().deiconify()
        
    def set_work_state(self): 
        self.state = 'work'
        self.start_time = datetime.datetime.now()
        self.winfo_toplevel().withdraw()
        self.work.grid_remove()
        
    def __start_work(self):
        self.set_work_state()
        
    def format_timedelta(self, time_delta):
        day = str(time_delta.days)
        hour = str(time_delta.seconds // 3600)
        min = str((time_delta.seconds // 60) % 60) 
        sec = str(time_delta.seconds % 60)
        return (day.rjust(2, '0') + ":" + hour.rjust(2, '0') + ":"  + min.rjust(2, '0')+ 
                ":" + sec.rjust(2, '0'))
        
    def tick(self):
        global REST_TIME, WORK_TIME
        
        cur_time = datetime.datetime.now()
        time_delta = cur_time - self.start_time 
        
        if self.state == 'rest':
            if time_delta > REST_TIME :
                self.set_wait_work_state()
        elif self.state == 'work':
            if time_delta > WORK_TIME : 
                self.set_rest_state()
        
        '''show time'''
        self.time.after(1000, self.tick)
        time_delta = cur_time - self.start_time
        self.time.config(text = self.format_timedelta(time_delta))
        

if __name__ == '__main__':
    window = Window()
    window.mainloop()
        
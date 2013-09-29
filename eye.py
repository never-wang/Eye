'''
Created on 2013.8.19

@author: nEver
'''

import datetime
import wx
#from PIL import Image, ImageTk
import platform
try:
    import gtk
except:
    pass    
import config
#import tray

import ctypes

CONFIG_FILENAME = 'config.ini'

class Window(wx.Frame):
    def __init__(self):
        if platform.system() == 'Windows':
            monitor_width = ctypes.windll.user32.GetSystemMetrics(0)
            monitor_height = ctypes.windll.user32.GetSystemMetrics(1)
        elif platform.system() == 'Linux':
            monitor_width = gtk.gdk.screen_width()
            monitor_height = gtk.gdk.screen_height()
        else :
            exit

        self.config = config.Config(CONFIG_FILENAME)
        
        wx.Frame.__init__(self, None)
        self.ShowFullScreen(True)
        '''removes all window manager decorations from the window'''
        '''force a widget to be a certain size, regardless of the size of its contents'''
        
        width = monitor_width
        height = monitor_height 
        
        image = wx.Image(self.config.image_file(), type = wx.BITMAP_TYPE_ANY)
        image_width, image_height = image.GetSize()
        '''resize image'''
        ratio = max(1.0 * width / image_width, 1.0 * height / image_height)
        image.Rescale(int(image_width * ratio), int(image_height * ratio))
        image_width, image_height = image.GetSize()
        #Image.open('rei.jpg').show()
        #self.canvas.create_image(image_width / 2, image_height / 2 , image = self.photo_image)
        self.background = wx.StaticBitmap(self, bitmap = wx.BitmapFromImage(image), size = (image_width, image_height))
        self.background.Show()
        
        return 
        #self.canvas.pack()
        
        self.time = wx.StaticText(self, bg='white', font = ('Times', '32'))
        self.time.grid(sticky = Tkinter.N)
        '''set the width of cell (0, 0), which place the time'''
        self.columnconfigure(0, weight = monitor_width)
        
        '''add a start work button'''
        self.work = Tkinter.Button(self, text = "Start Work !", command = self.start_work, 
                                   font = ('Times', '30'));
        '''set the width and height of cell (0, 0), which place the button'''
        self.columnconfigure(0, weight = monitor_width)
        self.rowconfigure(1, weight = monitor_height)
        
        self.set_wait_work_state()
        
        self.tick()
        
        tray.Tray(self)

    def time_reset(self):
        self.time.config(text = self.format_timedelta(datetime.timedelta()))
        
    def set_rest_state(self):     
        self.state = 'rest'
        self.start_time = datetime.datetime.now()
        self.time_reset()
        self.winfo_toplevel().deiconify()    
        
    def set_wait_work_state(self):
        self.state = 'wait_work'
        self.start_time = datetime.datetime.now()
        self.time_reset()
        self.work.grid()
        self.winfo_toplevel().deiconify()
        
    def set_work_state(self): 
        self.state = 'work'
        self.start_time = datetime.datetime.now()
        self.time_reset()
        self.winfo_toplevel().withdraw()
        self.work.grid_remove()
        
    def start_work(self):
        self.set_work_state()
        
    def format_timedelta(self, time_delta):
        day = str(time_delta.days)
        hour = str(time_delta.seconds // 3600)
        min = str((time_delta.seconds // 60) % 60) 
        sec = str(time_delta.seconds % 60)
        return (day.rjust(2, '0') + ":" + hour.rjust(2, '0') + ":"  + min.rjust(2, '0')+ 
                ":" + sec.rjust(2, '0'))
        
    def tick(self):
        cur_time = datetime.datetime.now()
        time_delta = cur_time - self.start_time 
        
        '''show time'''
        self.time.config(text = self.format_timedelta(time_delta))
        
        if self.state == 'rest':
            if time_delta > self.config.rest_time() :
                self.set_wait_work_state()
        elif self.state == 'work':
            if time_delta > self.config.work_time() : 
                self.set_rest_state()
        
        self.time.after(1000, self.tick)

    def window_config(self):
        '''user config the Eye by a window, the config will be stored in config file too'''
        print "fuck config"
        self.config_frame = Tkinter.Frame(Tkinter.Toplevel(), width = 400, height = 400)
        self.config_frame.grid()
        
        print "fuck config"

        self.config_text = Tkinter.Text(self.config_frame)
        text = self.config.text()
        if text != None:
            self.config_text.insert('0.0', text)
        self.config_text.grid()
        
        print "fuck config"

        button_frame = Tkinter.Frame(self.config_frame)
        button_frame.grid()

        accept_button = Tkinter.Button(button_frame, text = 'Accept', command = self.config_accept)
        accept_button.grid(row = 1, column = 0)
        cancel_button = Tkinter.Button(button_frame, text = 'Cancel', command = self.config_cancel)
        cancel_button.grid(row = 1, column = 1)

    def config_accept(self):
        text = self.config_text.get('0.0', Tkinter.END)
        self.config.set_text(text)
        self.config_frame.winfo_toplevel().withdraw()

    def config_cancel(self):
        self.config_frame.winfo_toplevel().withdraw()

if __name__ == '__main__':
    app = wx.App(False)
    window = Window()
    app.MainLoop()
        

# -�~- coding: utf-8 -�~-
'''
Created on 2013.8.19

@author: nEver
'''
import datetime
import wx
import platform    
import config
import tray
import ctypes

CONFIG_FILENAME = 'config.ini'

class Window(wx.Frame):
    def __init__(self, app):
        if platform.system() == 'Windows':
            monitor_width = ctypes.windll.user32.GetSystemMetrics(0)
            monitor_height = ctypes.windll.user32.GetSystemMetrics(1)
        elif platform.system() == 'Linux':
            monitor_width = gtk.gdk.screen_width()
            monitor_height = gtk.gdk.screen_height()
        else :
            exit

        self.app = app
        self.config = config.Config(CONFIG_FILENAME)
        
        wx.Frame.__init__(self, None)
        '''removes all window manager decorations from the window'''
        '''force a widget to be a certain size, regardless of the size of its contents'''
        
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.erase_background)
        
        box = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(box)
        
        self.time = wx.StaticText(self)
        font = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.time.SetFont(font)
        self.time.SetBackgroundColour(wx.ColourDatabase().Find("WHITE"))
        time_width, time_height = self.time.GetSize()
        time_border = 20
        self.time_reset()
        box.Add(self.time, 0, wx.TOP | wx.CENTER, 20)
        
        self.work = wx.Button(self, label = "Start Work !")
        self.work.SetFont(font)
        button_width, button_height = self.work.GetSize() 
        box.Add(self.work, 0, wx. wx.TOP | wx.CENTRE , 
                monitor_height / 2 - button_height / 2 - time_height - time_border)
        self.work.Show(False)
        self.work.Bind(wx.EVT_BUTTON, self.start_work)
    
        '''must make sure that the function is called after all widget that you want to show has been defined and added'''
        self.ShowFullScreen(True)
        
        self.set_wait_work_state()
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.tick)
        self.timer.Start(milliseconds = 1000)     
        
        tray.Tray(self)
        
    def erase_background(self, event):
        dc = event.GetDC()
        dc.Clear()
        
        width, height = self.GetSize()
        image = wx.Image(self.config.image_file(), type = wx.BITMAP_TYPE_ANY)
        image_width, image_height = image.GetSize()
        '''resize image'''
        ratio = max(1.0 * width / image_width, 1.0 * height / image_height)
        image.Rescale(int(image_width * ratio), int(image_height * ratio))
        image_width, image_height = image.GetSize()
        bitmap = wx.BitmapFromImage(image)
        dc.DrawBitmap(bitmap, 0, 0)

    def time_reset(self):
        self.time.SetLabel(self.format_timedelta(datetime.timedelta()))
        
    def set_rest_state(self):     
        self.state = 'rest'
        self.start_time = datetime.datetime.now()
        self.time_reset()
        self.Show(True) 
        self.work.Show(False)
        self.Layout()
        
    def set_wait_work_state(self):
        self.state = 'wait_work'
        self.start_time = datetime.datetime.now()
        self.time_reset()
        self.work.Show(True)
        self.Show(True)
        self.Layout()
        
    def set_work_state(self): 
        self.state = 'work'
        self.start_time = datetime.datetime.now()
        self.time_reset()
        self.work.Show(False)
        self.Show(False)
        self.Layout()
        
    def start_work(self, event):
        self.set_work_state()
        
    def format_timedelta(self, time_delta):
        day = str(time_delta.days)
        hour = str(time_delta.seconds // 3600)
        min = str((time_delta.seconds // 60) % 60) 
        sec = str(time_delta.seconds % 60)
        return (day.rjust(2, '0') + ":" + hour.rjust(2, '0') + ":"  + min.rjust(2, '0')+ 
                ":" + sec.rjust(2, '0'))
        
    def tick(self, event):
        cur_time = datetime.datetime.now()
        time_delta = cur_time - self.start_time 
        
        '''show time'''
        self.time.SetLabel(self.format_timedelta(time_delta))
        
        if self.state == 'rest':
            if time_delta > self.config.rest_time() :
                self.set_wait_work_state()
        elif self.state == 'work':
            if time_delta > self.config.work_time() : 
                self.set_rest_state()

    def window_config(self):
        '''user config the Eye by a window, the config will be stored in config file too'''
        self.config_frame = wx.Frame(None, size = (300, 300), title = '设置',
                                     style = wx.DEFAULT_FRAME_STYLE & (~ wx.RESIZE_BORDER) & (~ wx.MAXIMIZE_BOX))
        self.config_frame.SetBackgroundColour(wx.ColourDatabase().Find("WHITE"))
        self.config_frame.Centre()
        self.config_frame.Show()
        frame_width, frame_height = self.config_frame.GetSize()
        
        box = wx.BoxSizer(wx.VERTICAL)
        self.config_frame.SetSizer(box)

        self.config_text = wx.TextCtrl(self.config_frame, style = wx.TE_MULTILINE)
        text = self.config.text()
        if text != None:
            self.config_text.WriteText(text)
        box.Add(self.config_text, 1, wx.EXPAND | wx.ALL, 0)
        
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(button_box, 0)

        accept_button = wx.Button(self.config_frame, label = '确定')
        accept_button_width, accept_button_height = accept_button.GetSize()
        accept_button.Bind(wx.EVT_BUTTON, self.config_accept)
        button_box.Add(accept_button, 0, wx.LEFT, frame_width / 2 - accept_button_width - 5)
        cancel_button = wx.Button(self.config_frame, label = '取消')
        cancel_button_width, cancel_button_height = accept_button.GetSize()
        cancel_button.Bind(wx.EVT_BUTTON, self.config_cancel)
        button_box.Add(cancel_button, 0, wx.RIGHT, frame_width / 2 - cancel_button_width - 5)
        self.config_frame.Layout()

    def config_accept(self, event):
        text = self.config_text.GetValue()
        self.config.set_text(text)
        self.config_frame.Close()
        del self.config_frame
        del self.config_text

    def config_cancel(self, event):
        self.config_frame.Close()
        del self.config_frame
        del self.config_text

if __name__ == '__main__':
    app = wx.App(False)
    window = Window(app)
    app.MainLoop()
        

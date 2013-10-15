# -�~- coding: utf-8 -�~-
'''
Created on 2013年9月30日

@author: never
'''
import platform
if platform.system() == 'Windows':
    import wx
elif platform.system() == 'Linux':
    import gtk
    import gobject

import ctypes
import config
import eye
import tray
import state

class View():
    def __init__(self, eye):
        self.config = eye.config
        self.state = eye.state
            
    def start_work(self, event):
        self.state.set_state(state.WORK_STATE)
        self.set_view()
    
    def start_rest(self, event):
        self.state.set_state(state.REST_STATE)
        self.set_view()
        
    def update_view(self, event): 
        is_state_changed = self.state.update_state()
        
        if is_state_changed == True:
            self.set_view()
        
        self.set_time()

class WindowsView(View):
    '''the WindwsView is implemented by wxpython'''
    
    def __init__(self, eye):
        View.__init__(self, eye)
        
        monitor_width = ctypes.windll.user32.GetSystemMetrics(0)
        monitor_height = ctypes.windll.user32.GetSystemMetrics(1)

        self.app = wx.App(False)
        
        self.frame = wx.Frame(None, size = (monitor_width, monitor_height))
        self.frame.Bind(wx.EVT_ERASE_BACKGROUND, self.erase_background)
        self.frame.ShowFullScreen(True)
        
        box = wx.BoxSizer(wx.VERTICAL)
        self.frame.SetSizer(box)
        
        self.time = wx.StaticText(self.frame)
        font = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.time.SetFont(font)
        self.time.SetBackgroundColour(wx.ColourDatabase().Find("WHITE"))
        time_width, time_height = self.time.GetSize()
        time_border = 20
        box.Add(self.time, 0, wx.TOP | wx.CENTER, 20)
        
        self.work = wx.Button(self.frame, label = "Start Work !")
        self.work.SetFont(font)
        button_width, button_height = self.work.GetSize() 
        box.Add(self.work, 0, wx. wx.TOP | wx.CENTRE , 
                monitor_height / 2 - button_height / 2 - time_height - time_border)
        self.work.Bind(wx.EVT_BUTTON, self.start_work)
        
        self.timer = wx.Timer(self.frame)
        self.Bind(wx.EVT_TIMER, self.update_view)
        self.timer.Start(milliseconds = 1000)
        
        self.tray = tray.WindowsTray(self)     
        
        self.set_view()
        self.set_time()

    def run(self):
        self.app.MainLoop()
        
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
    
    def set_time(self):
        self.time.SetLabel(self.state.time())
        self.Layout()
        
    def set_view(self):
        cur_state = self.state.state()
        if cur_state == state.WAIT_WORK_STATE:
            self.work.Show(True)
            self.Show(True)
        elif cur_state == state.WORK_STATE:
            self.work.Show(False)
            self.Show(False)
        elif cur_state == state.REST_STATE:
            self.Show(True) 
            self.work.Show(False)
        else:
            print 'Unkown Eye State'
        self.set_time()
        self.Layout()

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

class LinuxView(View):
    '''the WindwsView is implemented by wxpython'''
    
    def __init__(self, eye):
        View.__init__(self, eye)
        
        monitor_width = gtk.gdk.screen_width()
        monitor_height = gtk.gdk.screen_height()

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.fullscreen()
        self.window.connect("destroy", gtk.main_quit)
        self.window.show()

        self.fixed = gtk.Fixed()
        self.window.add(self.fixed)
        self.fixed.show()

        self.image = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file(self.config.image_file())
        image_width = pixbuf.get_width()
        image_height = pixbuf.get_height()
        ratio = max(1.0 * monitor_width / image_width, 
                1.0 * monitor_height / image_height)
        pixbuf = pixbuf.scale_simple(int(image_width * ratio), 
                int(image_height * ratio), gtk.gdk.INTERP_BILINEAR)
        self.image.set_from_pixbuf(pixbuf)
        self.fixed.put(self.image, 0, 0)
        self.image.show()

        self.time = gtk.Label()
        width, height = self.time.size_request()
        self.fixed.put(self.time, monitor_width / 2 - width / 2, 10)
        self.time.show()
        
        self.work = gtk.Button(label="Start Work !")
        self.work.connect('clicked', self.start_work)
        width, height = self.work.size_request()
        self.fixed.put(self.work, monitor_width / 2 - 
                width / 2, monitor_height / 2 - height / 2)
        self.work.show()
       
        self.set_time()
        gobject.timeout_add(1000, self.set_time)

    def run(self):
        gtk.main()
    
    def set_time(self):
        self.time.set_markup(
                '<span background="white" size="38000">' + 
                self.state.time() + '</span>')
   
    def set_view(self):
        cur_state = self.state.state()
        if cur_state == state.WAIT_WORK_STATE:
            self.work.show()
            self.window.show_all()
        elif cur_state == state.WORK_STATE:
            self.work.hide()
            self.window.hide_all()
        elif cur_state == state.REST_STATE:
            self.window.show_all()
            self.work.hide()
        else:
            print 'Unkown Eye State'
        self.set_time()

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

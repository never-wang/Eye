#!/usr/bin/env python
# -�~- coding: utf-8 -�~-
#########################################################################
# Author: Wang Wencan
# Created Time: Wed 25 Sep 2013 09:26:22 AM CST # File Name: tray.py
# Description: 
#########################################################################
import platform
if platform.system() == 'Windows':
    import wx
elif platform.system() == 'Linux':
    import gtk
    import appindicator
import os

class Tray():
    config_window_width = 300
    config_window_height = 300
    def __init__(self, view):
        self.view = view
        self.itemlist = [(1, "设置", self.menu_config),
                         (2, '休息', self.menu_rest),
                         (3, '退出', self.menu_quit)]
    
    def menu_rest(self, event):
        self.view.start_rest(event)

class WindowsTray(Tray):
    def __init__(self, view):
        Tray.__init__(self, view)

        self.tray = wx.TaskBarIcon()
        self.tray.SetIcon(wx.Icon(os.path.os.path.join(os.path.dirname(__file__), "eye.gif"),  wx.BITMAP_TYPE_GIF)) 
        self.tray.Bind(wx.EVT_TASKBAR_CLICK, self.popup_menu)
    
    def popup_menu(self, event):
        menu = self.make_menu()
        self.tray.PopupMenu(menu)
            
    def make_menu(self):
        menu = wx.Menu()
        for id, text, callback in self.itemlist:
            item = menu.Append(id, text)
            menu.Bind(wx.EVT_MENU, callback, id = id)
        return menu
    
    def menu_config(self, event):
        '''user config the Eye by a window, the config will be stored in config file too'''
        self.config_frame = wx.Frame(None, 
                size = (self.config_window_width, self.config_window_height), title = '设置',
                style = wx.DEFAULT_FRAME_STYLE & (~ wx.RESIZE_BORDER) & (~ wx.MAXIMIZE_BOX))
        self.config_frame.SetBackgroundColour(wx.ColourDatabase().Find("WHITE"))
        self.config_frame.Centre()
        self.config_frame.Show()
        frame_width, frame_height = self.config_frame.GetSize()
        
        box = wx.BoxSizer(wx.VERTICAL)
        self.config_frame.SetSizer(box)

        self.config_text = wx.TextCtrl(self.config_frame, style = wx.TE_MULTILINE)
        text = self.view.config.text()
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

    def menu_quit(self, event):
        self.view.Close()
        self.tray.Destroy()
    
    def config_accept(self, event):
        text = self.config_text.GetValue()
        self.view.config.set_text(text)
        self.config_frame.Close()
        del self.config_frame
        del self.config_text

    def config_cancel(self, event):
        self.config_frame.Close()
        del self.config_frame
        del self.config_text

class LinuxTray(Tray):
    def __init__(self, view):
        Tray.__init__(self, view)

        self.tray = appindicator.Indicator('Eye', 'indicator-messages', appindicator.CATEGORY_APPLICATION_STATUS)
        self.tray.set_status(appindicator.STATUS_ACTIVE)
        self.tray.set_icon(os.path.join(os.path.abspath(os.path.dirname(__file__)), "eye.gif"))
        self.tray.set_attention_icon('indicator-messages-new')
        self.tray.set_menu(self.make_menu())
    
    def make_menu(self):
        menu = gtk.Menu()
        for id, text, callback in self.itemlist:
            item = gtk.MenuItem(text)
            item.connect('activate', callback)
            item.show()
            menu.append(item)
        menu.show()
        return menu
    
    def menu_config(self, event):
        '''user config the Eye by a window, the config will be stored in config file too'''
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_default
        self.config_frame = wx.Frame(None, size = (300, 300), title = '设置',
                                     style = wx.DEFAULT_FRAME_STYLE & (~ wx.RESIZE_BORDER) & (~ wx.MAXIMIZE_BOX))
        self.config_frame.SetBackgroundColour(wx.ColourDatabase().Find("WHITE"))
        self.config_frame.Centre()
        self.config_frame.Show()
        frame_width, frame_height = self.config_frame.GetSize()
        
        box = wx.BoxSizer(wx.VERTICAL)
        self.config_frame.SetSizer(box)

        self.config_text = wx.TextCtrl(self.config_frame, style = wx.TE_MULTILINE)
        text = self.view.config.text()
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

    def menu_quit(self, event):
        gtk.main_quit()
        

if __name__ == "__main__":
    Tray("test")

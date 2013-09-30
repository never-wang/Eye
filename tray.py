#!/usr/bin/env python
# -�~- coding: utf-8 -�~-
#########################################################################
# Author: Wang Wencan
# Created Time: Wed 25 Sep 2013 09:26:22 AM CST
# File Name: tray.py
# Description: 
#########################################################################
try:
    import appindicator
except ImportError:
    appindicator = None
import wx
import os

class Tray():
    def __init__(self, eye):
        self.eye = eye
        if appindicator == None:
            self.tray = wx.TaskBarIcon()
            self.tray.SetIcon(wx.Icon(os.path.os.path.join(os.path.dirname(__file__), "eye.gif"),  wx.BITMAP_TYPE_GIF)) 
            #self.tray.connect('popup-menu', self.popup_menu)
            self.tray.Bind(wx.EVT_TASKBAR_CLICK, self.popup_menu)
        else:
            self.tray = appindicator.Indicator('GoAgent', 'indicator-messages', appindicator.CATEGORY_APPLICATION_STATUS)
            self.tray.set_status(appindicator.STATUS_ACTIVE)
            self.tray.set_attention_icon('indicator-messages-new')
            self.tray.set_icon(os.path.join(os.path.dirname(__file__), "eye.gif"))
            self.tray.set_menu(self.make_menu())
            self.iteration()
    
    def iteration(self):
        gtk.main_iteration(block = False)
        self.eye.time.after(1, self.iteration)
    
    def popup_menu(self, event):
        menu = self.make_menu()
        self.tray.PopupMenu(menu)
            
    def make_menu(self):
        itemlist = [(1, "设置", self.menu_config),
                    (2, '休息', self.menu_rest),
                    (3, '退出', self.menu_quit)]
        if appindicator == None:
            menu = wx.Menu()
            for id, text, callback in itemlist:
                item = menu.Append(id, text)
                menu.Bind(wx.EVT_MENU, callback, id = id)
        else:
            menu = gtk.Menu()
            for id, text, callback in itemlist:
                item = gtk.MenuItem(text)
                item.connect('activate', callback)
                item.show()
                menu.append(item)
            menu.show()
        return menu
    
    def menu_config(self, menuitem):
        self.eye.window_config()       

    def menu_rest(self, menuitem):
        self.eye.set_rest_state()

    def menu_quit(self, menuitem):
        self.eye.Close()
        if appindicator == None:
            self.tray.Destroy()

if __name__ == "__main__":
    Tray("test")

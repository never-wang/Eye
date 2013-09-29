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
import gtk

class Tray():
    def __init__(self, eye):
        self.eye = eye
        if appindicator == None:
            self.app = wx.App()
            self.app.MainLoop()
        else:
            self.tray = appindicator.Indicator('GoAgent', 'indicator-messages', appindicator.CATEGORY_APPLICATION_STATUS)
            self.tray.set_status(appindicator.STATUS_ACTIVE)
            self.tray.set_attention_icon('indicator-messages-new')
            self.tray.set_icon(os.path.join(os.path.abspath(os.path.dirname(__file__)), "eye.gif"))
            self.tray.set_menu(self.make_menu())

        self.iteration()
    
    def iteration(self):
        if appindicator == None:
            pass
        else:
            gtk.main_iteration(block = False)
        
        self.eye.time.after(10, self.iteration)
            
    def make_menu(self):
        menu = gtk.Menu()
        itemlist = [("设置", self.menu_config),
                ('休息', self.menu_rest),
                ('退出', self.menu_quit)]
        for text, callback in itemlist:
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
        self.eye.quit()

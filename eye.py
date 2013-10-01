# -�~- coding: utf-8 -�~-
'''
Created on 2013.8.19

@author: nEver
'''
import datetime
import wx
import platform    
from config import *
import tray
import ctypes
import view

WORK_STATE = 'WORK'
REST_STATE = "REST"
WAIT_WORK_STATE = 'WAIT_WORK'
CONFIG_FILENAME = 'config.ini'

class Eye():
    def __init__(self):
        self.state = WAIT_WORK_STATE
        self.start_time = datetime.datetime.now()
        
        self.config = Config(CONFIG_FILENAME)
        
        if platform.system() == 'Windows':
            self.view = view.WindowsView(self)
        elif platform.system() == 'Linux':
            pass
        else :
            exit
        
        self.view.run()
        
    def update_state(self):
        cur_time = datetime.datetime.now()
        time_delta = cur_time - self.start_time 
        print time_delta, self.state, self.config.work_time()
        
        if self.state == REST_STATE:
            if time_delta > self.config.rest_time() :
                self.set_state(WAIT_WORK_STATE)
                return True
        elif self.state == WORK_STATE:
            if time_delta > self.config.work_time() : 
                self.set_state(REST_STATE)
                return True
        return False
        
    def set_state(self, state):     
        self.state = state
        self.start_time = datetime.datetime.now()
    
    def time(self):
        time_delta = datetime.datetime.now() - self.start_time
        day = str(time_delta.days)
        hour = str(time_delta.seconds // 3600)
        min = str((time_delta.seconds // 60) % 60) 
        sec = str(time_delta.seconds % 60)
        return (day.rjust(2, '0') + ":" + hour.rjust(2, '0') + ":"  + min.rjust(2, '0')+ 
                ":" + sec.rjust(2, '0'))

if __name__ == '__main__':
    eye = Eye()
        

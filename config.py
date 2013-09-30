# -�~- coding: utf-8 -�~-

import ConfigParser
import datetime
import os

class Config:
    def __init__(self, config_filename):
        self.config_filename = config_filename
        defaults = {'rest_time' : '10', 'work_time' : '50', 
                'image_file' : 'rei.jpg', 'time_unit' : 'min'}
        self.config = ConfigParser.ConfigParser(defaults)
        self.config.add_section('General') 
        try:
            self.config.read(self.config_filename)
        except:
            pass
        
    def rest_time(self):
        rest_time = self.config.getint('General', 'rest_time')
        if self.time_unit() == 'hour':
            return datetime.timedelta(hours = rest_time)
        elif self.time_unit() == 'min':    
            return datetime.timedelta(minutes = rest_time)
        else: 
            '''sec or other'''
            return datetime.timedelta(seconds = rest_time)

    def work_time(self):
        work_time = self.config.getint('General', 'work_time')
        if self.time_unit() == 'hour':
            return datetime.timedelta(hours = work_time)
        elif self.time_unit() == 'min':    
            return datetime.timedelta(minutes = work_time)
        else: 
            '''sec or other'''
            return datetime.timedelta(seconds = work_time)
    
    def image_file(self):
        image_file = self.config.get('General', 'image_file')
        if os.path.isabs(image_file):
            return image_file
        else:
            prefix = os.path.dirname(__file__)
            return os.path.join(prefix, image_file)
    
    def time_unit(self):
        return self.config.get('General', 'time_unit')

    def text(self):
        try :
            file = open(self.config_filename, 'r')
            text = file.read()
            file.close()
            return text
        except :
            return None
        
    def set_text(self, text):
        file = open(self.config_filename, 'w')
        file.write(text)
        file.close()
        try :
            self.config.read(self.config_filename)
        except :
            pass

if __name__ == "__main__":
    config = Config("eye.ini")
    print config.get_rest_time()
    #print config.get_work_time()
    print config.get_image_file()
    config.set_from_window()
    gtk.main()
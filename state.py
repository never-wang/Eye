# -�~- coding: utf-8 -�~-
'''
Created on 2013年10月1日

@author: never
'''
import thread
import datetime
import SocketServer
import threading

SERVER_ROLE = 'SERVER'
CLIENT_ROLE = 'CLIENT'

WORK_STATE = 'WORK'
REST_STATE = "REST"
WAIT_WORK_STATE = 'WAIT_WORK'

TIME_IDENT = 'TIME'
STATE_IDENT = 'STATE'

class State():
    def __init__(self, eye):
        self.config = eye.config
        self.cur_state = WAIT_WORK_STATE
        self.start_time = datetime.datetime.now()
            
    def update_state(self):
        cur_time = datetime.datetime.now()
        time_delta = cur_time - self.start_time 
        print time_delta, self.cur_state
        
        if self.cur_state == REST_STATE:
            if time_delta > self.config.rest_time() :
                self.set_state(WAIT_WORK_STATE)
                self.view.set_view()
        elif self.cur_state == WORK_STATE:
            if time_delta > self.config.work_time() : 
                self.set_state(REST_STATE)
                self.view.set_view()
        self.view.set_time()

        self.condition.notify()
        
        self.timer = threading.Timer(1, self.update_state)
        self.timer.start()

    def quit(self):
        if self.timer:
            self.timer.cancel()
        
class StateServer(SocketServer.TCPServer):
    def __init(self, addr, handler, state):
        SocketServer.TCPServer.__init__(self, addr, handler)
        self.state = state
        
class ServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        state = self.server.state.state()
        time = self.server.state.time()
        condition = self.server.state.condition
       
        whiel True:
            coniditon.wait()
            self.request.send(state)
            self.request.send(time)
        
class ServerState(State):
    def __init__(self, eye):
        State.__init__(self, eye)
        self.conditon = threading.Condition()
        thread.start_new_thread(self.start_server, ())
       # self.start_server()
        
    def start_server(self):
        server = StateServer(("", self.config.port()), ServerHandler, self)
        server.serve_forever()
    
    def state(self):
        return self.cur_state
        
    def set_state(self, state):     
        self.cur_state = state
        self.start_time = datetime.datetime.now()
    
    def time(self):
        time_delta = datetime.datetime.now() - self.start_time
        day = str(time_delta.days)
        hour = str(time_delta.seconds // 3600)
        min = str((time_delta.seconds // 60) % 60) 
        sec = str(time_delta.seconds % 60)
        return (day.rjust(2, '0') + ":" + hour.rjust(2, '0') + ":"  + min.rjust(2, '0')+ 
                ":" + sec.rjust(2, '0'))

class ClientState(State):
    def __init__(self, eye):
        State.__init__(self, eye)
        socket.create_connection(address = config.server_address(), timeout = config.timeout())
        

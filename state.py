# -�~- coding: utf-8 -�~-
'''
Created on 2013年10月1日

@author: never
'''
import thread
import datetime
import SocketServer

SERVER_ROLE = 'SERVER'
CLIENT_ROLE = 'CLIENT'

WORK_STATE = 'WORK'
REST_STATE = "REST"
WAIT_WORK_STATE = 'WAIT_WORK'

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
                return True
        elif self.cur_state == WORK_STATE:
            if time_delta > self.config.work_time() : 
                self.set_state(REST_STATE)
                return True
        return False
        
class StateServer(SocketServer.TCPServer):
    def __init(self, addr, handler, state):
        SocketServer.TCPServer.__init__(self, addr, handler)
        self.state = state
        
class ServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        state = self.server.state.state()
        time = self.server.state.time()
        
        self.request.sendall(pickle.dumps((pick, time)))

class ServerState(State):
    def __init__(self, eye):
        State.__init__(self, eye)
        thread.start_new_thread(self.start_server, ())
        
    def start_server(self):
        server = StateServer(("localhost", self.config.port()), ServerHandler, self)
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
        
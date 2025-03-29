from .agents import *
from enum import Enum

class Director():

    class States(str, Enum):
        WAIT_FOR_USER = 'wait_for_user'
        REQ_GATHERING = 'req_gathering'
        FUNC_SIGNATURES = 'func_signatures'
        CODING = 'coding'
        ACCEPT = 'accept'

    class Events(str, Enum):
        READY = 'ready'
        REQ_RECEIVED = 'req_received'
    
    def __init__(self):
        self.req_gatherer =  RequirementsGatherer()
        self.func_signatures = FunctionSignatureArchitect()
        self.coder = Coder()
        self.current_state = self.States.WAIT_FOR_USER
        self.current_event = self.Events.READY
        self.current_data = None
        self.loop()
    

    def loop(self):
        while(self.current_state != self.States.ACCEPT):
            
            self.handleState(self.current_state, self.current_event, self.current_data)

    
    def handleState(self, state, event, data):
        match state:
            case self.States.WAIT_FOR_USER:
                self.handle_wait_for_user(event, data)
            case self.States.REQ_GATHERING:
                self.handle_req_gathering(event, data)
            case self.States.FUNC_SIGNATURES:
                self.handle_func_signatures(event, data)
            case self.States.CODING:
                self.handle_coding(event, data)
            case self.States.ACCEPT:
                self.handle_accept(event, data)
            case _:
                raise Exception('No state in tree')
            
    def handle_wait_for_user(self, event, data):
        match event:
            case self.Events.READY:
                prompt = self.get_inital_prompt()
                result = self.req_gatherer.send_message(prompt)
                # self.                
            
    def handle_req_gathering(self, event, data):
        pass
            
    def handle_func_signatures(self, event, data):
        pass
            
    def handle_coding(self, event, data):
        pass
            
    def handle_accept(self, event, data):
        pass

    def get_initial_prompt():
        # return input('what do you want to build?)
        return 'do your part to build a project that takes a user input from the console and generates that number of the fibonacci sequence back out to the console in python 3.12. '
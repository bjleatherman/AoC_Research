from agents import *
from enum import Enum

class Director():

    class States(str, Enum):
        WAIT_FOR_USER = 'wait_for_user'
        REQ_GATHERING = 'req_gathering'
        FUNC_SIGNATURES = 'func_signatures'
        CODE = 'code'
        REQUEST_INFO = 'request_info'
        ACCEPT_PROGRAM = 'accept_program'

    class Events(str, Enum):
        READY = 'ready'
        INFO_COLLECTED = 'info_collected'
        ASK_USER_QUESTION = 'ask_user_question'
        RETURN_SIGNATURES_ANSWER = 'return_signatures_answer'
        RETURN_CODE_ANSWER = 'return_code_answer'
        SIGNATURES_COLLECTED = 'signatures_collected'
        ALL_CODE_WRITTEN = 'all_code_written'

    program_requirements = None
    
    def __init__(self, log_file):
        self.req_gatherer =  RequirementsGatherer(log_file)
        self.func_signatures = FunctionSignatureArchitect(log_file)
        self.coder = Coder(log_file)
        self.current_state = self.States.WAIT_FOR_USER
        self.current_event = self.Events.READY
        self.current_data = None

    def start(self):
        self.loop()
    

    def loop(self):
        while(self.current_state != self.States.ACCEPT_PROGRAM):
            
            self.handleState(self.current_state, self.current_event, self.current_data)

    
    def handleState(self, state, event, data):
        match state:
            case self.States.WAIT_FOR_USER:
                self.handle_wait_for_user(event, data)
            case self.States.REQ_GATHERING:
                self.handle_req_gathering(event, data)
            case self.States.FUNC_SIGNATURES:
                self.handle_func_signatures(event, data)
            case self.States.CODE:
                self.handle_code(event, data)
            case self.States.ACCEPT_PROGRAM:
                self.handle_accept(event, data)
            case _:
                raise Exception('No state in tree')
            
    def handle_wait_for_user(self, event, data):
        match event:
            case self.Events.READY:
                prompt = self.get_initial_prompt()
                result = self.req_gatherer.handle_send_message(prompt)
                if result == self.Events.INFO_COLLECTED.value:
                    self.current_state = self.States.REQ_GATHERING
                    self.current_event = self.Events.READY
                else:
                    raise Exception('Requirements Gatherer returned an unhandled event')
            case _:
                raise Exception('Unhandled state transition')
            
    def handle_req_gathering(self, event, data):
        match event:
            case self.Events.READY:
                self.current_state = self.States.FUNC_SIGNATURES
                self.current_event = self.Events.READY
                self.program_requirements = self.req_gatherer.get_requirements_package()
            case _:
                raise Exception('Unhandled state transition')
            
    def handle_func_signatures(self, event, data):
        match event:
            case self.Events.READY:
                result = self.func_signatures.send_message()
            case _:
                raise Exception('Unhandled state transition')
            
    def handle_code(self, event, data):
        pass
            
    def handle_accept(self, event, data):
        pass

    def get_initial_prompt(self):
        # return input('what do you want to build?)
        return 'do your part to build a project that takes a user input from the console and generates that number of the fibonacci sequence back out to the console in python 3.12. '
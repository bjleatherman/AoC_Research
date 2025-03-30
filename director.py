from agents import *
from enum import Enum

class Director():

    class States(str, Enum):
        WAIT_FOR_USER = 'wait_for_user'
        REQ_GATHERING = 'req_gathering'
        FUNC_SIGNATURES = 'agent_func_signatures'
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

    class Results(str, Enum):
        ACCEPT = 'accept'
        REQUEST_MORE_INFO = 'request_more_info'
        INFO_COLLECTED = 'info_collected'

    class Data(str, Enum):
        FUNC = 'func'
        CODE = 'code'
    
    def __init__(self, log_file, code_file):
        self.agent_req_gatherer =  RequirementsGatherer(log_file)
        self.agent_func_signatures = FunctionSignatureArchitect(log_file)
        self.agent_coder = Coder(log_file)
        self.current_state = self.States.WAIT_FOR_USER
        self.current_event = self.Events.READY
        self.current_data = None
        self.program_requirements = None
        self.raw_func_signatures = None
        self.empty_functions = []
        self.question_for_user = None
        self.last_user_response = None
        self.initial_function_count = 0
        self.code_file = code_file

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

            case self.States.REQUEST_INFO:
                self.handle_user_question(event, data)

            case self.States.ACCEPT_PROGRAM:
                self.handle_accept(event, data)

            case _:
                raise Exception('No state in tree')
            
    def handle_wait_for_user(self, event, data):
        match event:
            case self.Events.READY:
                prompt = self.get_initial_prompt()
                result = self.agent_req_gatherer.handle_send_message(prompt)
                if result == self.Results.INFO_COLLECTED.value:
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
                self.program_requirements = self.agent_req_gatherer.get_requirements_package()
            case _:
                raise Exception('Unhandled state transition')
            
    def handle_func_signatures(self, event, data):

        result = None

        match event:
            case self.Events.READY:
                result = self.agent_func_signatures.send_message(
                    self.program_requirements
                )
            case self.Events.RETURN_SIGNATURES_ANSWER:
                result = self.agent_func_signatures.send_message(
                    self.last_user_response
                )
            case _:
                raise Exception('Unhandled state transition')
                
        if result == self.Results.ACCEPT.value:
            self.raw_func_signatures = self.agent_func_signatures.last_accepted_response
            self.split_func_signatures()
            self.current_state = self.States.CODE
            self.current_event = self.Events.READY
        elif result == self.Results.REQUEST_MORE_INFO:
            self.current_state = self.States.REQUEST_INFO
            self.current_event = self.Events.ASK_USER_QUESTION
            self.current_data = self.Data.FUNC
            self.question_for_user = self.agent_func_signatures.last_request_response
            
    def handle_code(self, event, data):
        
        result = None

        print(f'Functions Remaining: {len(self.empty_functions)} of {self.initial_function_count}')

        if len(self.empty_functions) == 0:
            self.current_state = self.States.ACCEPT_PROGRAM
            return

        match event:
            case self.Events.READY:
                result = self.agent_coder.send_message(
                    f'program requirements:\n' +
                    self.program_requirements + '\n' +
                    str(self.empty_functions.pop())
                    )
            case self.Events.RETURN_CODE_ANSWER:
                result = self.agent_coder.send_message(
                    f'program requirements:\n' +
                    self.program_requirements + '\n' +
                    'answer from user:\n' +
                    self.last_user_response
                )

        if result == self.Results.ACCEPT.value:
            self.append_function_to_doc(self.agent_coder.last_accepted_response)
            self.current_state = self.States.CODE
            self.current_event = self.Events.READY
        elif result == self.Results.REQUEST_MORE_INFO:
            self.current_state = self.States.REQUEST_INFO
            self.current_event = self.Events.ASK_USER_QUESTION
            self.current_data = self.Data.CODE
            self.question_for_user = self.agent_coder.last_request_response

    def handle_user_question(self, event, data):
        match event:
            case self.Events.ASK_USER_QUESTION:
                self.get_user_answer()

                if data == self.Data.FUNC:
                    self.current_state = self.States.FUNC_SIGNATURES
                    self.current_event = self.Events.RETURN_SIGNATURES_ANSWER
                elif data == self.Data.CODE:
                    self.current_state = self.States.CODE
                    self.current_event = self.Events.RETURN_CODE_ANSWER
            case _:
                raise Exception('Unhandled state transition')
                            
    def handle_accept(self, event, data):
        print('Your Program is Finished')

    def get_initial_prompt(self):
        return input('what do you want to build?')
        # return 'do your part to build a project that takes a user input from the console and generates that number of the fibonacci sequence back out to the console in python 3.12. '
    
    def split_func_signatures(self):
        cleaned_text = self.raw_func_signatures.replace('\r', '').replace('\n', '').strip()
        delimiter = self.agent_func_signatures.delimiter
        self.empty_functions = cleaned_text.split(delimiter)

        self.initial_function_count = len(self.empty_functions)

    def handle_user_question(self):
        self.last_user_response = input(self.question_for_user)

    def append_function_to_doc(self, func_string):
        with open(self.code_file, 'a') as f:
            f.write(f'{func_string}\n')
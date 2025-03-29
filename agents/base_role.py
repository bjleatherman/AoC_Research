from enum import Enum
from pydantic import BaseModel, Field
from message_builder import MessageBuilder

class Role:
    description = 'You have a generic role'
    delimiter = ";"

    class ActionType(str, Enum):
        ACCEPT = 'accept'
        REJECT = 'reject'
        REQUEST_MORE_INFO = 'request_more_info'

    def __init__(self, log_file):
        self.current_chat_history = []
        self.archived_chat_history = []
        self.log_file = log_file

    @staticmethod
    def get_fields(delimiter):
        return [ 
            {   
                'name': 'response',
                'type': str, 
                'description': '\n'.join([
                    'A string of python code or a clarifying question.', 
                    'This field corresponds to the action field.', 
                    'If there is any ambiguity, please ask a followup question for clarification.', 
                    'Do not just assume that you know what to write. Clarify with the user what they are asking you to write.',
                    'Do NOT Add any example usage, send code as though it\'s going to be dropped into the codebase.',
                ])
            }
        ]

    def build_response_format(self):
        annotations = {}
        class_attrs = {}

        # Use instance's delimiter, allowing overrides at subclass level
        fields = self.get_fields(self.delimiter)

        for field in fields:
            annotations[field['name']] = field['type']
            class_attrs[field['name']] = Field(description=field['description'])

        annotations['action'] = self.ActionType
        class_attrs['action'] = Field(description='The possible actions that can be taken.')

        response_format = type(
            f"{self.__class__.__name__}ResponseFormat",
            (BaseModel,),
            {
                '__annotations__': annotations,
                **class_attrs
            }
        )
        return response_format

    def handle_send_message(self, query):
        response = self.send_message(query)
        
        return response.action.value
        
    def send_message(self, query: str):
        response_format = self.build_response_format()
        response = MessageBuilder.build_send_message(
            query=query,
            system_description=self.description,
            response_format=response_format, 
            chat_history=self.current_chat_history
        )

        self.log_message(role='user', user_content=query)
        self.log_message(role='system', response=response.response, action=response.action.value)

        return response

    def log_message(self, role, user_content='', response='', action=''):
        if user_content:
            content = user_content
        elif response and action:
            content = f'[Response]: {response}, [Action Taken]: {action}'
        else:
            content = ''

        message = {'role': role, 'content': content}
        self.current_chat_history.append(message)

        with open(self.log_file, 'a') as f:
            f.write(f'{message}\n')

    def print_current_chat_history(self):
        for message in self.current_chat_history:
            content = message['content'].replace(self.delimiter, f"{self.delimiter}\n")
            print(f"[{message['role']}]: {content}")

    def get_current_chat_history(self):
        return self.current_chat_history

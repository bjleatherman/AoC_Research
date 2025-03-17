from enum import Enum
from pydantic import BaseModel, Field
from message_builder import MessageBuilder
from typing import Type, Dict, Any

class Role:
    
    description = 'You have a generic role'
    delimiter = ";"
    archived_chat_histories = []
    current_chat_history = []

    @classmethod
    def get_fields(cls):
        return [ 
            {   
                'name':'response',
                'type': str, 
                'description':'\n'.join([
                    'A string of python code or a clarifying question.', 
                    'This field corresponds to the action field.', 
                    'If there is any ambiguity, please ask a followup question for clarification.', 
                    'Do not just assume that you know what to write. Clarify with the user what they are asking you to write.',
                    'Do NOT Add any example usage, send code as though its going to be dropped into the codebase.',
                ])
            }
        ]

    class ActionType(str, Enum):
        ACCEPT = 'accept'
        REJECT = 'reject'
        REQUEST_MORE_INFO = 'request_more_info'

    @classmethod
    def build_response_format(cls):
        """
        Dynamically builds a ResponseFormat class using the fields defined in `fields`.
        """
        annotations = {}  # Pydantic requires explicit type annotations
        class_attrs = {}

        fields = cls.get_fields()

        # Convert `fields` into class attributes
        for field in fields:
            field_name = field['name']
            field_type = field['type']
            field_description = field['description']

            annotations[field_name] = field_type
            class_attrs[field_name] = Field(description=field_description)

        # Add the `action` field, always using the class's `ActionType`
        annotations['action'] = cls.ActionType
        class_attrs['action'] = Field(description='The possible actions that can be taken.')

        # Create the dynamic Pydantic model
        response_format = type(
            f"{cls.__name__}ResponseFormat",
            (BaseModel,),
            {
                '__annotations__': annotations,  # Explicitly set type annotations
                **class_attrs  # Assign fields separately
            }
        )

        return response_format

    @classmethod
    def send_message(cls, query: str):
        response_format = cls.build_response_format()

        response = MessageBuilder.build_send_message(
            query=query,
            system_description=cls.description,
            response_format=response_format, 
            chat_history=cls.current_chat_history
        )

        cls.log_message(role='user', user_content=query)
        cls.log_message(role='system', response=response.response, action=response.action.value)

        return response

    @classmethod
    def log_message(cls, role, user_content='', response='', action=''):
        if user_content:
            content = user_content
        elif response and action:
            content = f'[Response]: {response}, [Action Taken]: {action}'
        else:
            content = ''

        message = {'role': role, 'content': content}
        cls.current_chat_history.append(message)

    @classmethod
    def print_current_chat_history(cls):
        for message in cls.current_chat_history:
            content = message['content'].replace(cls.delimiter, f"{cls.delimiter}\n")
            print(f"[{message['role']}]: {content}")

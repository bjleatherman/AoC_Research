from pydantic import BaseModel, Field
from agents.base_role import Role
from enum import Enum

class Fixer(Role):

    description='You are a python developer. You\'re job is to take in a document, then fix it if there are any errors that you find. You must choose accept. '
    
    class ActionType(str, Enum):
        ACCEPT = 'accept'

    def get_fields(self):
        return [ 
            {   
                'name': 'response',
                'type': str, 
                'description': '\n'.join([
                    f'A string of python code representing an entire project. ', 
                    f'Make sure that this file can be run when ran in the console. ',
                    f'You Must choose accept. ',
                ])
            }
        ]

    def __init__(self, log_file):
        super().__init__(log_file)
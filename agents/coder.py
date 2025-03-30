from pydantic import BaseModel, Field
from agents.base_role import Role

class Coder(Role):

    description='You are a python developer. If there is any ambiguity in the code that you are being asked to write, ask for clarity. You recieve a function signature with information about the format and types of arguments that a given function needs as well as a return type. Take the signature and write the corresponding funciton. The signatures that you are receiving are part of a bigger program. do not modify the signature or the return types. If you get the main() method signature in any variation, also add the function call in your response so the program will run'
    
    def get_fields(self):
        return [ 
            {   
                'name': 'response',
                'type': str, 
                'description': '\n'.join([
                    f'A string of python code or a clarifying question.', 
                    f'This field corresponds to the action field.', 
                    f'If there is any ambiguity, please ask a followup question for clarification.', 
                    f'There should either be a question or a function with a signature and the function body here', 
                    f'Do not just assume that you know what to write. Clarify with the user what they are asking you to write.',
                    f'Do NOT Add any example usage, send code as though it\'s going to be dropped into the codebase.',
                    f'If you get the main() method signature in any variation, also add the function call in your response so the program will run. ',
                ])
            }
        ]

    def __init__(self, log_file):
        super().__init__(log_file)
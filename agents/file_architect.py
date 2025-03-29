from agents.base_role import Role
from typing import Type, Dict, Any
from enum import Enum

class FileArchitect(Role):

    description='You are the file scaffolding architect for a python project. Your job is to come up with the basic file architecture for a project, not to write any code. You will be asked to design some file scaffolding. If you dont have enough information to proceed ASK FOR MORE INFORMATION' 

    def __init__(self, log_file):
        super().__init__(log_file)

    @classmethod
    def get_fields(cls):
        return [
        {
            'name':'response',
            'type':str,
            'description':'\n'.join([
                f'This field contains the response to the prompt, either function signatures, or a clarifying question.',
                f'A {cls.delimiter} separated string of folder names that should go into the project root folder. There are no sub-folders. ', 
                f'This field corresponds to the create folders action. ', 
                f'Please ask follow up questions if you are unsure of what to do. The less ambiguity the better. Do not add anything other than comma separated folder names here. ',
                f'If there is not enough information to proceed, ask for more information here instead of writing files names. '
            ])
        },
    ]
from agents.base_role import Role
from typing import Type, Dict, Any
from enum import Enum

class FunctionSignatureArchitect(Role):

    description='You are the function signature architect for a python project. Your job is to come up with the basic function signatures for a project, not to write any code. You will be asked to write some helpful function signatures that someone else will complete. Your functions should work together in a clear way If you dont have enough information to proceed ASK FOR MORE INFORMATION'

    @classmethod
    def get_fields(cls):
        return [
        {
            'name':'response',
            'type':str,
            'description':'\n'.join([
                f'This field contains the response to the prompt, either function signatures, or a clarifying question.',
                f'A field that contains a {cls.delimiter} separated list of python function signatures. ',
                f'The signature should contain types for parameters and information about the expected return type. ', 
                f'Each {cls.delimiter} separated signature should be able to be pasted into a python document and run when other information is added'
                f'This field corresponds to the create signatures action. ', 
                f'Please ask follow up questions if you are unsure of what to do. The less ambiguity the better. Do not add anything other than semi-colon separated folder names here. ',
                f'If you need more information about the project, do not add function signatures here, only ask your question',
            ])
        }
    ]
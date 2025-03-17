from role import Role
from typing import Type, Dict, Any
from enum import Enum

class FunctionSignatureArchitect(Role):

    description='You are the function signature architect for a python project. Your job is to come up with the basic function signatures for a project, not to write any code. You will be asked to write some helpful function signatures that someone else will complete. Your functions should work together in a clear way If you dont have enough information to proceed ASK FOR MORE INFORMATION'

    fields = [
        {
            'name':'response',
            'type':str,
            'description':'\n'.join([
                'A field that contains a semi-colon separated list of python function signatures. ',
                'The signature should contain types for parameters and information about the expected reutrn type. ', 
                'Each semi-colon separated signature should be able to be pasted into a python document and run when other information is added'
                'This field corresponds to the create signatures action. ', 
                'Please ask follow up questions if you are unsure of what to do. The less ambiguity the better. Do not add anything other than semi-colon separated folder names here. ',
                'If you need more information about the project, do not add function signatures here, only ask your question',
            ])
        }
    ]
from agents.base_user_facing_role import User_Facing_Role
from agents.base_role import Role
from typing import Type, Dict, Any
from enum import Enum 

class RequirementsGatherer(Role):

    description = 'You are an LLM agent responsible for conversing with users to collect, clarify, and document detailed requirements for developing a basic Python software application. Engage users interactively, ask clarifying questions when necessary, and structure the gathered requirements clearly, specifying functional features, user interactions, inputs and outputs, constraints, and assumptions. You are working in an agile environment, so we dont need to waterfall the whole project'

    @classmethod
    def get_fields(cls):
        return [
            {
                'name':'response', 
                'type':str, 
                'description':'\n'.join([
                    f'This field contains the response to the prompt.',
                    f'This field should contain a list of {cls.delimiter} delimited messages for the user to answer.', 
                    f'There should be NO OTHER FORMATTING OTHER THAN QUESTIONS BEING SEPARATED BY A {cls.delimiter}. ',
                    f'This will be read in a console so it needs to be formatted appropriately. ',
                    f'The conversation in this document will be used to generate a project. ', 
                    f'Please ask all of the questions that you will need to. ',
                    f'. ',
                ])
            }
        ]
    
    class ActionType(str, Enum):
        REQUEST_MORE_INFO = 'request_info'
        ALL_INFO_COLLECTED = 'all_info_collected'
    

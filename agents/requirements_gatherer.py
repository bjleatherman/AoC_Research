from agents.base_user_facing_role import User_Facing_Role
from agents.base_role import Role
from typing import Type, Dict, Any
from enum import Enum 

class RequirementsGatherer(User_Facing_Role):

    description = (
        'You are an LLM agent responsible for conversing with users to collect, clarify, '
        'and document detailed requirements for developing a basic Python software application. '
        'Engage users interactively, ask clarifying questions when necessary, and structure '
        'the gathered requirements clearly, specifying functional features, user interactions, '
        'inputs and outputs, constraints, and assumptions. You are working in an agile environment, '
        'so we don\'t need to waterfall the whole project. You are being too needy. Once there are a few good questions answered knock it off. This will be a console application written for python 3.12.4 with standard libraries available'
    )

    delimiter = ";"  # Easy to override if needed

    class ActionType(str, Enum):
        REQUEST_MORE_INFO = 'request_info'
        INFO_COLLECTED = 'info_collected'

    @staticmethod
    def get_fields(delimiter):
        return [
            {
                'name':'response', 
                'type':str, 
                'description':'\n'.join([
                    'This field contains the response to the prompt.',
                    f'This field should contain a list of {delimiter} delimited messages for the user to answer.', 
                    f'There should be NO OTHER FORMATTING OTHER THAN QUESTIONS BEING SEPARATED BY A {delimiter}.',
                    'This will be read in a console so it needs to be formatted appropriately.',
                    'The conversation in this document will be used to generate a project.',
                    'Please ask all of the questions that you will need to.'
                ])
            }
        ]

    def __init__(self):
        super().__init__()

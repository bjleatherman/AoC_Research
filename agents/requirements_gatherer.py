from agents.base_user_facing_role import User_Facing_Role
from agents.base_role import Role
from typing import Type, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field
from message_builder import MessageBuilder

class RequirementsGatherer(User_Facing_Role):

    description = (
        f'You are an LLM agent responsible for conversing with users to collect, clarify, '
        f'and document detailed requirements for developing a basic Python software application. '
        f'Engage users interactively, ask clarifying questions when necessary, and structure '
        f'the gathered requirements clearly, specifying functional features, user interactions, '
        f'inputs and outputs, constraints, and assumptions. You are working in an agile environment, '
        f'so we don\'t need to waterfall the whole project. You are being too needy. Once there are a few good questions answered knock it off. This will be a console application written for python 3.12.4 with standard libraries available'
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
                    f'This field contains the response to the prompt.',
                    f'This field should contain a list of {delimiter} delimited messages for the user to answer.', 
                    f'There should be NO OTHER FORMATTING OTHER THAN QUESTIONS BEING SEPARATED BY A {delimiter}.',
                    f'This will be read in a console so it needs to be formatted appropriately.',
                    f'The conversation in this document will be used to generate a project.',
                    f'Please ask all of the questions that you will need to.'
                ])
            }
        ]

    def __init__(self, log_file):
        super().__init__(log_file)

    def get_requirements_package(self):

        class RequirementsPackageAction(str, Enum):
            INFO_COLLECTED = 'info_collected'

        class RequirementsPackage(BaseModel):
            response: str = Field(description='List of project requirements')
            action: RequirementsPackageAction = Field(description='The only possible action is INFO_COLLECTED')

        query = 'please build project requirements based on the chat history'
        description = 'You build simple requirements documentation for simple applications using a chat history as a guide'

        response = MessageBuilder.build_send_message(
            query=query,
            system_description=description,
            response_format=RequirementsPackage,
            chat_history=self.current_chat_history
        )

        self.log_message(role='user', user_content=query)
        self.log_message(role='system', response=response.response, action=response.action.value)

        return response.response
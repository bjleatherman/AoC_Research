from enum import Enum
from pydantic import BaseModel, Field
from message_builder import MessageBuilder
from typing import Type, Dict, Any
from agents.base_role import Role

class User_Facing_Role(Role):
    
    class ActionType(str, Enum):
        REQUEST_MORE_INFO = 'request_info'
        INFO_COLLECTED = 'info_collected'

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

        print(response.response)
        print (response.action.value)

        if (response.action.value == self.ActionType.INFO_COLLECTED):
            return response
        else:
            self.process_response(response)


    def process_response(self, response):
        if (response.action.value == self.ActionType.REQUEST_MORE_INFO):
            questions = response.response.split(self.delimiter)
            answers = []
            count = 1
            for question in questions:
                print(f'{count}/ {len(questions)}')
                answer = input(f'{question}: ')
                answers.append(f'{question}: {answer}\n')
                count += 1
        self.send_message(''.join(answers))
        

    def __init__(self, log_file):
        super().__init__(log_file)
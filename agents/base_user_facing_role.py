from enum import Enum
from pydantic import BaseModel, Field
from message_builder import MessageBuilder
from typing import Type, Dict, Any
from agents.base_role import Role

class User_Facing_Role(Role):
    
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

        cls.process_response(response)

    @classmethod
    def process_response(cls, response):
        print('processing')

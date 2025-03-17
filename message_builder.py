from pydantic import BaseModel
from typing import Type
from dotenv import load_dotenv
import os
from openai import OpenAI

class MessageBuilder:
   
    DEFAULT_MODEL='gpt-4o-mini'

    @staticmethod
    def build_send_message(query: str, system_description: str, response_format: Type[BaseModel],chat_history=None, model=DEFAULT_MODEL):
        
        load_dotenv()
        
        client =  OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        full_chat = [{'role':'system', 'content':system_description}]
        if chat_history is not None:
            full_chat.extend(chat_history)
        full_chat.append({'role':'user', 'content':query})

        completion = client.beta.chat.completions.parse(
            model=model,
            messages=full_chat,
            response_format=response_format
        )
        return completion.choices[0].message.parsed
from pydantic import BaseModel
from typing import Type, List, Dict
from dotenv import load_dotenv
import os
from openai import OpenAI

class MessageBuilder:
   
    DEFAULT_MODEL='gpt-4o-mini'

    @staticmethod
    def format_chat_history(raw_logs: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Ensure chat history is properly formatted for OpenAI API."""
        formatted_chat = []
        for entry in raw_logs:
            if isinstance(entry, dict) and "role" in entry and "content" in entry:
                formatted_chat.append({"role": entry["role"], "content": entry["content"]})
            else:
                print(f"Skipping malformed entry: {entry}")  # Debugging step
        return formatted_chat

    @staticmethod
    def build_send_message(query: str, 
                           system_description: str, 
                           response_format: Type[BaseModel],
                           chat_history=None, 
                           model=DEFAULT_MODEL):
        
        load_dotenv()
        
        client =  OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        full_chat = [{'role':'system', 'content':system_description}]
        
        if chat_history:
            formatted_history = MessageBuilder.format_chat_history(chat_history)
            full_chat.extend(formatted_history)

        full_chat.append({'role':'user', 'content':query})

        # print(full_chat)

        completion = client.beta.chat.completions.parse(
            model=model,
            messages=full_chat,
            response_format=response_format
        )

        return completion.choices[0].message.parsed
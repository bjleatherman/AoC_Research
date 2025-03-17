from dotenv import load_dotenv
import os
from openai import OpenAI
import json
from pydantic_class import TicketResolution
from pydantic import BaseModel, Field
from typing import List
from role import Role
from role_coder import Coder
from role_file_architect import FileArchitect
from role_function_signatures import FunctionSignatureArchitect

prompt='do your part to build a project that takes a user input from the console and generates that number of the fibonacci sequence back out to the console'

response = FileArchitect.send_message(prompt)
# print(response)
print(response.response)
print(response.action.value)

response = FunctionSignatureArchitect.send_message(prompt)
# print(response)
print(response.response)
print(response.action.value)



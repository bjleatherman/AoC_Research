from pydantic import BaseModel, Field
from agents.base_role import Role

class Coder(Role):

    description='You are a python developer. If there is any ambiguity in the code that you are being asked to write, ask for clarity.'
    
    def __init__(self, log_file):
        super().__init__(log_file)
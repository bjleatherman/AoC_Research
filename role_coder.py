from pydantic import BaseModel, Field
from role import Role

class Coder(Role):

    description='You are a python developer. If there is any ambiguity in the code that you are being asked to write, ask for clarity.'
    
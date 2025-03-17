from pydantic import BaseModel, Field

# Define the Pydantic model
class TicketResolution(BaseModel):
    class Step(BaseModel):
        description: str = Field(description='Description of the step taken.')
        action: str = Field(description='Action taken to resolve the issue.')

    steps: list[Step]
    final_resolution: str = Field(
        description='The final message that will be sent to the customer.'
    )
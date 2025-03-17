from agents.coder import Coder
from agents.file_architect import FileArchitect
from agents.function_signatures import FunctionSignatureArchitect
from agents.requirements_gatherer import RequirementsGatherer

prompt='do your part to build a project that takes a user input from the console and generates that number of the fibonacci sequence back out to the console'

# response = FileArchitect.send_message(prompt)
# print(response)
# print(response.response)
# print(response.action.value)

# response = FunctionSignatureArchitect.send_message(prompt)
# print(response)
# print(response.response)
# print(response.action.value)


response = RequirementsGatherer.send_message(prompt)

while response.action.value != RequirementsGatherer.ActionType.ALL_INFO_COLLECTED:
    RequirementsGatherer.print_current_chat_history()
    user_response = input()
    response = RequirementsGatherer.send_message(user_response)
print(f'Action: {response.action.value}\nResponse: {response.response}')
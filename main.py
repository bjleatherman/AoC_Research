from agents.coder import Coder
from agents.file_architect import FileArchitect
from agents.function_signatures import FunctionSignatureArchitect
from agents.requirements_gatherer import RequirementsGatherer
from director import Director
from datetime import datetime

prompt='do your part to build a project that takes a user input from the console and generates that number of the fibonacci sequence back out to the console. Do not use any libraries'

date = datetime.now().strftime('%y-%m-%d %H_%M%S')
log_file = f'results/log/test_{date}.txt'
code_file = f'results/code/test_{date}.txt'

director = Director(log_file=log_file, code_file=code_file)
director.start()


# response = FileArchitect.send_message(prompt)
# print(response)
# print(response.response)
# print(response.action.value)

# response = FunctionSignatureArchitect.send_message(prompt)
# print(response)
# print(response.response)
# print(response.action.value)

# rg = RequirementsGatherer()

# response = rg.send_message(prompt)

# while response.action.value != RequirementsGatherer.ActionType.INFO_COLLECTED:
#     rg.print_current_chat_history()
#     user_response = input()
#     response = rg.send_message(user_response)
# print(f'Action: {response.action.value}\nResponse: {response.response}')
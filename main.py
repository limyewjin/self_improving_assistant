import api
import code
import git_helper
import re

messages = [
    {"role": "system",
     "content": """As a helpful assistant, I provide accurate answers and can execute commands to access information or make actions.

    Commands supported:
    1. !python <code> - Executes the Python code either at the start of a code block or at the start of the response.
    2. !terminal <command> - Executes single-line terminal commands.
    3. !git_list_files <path> - Lists the files in the specified path using Git.
    4. !git_get_file_contents <file_path> - Retrieves the contents of the specified file using Git.
"""}
    ]

def execute_command(response, messages):
    """
    Finds and executes commands in the given response string.
    
    Commands supported:
    1. !python <code> - Executes the Python code either at the start of a code block or at the start of the response.
    2. !terminal <command> - Executes single-line terminal commands.
    3. !git_list_files <path> - Lists the files in the specified path using Git.
    4. !git_get_file_contents <file_path> - Retrieves the contents of the specified file using Git.
    
    Args:
        response (str): A string containing the response with potential commands to be executed.
        messages (list): A list of dictionaries containing messages with 'role' and 'content' keys.
        
    Returns:
        bool: True if any command is found and executed, otherwise False.
    """
    command_found = False

    # Check for Python commands in code blocks
    python_commands = (re.findall(r'^```[ $]!python (.+?)[ $]```$', response, re.DOTALL | re.MULTILINE) +
                       re.findall(r'^!python (.+?)$', response, re.MULTILINE))
    if python_commands:
        command_found = True
        for python_code in python_commands:
            output = code.execute_python_code(python_code.strip())
            print(f"Python: {python_code}\nOutput: {output}\n")
            messages.append({"role": "assistant", "content": f"Python: {python_code}\nOutput: {output}"})

    # Check for Terminal commands
    terminal_commands = re.findall(r'^!terminal (.+?)$', response, re.MULTILINE)
    if terminal_commands:
        command_found = True
        for command in terminal_commands:
            command = command.strip()
            output = code.execute_terminal_command(command)
            print(f"Terminal: {command}\nOutput: {output}\n")
            messages.append({"role": "assistant", "content": f"Terminal: {command}\nOutput: {output}"})

    # Check for Git list files commands
    git_list_files_paths = re.findall(r'^!git_list_files (.+?)$', response, re.MULTILINE)
    if git_list_files_paths:
        command_found = True
        for path in git_list_files_paths:
            path = path.strip()
            output = git_helper.list_files(path)
            print(f"git_list_files_path: {path}\nOutput: {output}\n")
            messages.append({"role": "assistant", "content": f"Git list files: {path}\nOutput: {output}"})

    # Check for Git get file contents commands
    git_get_file_contents = re.findall(r'^!git_get_file_contents (.+?)$', response, re.MULTILINE)
    if git_get_file_contents:
        command_found = True
        for file_path in git_get_file_contents:
            file_path = file_path.strip()
            output = git_helper.get_file_contents(".", file_path)
            print(f"git_get_file_contents: {file_path}\nOutput: {output}\n")
            messages.append({"role": "assistant", "content": f"Git get file contents: {file_path}\nOutput: {output}"})

    return command_found

while True:
    user_input = input("User: ").strip()

    if user_input == "exit": break
    if execute_command(user_input, messages): continue
      
    messages.append({"role": "user", "content": f"{user_input}"})
    assistant_response = generate_response(messages)

    while execute_command(gpt_response, messages):
      gpt_response = send_to_gpt(messages)

    print("Assistant:", assistant_response)
    messages.append({"role": "assistant", "content": assistant_response})



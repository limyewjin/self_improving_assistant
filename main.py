import api
import code
import constants
import git_helper
import re
import traceback

def execute_command(response, messages):
    """
    Finds and executes commands in the given response string.
    
    Commands supported:
    1. !python <code> - Executes the Python code either at the start of a code block or at the start of the response.
    2. !terminal <command> - Executes single-line terminal commands.
    3. !git_list_files <path> - Lists the files in the specified path using Git.
    4. !git_get_file_contents <file_path> - Retrieves the contents of the specified file using Git.
    5. !git_update_file_contents <file_path> <new_content> - Updates the file path to new content.
    6. !git_make_commit <commit_message> - Add all changes, commit, and push to the origin repository.
    
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
            try:
                output = code.execute_python_code(python_code.strip())
                print(f"Python: {python_code}\nOutput: {output}\n")
                messages.append({"role": "assistant", "content": f"Python: {python_code}\nOutput: {output}"})
            except Exception as e:
                traceback.print_exc()
                messages.append({"role": "assistant", "content": f"Error executing Python code: {str(e)}"})

    # Check for Terminal commands
    terminal_commands = re.findall(r'^!terminal (.+?)$', response, re.MULTILINE)
    if terminal_commands:
        command_found = True
        for command in terminal_commands:
            try:
                command = command.strip()
                output = code.execute_terminal_command(command)
                print(f"Terminal: {command}\nOutput: {output}\n")
                messages.append({"role": "assistant", "content": f"Terminal: {command}\nOutput: {output}"})
            except Exception as e:
                traceback.print_exc()
                messages.append({"role": "assistant", "content": f"Error executing terminal command: {str(e)}"})

    # Check for Git list files commands
    git_list_files_paths = re.findall(r'^!git_list_files (.+?)$', response, re.MULTILINE)
    if git_list_files_paths:
        command_found = True
        for path in git_list_files_paths:
            try:
                path = path.strip()
                output = git_helper.list_files(path)
                print(f"git_list_files_path: {path}\nOutput: {output}\n")
                messages.append({"role": "assistant", "content": f"Git list files: {path}\nOutput: {output}"})
            except Exception as e:
                traceback.print_exc()
                messages.append({"role": "assistant", "content": f"Error listing files: {str(e)}"})

    # Check for Git get file contents commands
    git_get_file_contents = re.findall(r'^!git_get_file_contents (.+?)$', response, re.MULTILINE)
    if git_get_file_contents:
        command_found = True
        for file_path in git_get_file_contents:
            try:
                file_path = file_path.strip()
                output = git_helper.get_file_contents(".", file_path)
                print(f"git_get_file_contents: {file_path}\nOutput: {output}\n")
                messages.append({"role": "assistant", "content": f"Git get file contents: {file_path}\nOutput: {output}"})
            except Exception as e:
                traceback.print_exc()
                messages.append({"role": "assistant", "content": f"Error getting file contents: {str(e)}"})

    # Check for Git update file contents commands
    git_update_file_contents = (
        re.findall(r'^!git_update_file_contents (.+?)(?:$|```)', response, flags=re.MULTILINE) +
        re.findall(r'^.*```\n!git_update_file_contents (.+?)\n```.*$', response, flags=re.MULTILINE | re.DOTALL))
    if git_update_file_contents:
        if len(git_update_file_contents) == 1:
            command_found = True
            try:
                parts = git_update_file_contents[0].split(' ')
                file_path = parts[0].strip()
                content = ' '.join(parts[1:]).strip()
                if content.startswith('"') and content.endswith('"'):
                    content = content.strip('"')
                if content.startswith("'") and content.endswith("'"):
                    content = content.strip("'")
                if content.count('\n') <= 1:
                    content = content.encode("utf-8").decode("unicode_escape")
                output = git_helper.update_file_contents(".", file_path, content)
                print(f"git_update_file_contents: {file_path}\nOutput: {output}\n")
                messages.append({"role": "assistant", "content": f"Git update file contents: {file_path}\nOutput: {output}"})
            except Exception as e:
                traceback.print_exc()
                messages.append({"role": "assistant", "content": f"Error updating file contents: {str(e)}"})
        else:
            print(f"git_update_file_contents: unable to parse")
            messages.append({"role": "assistant", "content": f"Git update file contents: unable to parse"})

    # Check for Git get file contents commands
    git_make_commit = re.findall(r'^!git_make_commit (.+?)$', response, re.MULTILINE)
    if git_make_commit:
        if len(git_make_commit) == 1:
            command_found = True
            try:
                commit_message = git_make_commit[0].strip()
                git_helper.make_commit(".", commit_message)
                print(f"git_make_commit: {commit_message}\n")
                messages.append({"role": "assistant", "content": f"Git make commit\nOutput: {commit_message}"})
            except Exception as e:
                traceback.print_exc()
                messages.append({"role": "assistant", "content": f"Error making commit: {str(e)}"})
        else:
            print(f"git_make_commit: unable to parse")
            messages.append({"role": "assistant", "content": f"Git make commit: unable to parse"})

    return command_found

def optimize_messages(messages):
    new_messages = []
    context = ""
    for message in messages:
        if message["role"] == "assistant" and message["content"].strip() == "":
            continue
        if "\nOutput:" in message["content"] and not message["content"].startswith("Git get file contents"):
            if len(message["content"]) > 100:
                # Use GPT to decide whether to keep the message or rewrite it
                new_context = context + message["content"]
                response = api.generate_response([{"role": "assistant", "content": new_context}, {"role": "assistant", "content": "Optimize messages"}])
                if len(response) > 100:
                    # Rewrite the message to optimize the size
                    message["content"] = message["content"][:50] + "..." + message["content"][-50:]
                    context += message["content"]
                else:
                    # Keep the message
                    context = new_context
        new_messages.append(message)
    return new_messages

messages = constants.messages

while True:
    user_input = input("User: ").strip()

    if user_input == "exit": break
    if execute_command(user_input, messages): continue
      
    messages.append({"role": "user", "content": f"{user_input}"})
    gpt_response = api.generate_response(messages)
    print("Assistant:", gpt_response)

    while execute_command(gpt_response, messages):
      gpt_response = api.generate_response(messages)
      print("Assistant:", gpt_response)

    messages.append({"role": "assistant", "content": gpt_response})
    messages = optimize_messages(messages)

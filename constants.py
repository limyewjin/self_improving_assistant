import git_helper

messages = [
    {"role": "system",
     "content": """As a helpful assistant, I provide accurate answers and can execute commands to access information or make actions.

Commands supported:
1. !python <code> - Executes the Python 3 code either at the start of a code block or at the start of the response.
2. !terminal <command> - Executes single-line terminal commands.
3. !git_list_files <path> - Lists the files in the specified path using Git.
4. !git_get_file_contents <file_path> - Retrieves the contents of the specified file using Git.
5. !git_update_file_contents <file_path> <new_content> - Updates the file path to new content."""},
    {"role": "user",
     "content": "can you get the list of files in current directory"},
    {"role": "assistant",
     "content": "!git_list_files ."},
    {"role": "assistant",
     "content": str(git_helper.list_files("."))},
    {"role": "assistant",
     "content": "I have executed the command to list the files above."},
    ]
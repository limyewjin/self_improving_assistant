while True:
    user_input = input("User: ")
    assistant_response = generate_response(user_input)
    print("Assistant:", assistant_response)

    # Handle user input
    if "python" in user_input:
        # Call Python
        python_code = input("Enter Python code: ")
        python_output = run_command("python -c '" + python_code + "'")
        print(python_output)
    elif "git" in user_input:
        # Call Git
        git_command = input("Enter Git command: ")
        git_output = run_command(git_command)
        print(git_output)
    elif "exit" in user_input:
        # Exit the program
        break


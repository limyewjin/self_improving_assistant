import subprocess

import io
from contextlib import redirect_stdout, redirect_stderr

def execute_python_code(code):
    """
    Executes a given Python code string and returns the standard output and error as strings.

    Args:
        code (str): A string containing Python code to be executed.

    Returns:
        tuple: A tuple containing the standard output (stdout) and standard error (stderr) as strings.
    """
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    try:
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            exec(code, globals())
    except Exception as e:
        return None, str(e)
    return stdout_buffer.getvalue(), stderr_buffer.getvalue()

def execute_terminal_command(command, timeout=None, shell=False, print_output=False, raise_on_error=True):
    """
    Run a terminal command and return the output, error, and return code.

    Args:
        command (str): The command to run.
        timeout (int, optional): Maximum time (in seconds) to wait for the command to complete. Defaults to None.
        shell (bool, optional): Run the command in a shell. Defaults to False.
        print_output (bool, optional): Print the output and error streams. Defaults to False.
        raise_on_error (bool, optional): Raise an exception if the command returns a non-zero exit status. Defaults to True.

    Returns:
        dict: A dictionary containing the return code, stdout, and stderr.
    """
    try:
        process = subprocess.Popen(
            command.split() if not shell else command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=shell,
            text=True,
        )
        stdout, stderr = process.communicate(timeout=timeout)

        if process.returncode != 0 and raise_on_error:
            raise subprocess.CalledProcessError(
                process.returncode, command, output=stdout, stderr=stderr
            )

        if print_output:
            print(f"Output:\n{stdout}")
            if stderr:
                print(f"Error:\n{stderr}")

        return {
            "returncode": process.returncode,
            "stdout": stdout.strip(),
            "stderr": stderr.strip(),
        }

    except subprocess.TimeoutExpired as timeout_error:
        process.kill()
        print(f"TimeoutError: Command '{command}' timed out after {timeout} seconds")
        raise

    except subprocess.CalledProcessError as called_process_error:
        print(
            f"CalledProcessError: Command '{command}' returned non-zero exit status {called_process_error.returncode}"
        )
        if not raise_on_error:
            return {
                "returncode": called_process_error.returncode,
                "stdout": called_process_error.stdout.strip(),
                "stderr": called_process_error.stderr.strip(),
            }
        raise

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

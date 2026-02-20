import os
import subprocess
def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, file_path))
        # Will be True or False
        valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
        if valid_target_dir == True:
            if os.path.isfile(target_dir):
                if file_path.endswith('.py'):
                    try:
                        command = ["python", target_dir]
                        if not args is None:
                            command.extend(args)
                        result = subprocess.run(command, cwd=abs_working_dir, capture_output=True, text=True, timeout=30)
                        output = []
                        if result.returncode != 0:
                            output.append(f'Process exited with code {result.returncode}')
                        if result.stdout:
                            output.append(f"STDOUT:\n{result.stdout}")
                        if result.stderr:
                            output.append(f"STDERR:\n{result.stderr}")
                        if not result.stdout and not result.stderr:
                            output.append('No output produced')
                        return "\n".join(output)
                    except Exception as e:
                        return f"Error: executing Python file: {e}"
                else:
                    return f'Error: "{file_path}" is not a Python file'
            else:
                return f'Error: "{file_path}" does not exist or is not a regular file'
        else:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: executing Python file: {e}"
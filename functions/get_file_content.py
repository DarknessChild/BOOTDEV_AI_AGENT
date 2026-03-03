import os
from google.genai import types
schema_get_files_info = types.FunctionDeclaration(
    name="get_file_content",
    description="Runs arbitrary python code from a given file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Location of the python file to execute, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, file_path))
        # Will be True or False
        valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
        if valid_target_dir == True:
            if os.path.isfile(target_dir):
                try:
                    max_chars = 10000
                    with open(target_dir, 'r', encoding='utf-8') as f:
                        content = f.read(max_chars)
                        if f.read(1):
                            content += f'[...File "{file_path}" truncated at {max_chars} characters]'
                        return content
                except Exception as e:
                    return f'Error: {e}'
            else:
                return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f'Error: {e}'
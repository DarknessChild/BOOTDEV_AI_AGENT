import os
from google.genai import types
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
        # Will be True or False
        valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
        if valid_target_dir == True:
            if os.path.isdir(target_dir):
                try:
                    formatted_file_list = []
                    directory_files = os.listdir(target_dir)
                    for file in directory_files:
                        abs_file = os.path.join(target_dir, file)
                        file_size = os.path.getsize(abs_file)
                        is_dir = os.path.isdir(abs_file)
                        formatted_string = f"- {file}: file_size={file_size} bytes, is_dir={is_dir}"
                        formatted_file_list.append(formatted_string)
                    final_string = "\n".join(formatted_file_list)
                    return final_string
                except Exception as e:
                    return f'Error: {e}'
            else:
                return f'Error: "{directory}" is not a directory'
        else:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return f'Error: {e}'

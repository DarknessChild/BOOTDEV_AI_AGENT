import os
from google.genai import types
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file to a given location",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Location of where to write the file, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content to write to the new file. It should be UTF8 encoded text."
            )
        },
    ),
)
def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, file_path))
        # Will be True or False
        valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
        if valid_target_dir == True:
            if not os.path.isdir(target_dir):
                try:
                    folder_list = os.path.dirname(target_dir)
                    os.makedirs(folder_list, exist_ok=True)
                    with open(target_dir, "w") as f:
                        f.write(content)
                    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
                except Exception as e:
                    return f'Error: {e}'
            else:
                return f'Error: Cannot write to "{file_path}" as it is a directory'
        else:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f'Error: {e}'
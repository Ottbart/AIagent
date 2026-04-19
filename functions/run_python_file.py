import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file with optional arguments in a subprocess. Returns exit code, stdout and stderr",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Command-line arguments passed to the Python script",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A single argument",
                )
            ),
        },
    ),
)  

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file_abs]) == working_dir_abs

        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file_abs]

        if args:
            command.extend(args)

        running_process =  subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )

        output_str = []

        if running_process.returncode != 0:
            output_str.append(f"Process exited with code {running_process.returncode}")
        if not running_process.stdout and not running_process.stderr:
            output_str.append("No output produced")
        else:
            if running_process.stdout:
                output_str.append(f"STDOUT: {running_process.stdout}")
            if running_process.stderr:
                output_str.append(f"STDERR: {running_process.stderr}")
                
        return "\n".join(output_str)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"




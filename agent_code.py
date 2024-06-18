import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from langsmith import traceable
from langchain_community.tools.shell.tool import ShellTool
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
import subprocess
from typing import Optional

ROOT_DIR = "./"
VALID_FILE_TYPES = {"py", "txt", "md", "cpp", "c", "h", "hpp", "java", "kt", "asm", "s", "js", "jsx", "html", "css", "ts", "tsx", "json", "yml", "yaml", "xml", "csv"}


@tool
def create_react_app_with_vite():
    """
    This function creates a new React application using Vite in the 'app' directory located in the root.

    It navigates to the root directory, finds or creates the 'app' directory,
    and uses the npm 'create vite@latest' command to scaffold a new React project
    with Vite as the build tool and React as the template. If the process is
    successful, it prints a success message. If any subprocess command fails,
    it catches the CalledProcessError exception and prints an error message.
    """
    try:
        # Create a new Vite project in the app directory with React template
        subprocess.run(['npm', 'create', 'vite@latest', './app', '--template', 'react'], check=True)
        # Print success message if project creation is successful
        return f"Successfully created a new React app using Vite."
    except subprocess.CalledProcessError as e:
        # Print error message if any subprocess command fails
        return f"An error occurred: {e}"
    except Exception as e:
        # Print error message if any other exception occurs
        return f"An unexpected error occurred: {e}"


@tool
def create_directory(directory: str) -> str:
    """
    Create a new writable directory with the given directory name if it does not exist.
    If the directory exists, it ensures the directory is writable.

    Parameters:
    directory (str): The name of the directory to create.

    Returns:
    str: Success or error message.
    """
    if ".." in directory:
        return f"Cannot make a directory with '..' in path"
    try:
        os.makedirs(directory, exist_ok=True)
        subprocess.run(["chmod", "u+w", directory], check=True)
        return f"Directory successfully '{directory}' created and set as writeable."
    except subprocess.CalledProcessError as e:
        return f"Failed to create or set writable directory '{directory}': {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


@tool
def find_file(filename: str, path: str) -> Optional[str]:
    """
    Recursively searches for a file in the given path.
    Returns string of full path to file, or None if file not found.
    """
    # TODO handle multiple matches
    for root, dirs, files in os.walk(path):
        if filename in files:
            return os.path.join(root, filename)
    return None


@tool
def create_file(filename: str, content: str = "", directory=""):
    """Creates a new file and content in the specified directory."""
    # Validate file type
    try:
        file_stem, file_type = filename.split(".")
        assert file_type in VALID_FILE_TYPES
    except:
        return f"Invalid filename {filename} - must end with a valid file type: {valid_file_types}"
    directory_path = os.path.join(ROOT_DIR, directory)
    file_path = os.path.join(directory_path, filename)
    if not os.path.exists(file_path):
        try:
            with open(file_path, "w")as file:
                file.write(content)
            print(f"File '{filename}' created successfully at: '{file_path}'.")
            return f"File '{filename}' created successfully at: '{file_path}'."
        except Exception as e:
            print(f"Failed to create file '{filename}' at: '{file_path}': {str(e)}")
            return f"Failed to create file '{filename}' at: '{file_path}': {str(e)}"
    else:
        print(f"File '{filename}' already exists at: '{file_path}'.")
        return f"File '{filename}' already exists at: '{file_path}'."


@tool
def update_file(filename: str, content: str, directory: str = ""):
    """Updates, appends, or modifies an existing file with new content."""
    if directory:
        file_path = os.path.join(ROOT_DIR, directory, filename)
    else:
        file_path = find_file(filename, ROOT_DIR)

    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, "a") as file:
                file.write(content)
            return f"File '{filename}' updated successfully at: '{file_path}'"
        except Exception as e:
            return f"Failed to update file '{filename}' at: '{file_path}' - {str(e)}"
    else:
        return f"File '{filename}' not found at: '{file_path}'"


# List of tools to use
tools = [
    ShellTool(ask_human_input=True),
    create_directory,
    create_react_app_with_vite,
    find_file,
    create_file,
    update_file
]


# Configure the language model
llm = ChatOpenAI(model="gpt-4o", temperature=0)


# Set up the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert java developer.",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


# Bind the tools to the language model
llm_with_tools = llm.bind_tools(tools)


agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)


agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


if __name__ == "__main__":
    from langchain.tools import list

    # Main loop to prompt the user
    while True:
        user_prompt = input("Prompt: ")
        list(agent_executor.stream({"input": user_prompt}))

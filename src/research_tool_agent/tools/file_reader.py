from langchain_core.tools import tool

@tool
def file_reader(file_path: str) -> str:
    """
    Reads the content of a local text file.
    Input should be the absolute or relative path to the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content[:2000] + ("... [truncated]" if len(content) > 2000 else "")
    except FileNotFoundError:
        return f"Error: File not found at path {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"
import sys
import os

# Add the project root directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.main import (
    check_env_vars,
    initialize_openai,
    parse_document,
    create_or_load_index,
    chat_with_index_with_options,
)


def main():
    # Check environment variables and retrieve API keys
    openai_api_key, llama_cloud_api_key = check_env_vars()

    # Initialize OpenAI with the API key
    initialize_openai(openai_api_key)

    # Specify the name of the file to parse
    hardcoded_file_name = "proton_x70.html"

    # Extract the base name of the file without the extension
    origin_basename, _ = os.path.splitext(hardcoded_file_name)

    # Parse the document using the specified file name and the Llama Cloud API key
    parse_file_path = parse_document(hardcoded_file_name, llama_cloud_api_key)

    # Create or load the index using the parsed file path and the base name
    index = create_or_load_index(parse_file_path, origin_basename)

    # Start a chat session with the created index with predefined questions
    chat_with_index_with_options(index)


if __name__ == "__main__":
    # Call the main function when the script is executed directly
    main()

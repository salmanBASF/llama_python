# tutorial/5-upload-origin.py

import os

from utils.main import (
    check_env_vars,
    initialize_openai,
    parse_document,
    create_or_load_index,
    chat_with_index_with_options,
)

from utils.archive import (
    upload_file,
)


def main():
    # Check environment variables and retrieve API keys
    openai_api_key, llama_cloud_api_key = check_env_vars()

    # Initialize OpenAI with the API key
    initialize_openai(openai_api_key)

    # hardcoded_file_name = "proton_x70.html"
    file_name = upload_file()

    # Parse the document using the specified file name and the Llama Cloud API key
    parse_file_path = parse_document(file_name, llama_cloud_api_key)

    # Create or load the index using the parsed file path and the base name
    index = create_or_load_index(parse_file_path)

    # Start a chat session with the created index with predefined questions
    chat_with_index_with_options(index)


if __name__ == "__main__":
    # Call the main function when the script is executed directly
    main()

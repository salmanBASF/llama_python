# tutorial/8-reader-simplewebpage.py

import os

from utils.main import (
    check_env_vars,
    initialize_openai,
    parse_document,
    create_or_load_index,
    chat_with_index_with_options,
    save_text_to_storage_origin,
)
from llama_index.readers.web import SimpleWebPageReader


def main():
    # Check environment variables and retrieve API keys
    openai_api_key, llama_cloud_api_key = check_env_vars()

    # Initialize OpenAI with the API key
    initialize_openai(openai_api_key)

    # url rom which you want to fetch data
    # NOTE: not every website can be parsed, some websites may block the request
    url = "https://www.nst.com.my/opinion/letters/2024/08/1088777/earth-choking-waste"

    # Extract the filename from url.
    # Examples: url = "https://www.nst.com.my/news/earth-choking-waste" -> "earth-choking-waste.html"
    url_file_name = url.split("/")[-1] + ".html"

    # Create an instance of SimpleWebPageReader
    web_page_reader = SimpleWebPageReader()

    # Load data from the URLs
    documents = web_page_reader.load_data(urls=[url])

    # just take the first document
    document = documents[0]

    # Save the document to the storage_origin
    save_text_to_storage_origin(document.text, url_file_name)

    # Parse the document using the specified file name and the Llama Cloud API key
    parse_file_path = parse_document(url_file_name, llama_cloud_api_key)

    # Create or load the index using the parsed file path and the base name
    index = create_or_load_index(parse_file_path)

    # Start a chat session with the created index with predefined questions
    chat_with_index_with_options(index)


if __name__ == "__main__":
    # Call the main function when the script is executed directly
    main()

import os

from utils.main import (
    check_env_vars,
    initialize_openai,
    parse_document,
    create_or_load_index,
    chat_with_index,
)

# from llama_index.readers.file import PandasCSVReader


def main():
    # Check environment variables and retrieve API keys
    openai_api_key, llama_cloud_api_key = check_env_vars()

    # Initialize OpenAI with the API key
    initialize_openai(openai_api_key)

    # Specify the name of the file to parse
    excel_filename = "employeesData.csv"

    # parser = PandasCSVReader()

    # # Loading data using the LlamaParse instance
    # documents = parser.load_data(f"./storage_origin/{excel_filename}")

    # # Extracting the text content from the parsed documents
    # print(documents[0])

    # # Opening the parse_file_path in write mode
    # with open(parse_file_path, "w", encoding="utf-8") as output_file:
    #     output_file.write(text_doc)  # Writing the text_doc content to the output_file

    # print(
    #     f"Document parsed and saved to {parse_file_path}"
    # )  # Printing a message indicating the successful parsing and saving of the document
    # return parse_file_path  # Returning the parse_file_path

    # Parse the document using the specified file name and the Llama Cloud API key
    parse_file_path = parse_document(excel_filename, llama_cloud_api_key)

    # Create or load the index using the parsed file path and the base name
    index = create_or_load_index(parse_file_path)

    # Start a chat session with the created index
    chat_with_index(index)


if __name__ == "__main__":
    # Call the main function when the script is executed directly
    main()

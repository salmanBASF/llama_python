# utis/main.py

import os  # Importing the os module for operating system related functionalities

from llama_index.core import (  # Importing specific classes from the llama_index.core module
    Settings,  # Importing the Settings class
    VectorStoreIndex,  # Importing the VectorStoreIndex class
    SimpleDirectoryReader,  # Importing the SimpleDirectoryReader class
    StorageContext,  # Importing the StorageContext class
    load_index_from_storage,  # Importing the load_index_from_storage function
)

# Importing the OpenAI class from the llama_index.llms.openai module
from llama_index.llms.openai import OpenAI

# Importing the LlamaParse class from the llama_parse module
from llama_parse import LlamaParse

from dotenv import load_dotenv

from utils.parse import extraction_rules

# Load environment variables from .env file
load_dotenv()


def check_env_vars():
    """
    Check for necessary environment variables and return their values.
    Raises:
        ValueError: If any of the required environment variables are not set.
    Returns:
        tuple: OPENAI_API_KEY and LLAMA_CLOUD_API_KEY
    """
    # Getting the value of the OPENAI_API_KEY environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Getting the value of the LLAMA_CLOUD_API_KEY environment variable
    llama_cloud_api_key = os.getenv("LLAMA_CLOUD_API_KEY")

    # Checking if the OPENAI_API_KEY variable is not set
    if openai_api_key is None:
        raise ValueError("OPENAI_API_KEY variable not set in .env")

    # Checking if the LLAMA_CLOUD_API_KEY variable is not set
    if llama_cloud_api_key is None:
        raise ValueError("LLAMA_CLOUD_API_KEY variable not set in .env")

    # Returning the values of the environment variables
    return (
        openai_api_key,
        llama_cloud_api_key,
    )


def initialize_openai(
    api_key,
):
    """
    Initialize the OpenAI model with the provided API key.
    Args:
        api_key (str): The API key for OpenAI.
    """
    # Initializing the OpenAI model with the provided api_key
    Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0, api_key=api_key)


def parse_document(file_name, api_key):
    """
    Parse a document and save the parsed content to a markdown file.
    Args:
        file_name (str): The name of the file to parse.
        api_key (str): The API key for LlamaParse.
    Returns:
        str: The path to the parsed document.
    """

    # Splitting the file_name into basename and extension
    # example file_name = "example.txt" -> origin_basename = "example", extension = ".txt"
    origin_basename, extension = os.path.splitext(file_name)

    # Generating the parse_file_path based on the basename
    parse_file_path = f"./storage_parse/{origin_basename}.md"

    # Checking if the parse_file_path already exists
    if os.path.exists(parse_file_path):
        print(f"Using existing Parse Documents in {parse_file_path} \n")
        return parse_file_path

    # else parse the document
    parser = LlamaParse(  # Creating an instance of the LlamaParse class
        api_key=api_key,  # Passing the api_key parameter to the LlamaParse constructor
        result_type="markdown",  # Setting the result_type to "markdown"
        # parsing_instruction=(  # Providing parsing instructions as a string
        #     "Extract main content. Remove navigation elements, sidebars, footers, "
        #     "and unrelated content. Set heading level 1 for the title of the content. "
        #     "There is only one heading level 1"
        # ),
        parsing_instruction=extraction_rules,
    )

    # Loading data using the LlamaParse instance
    documents = parser.load_data(f"./storage_origin/{file_name}")

    # Extracting the text content from the parsed documents
    text_doc = documents[0].text

    # Opening the parse_file_path in write mode
    with open(parse_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(text_doc)  # Writing the text_doc content to the output_file

    print(
        f"Document parsed and saved to {parse_file_path}"
    )  # Printing a message indicating the successful parsing and saving of the document
    return parse_file_path  # Returning the parse_file_path


def create_or_load_index(parse_file_path):
    """
    Create or load an index from the parsed document.
    Args:
        parse_file_path (str): The path to the parsed document.
    Returns:
        VectorStoreIndex: The loaded or created index.
    """
    # Extract the base name of the file without the extension
    # example: parse_file_path = "./storage_parse/some-example.md" -> origin_basename = "some-example"
    origin_basename = os.path.splitext(os.path.basename(parse_file_path))[0]

    # name of storage_index directory based on the origin_basename
    storage_index_dir = f"./storage_index/{origin_basename}"

    # Checking if the storage_index_dir already exists
    if os.path.exists(storage_index_dir):
        print(f"Using existing Index in {storage_index_dir}/ \n")

        # Creating a StorageContext instance with the persist_dir set to storage_index_dir
        storage_context = StorageContext.from_defaults(persist_dir=storage_index_dir)

        # Loading the index from the storage context
        index = load_index_from_storage(storage_context)
    else:
        print(f"Creating new index in {storage_index_dir}/ \n")

        # Creating an instance of the SimpleDirectoryReader class
        # Providing the parse_file_path as the input_files parameter
        parse_documents = SimpleDirectoryReader(
            input_files=[parse_file_path]
        ).load_data()  # Loading data using the SimpleDirectoryReader instance

        # Creating a VectorStoreIndex from the parse_documents
        index = VectorStoreIndex.from_documents(parse_documents)

        # Persisting the index to the storage context
        index.storage_context.persist(persist_dir=storage_index_dir)

    return index  # Returning the index


def chat_with_index(index) -> None:
    """
    Chat with a given index using a query engine.
    Args:
        index (VectorStoreIndex): The index to use for the chat.
    """
    query_engine = index.as_query_engine()  # Creating a query engine from the index

    print(
        "You may start chatting with your data. Enter 'exit' or 'quit' to end the chat.\n"
    )

    while True:  # Starting an infinite loop
        user_input = input("User: ")  # Prompting the user for input

        # Checking if the user wants to exit the chat
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting chat...")
            break  # Exiting the loop

        try:
            # Querying the index with the user input
            response = query_engine.query(user_input)
            print("Bot: ", response)

        except Exception as e:
            print(f"An error occurred: {e}")

        print("\n")  # Printing a new line


def chat_with_index_with_options(index) -> None:
    """
    Chat with a given index using a query engine with predefined options.
    Args:
        index (VectorStoreIndex): The index to use for the chat.
    """
    query_engine = index.as_query_engine()  # Creating a query engine from the index

    print(
        "Welcome to the chat! Select an option to start or type 'exit' or 'quit' to end the chat.\n"
    )
    options = {
        "1": "What is title of the main content?",
        "2": "List interesting points from the main content.",
        "3": "Please summarize the main content",
        "4": "What is the source of the content?",
        "5": "Other question",
    }

    while True:  # Starting an infinite loop
        print("Options:")

        # Iterate over the items in the options dictionary
        for key, value in options.items():
            print(f"{key}. {value}")  # Print the key and value of each item

        user_selection = input("\n Select an option (1-5): ")

        if user_selection.lower() in {
            "exit",
            "quit",
        }:  # Checking if the user wants to exit the chat
            print(
                "Exiting chat..."
            )  # Printing a message indicating the end of the chat
            break  # Exiting the loop

        if user_selection in options:
            if user_selection == "5":
                user_input = input("User: ")  # Prompting the user for custom input
            else:
                user_input = options[user_selection]

            try:
                # Querying the index with the user input
                response = query_engine.query(user_input)
                print("Bot: ", response)  # Printing the response from the index
            except Exception as e:
                print(
                    f"An error occurred: {e}"
                )  # Handling any exceptions that occur during the query

            print("\n")  # Printing a new line
        else:
            print("Invalid selection. Please choose a valid option.\n")


def save_text_to_storage_origin(text, file_name):
    # storage_origin directory if it doesn't exist
    storage_origin_dir = "./storage_origin"

    # Derive the file name from the URL if not provided
    if not file_name.endswith(".html"):
        file_name += ".html"

    # Create the full file path ending with extension .html
    file_path = os.path.join(storage_origin_dir, file_name)

    # Checking if the parse_file_path already exists
    if os.path.exists(file_path):
        print(f"Using existing origin document in {file_path} \n")
        return file_name

    # else Save the HTML content to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)

    print(f"Website HTML saved to {file_path}")

    return file_name


# Example usage:
# openai_api_key, llama_cloud_api_key = check_env_vars()
# initialize_openai(openai_api_key)
# parse_file_path = parse_document("example.txt", llama_cloud_api_key)
# index = create_or_load_index(parse_file_path, "example")
# chat_with_index(index) or chat_with_index_with_options(index)

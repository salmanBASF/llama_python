import os  # Importing the os module for operating system related functionalities
from llama_index.core import (  # Importing specific classes from the llama_index.core module
    Settings,  # Importing the Settings class
    VectorStoreIndex,  # Importing the VectorStoreIndex class
    SimpleDirectoryReader,  # Importing the SimpleDirectoryReader class
    StorageContext,  # Importing the StorageContext class
    load_index_from_storage,  # Importing the load_index_from_storage function
)
from llama_index.llms.openai import (
    OpenAI,
)  # Importing the OpenAI class from the llama_index.llms.openai module
from llama_parse import (
    LlamaParse,
)  # Importing the LlamaParse class from the llama_parse module
from dotenv import (
    load_dotenv,
)  # Importing the load_dotenv function from the dotenv module

# Load environment variables from .env file
load_dotenv()


def check_env_vars():  # Defining a function named check_env_vars
    openai_api_key = os.getenv(
        "OPENAI_API_KEY"
    )  # Getting the value of the OPENAI_API_KEY environment variable
    llama_cloud_api_key = os.getenv(
        "LLAMA_CLOUD_API_KEY"
    )  # Getting the value of the LLAMA_CLOUD_API_KEY environment variable

    if openai_api_key is None:  # Checking if the OPENAI_API_KEY variable is not set
        raise ValueError(
            "OPENAI_API_KEY variable not set in .env"
        )  # Raising a ValueError with an error message
    if (
        llama_cloud_api_key is None
    ):  # Checking if the LLAMA_CLOUD_API_KEY variable is not set
        raise ValueError(
            "LLAMA_CLOUD_API_KEY variable not set in .env"
        )  # Raising a ValueError with an error message

    return (
        openai_api_key,
        llama_cloud_api_key,
    )  # Returning the values of the environment variables


def initialize_openai(
    api_key,
):  # Defining a function named initialize_openai that takes an api_key parameter
    Settings.llm = OpenAI(
        model="gpt-3.5-turbo", temperature=0, api_key=api_key
    )  # Initializing the OpenAI model with the provided api_key


def parse_document(
    file_name, api_key
):  # Defining a function named parse_document that takes file_name and api_key parameters
    origin_basename, extension = os.path.splitext(
        file_name
    )  # Splitting the file_name into basename and extension
    parse_file_path = f"./storage_parse/{origin_basename}.md"  # Generating the parse_file_path based on the basename

    if os.path.exists(
        parse_file_path
    ):  # Checking if the parse_file_path already exists
        print(
            f"Using existing Parse Documents in {parse_file_path} \n"
        )  # Printing a message indicating the use of existing parse documents
        return parse_file_path  # Returning the parse_file_path

    # else parse the document
    parser = LlamaParse(  # Creating an instance of the LlamaParse class
        api_key=api_key,  # Passing the api_key parameter to the LlamaParse constructor
        result_type="markdown",  # Setting the result_type to "markdown"
        parsing_instruction=(  # Providing parsing instructions as a string
            "Extract main content. Remove navigation elements, sidebars, footers, "
            "and unrelated content. Set heading level 1 for the title of the content. "
            "There is only one heading level 1"
        ),
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


def create_or_load_index(
    parse_file_path, origin_basename
):  # Defining a function named create_or_load_index that takes parse_file_path and origin_basename parameters
    storage_index_dir = f"./storage_index/{origin_basename}"  # Generating the storage_index_dir based on the origin_basename

    if os.path.exists(
        storage_index_dir
    ):  # Checking if the storage_index_dir already exists
        print(
            f"Using existing Index in {storage_index_dir}/ \n"
        )  # Printing a message indicating the use of existing index
        storage_context = StorageContext.from_defaults(
            persist_dir=storage_index_dir
        )  # Creating a StorageContext instance with the persist_dir set to storage_index_dir
        index = load_index_from_storage(
            storage_context
        )  # Loading the index from the storage context
    else:
        print(
            f"Creating new index in {storage_index_dir}/ \n"
        )  # Printing a message indicating the creation of a new index

        parse_documents = SimpleDirectoryReader(  # Creating an instance of the SimpleDirectoryReader class
            input_files=[
                parse_file_path
            ]  # Providing the parse_file_path as the input_files parameter
        ).load_data()  # Loading data using the SimpleDirectoryReader instance

        index = VectorStoreIndex.from_documents(
            parse_documents
        )  # Creating a VectorStoreIndex from the parse_documents
        index.storage_context.persist(
            persist_dir=storage_index_dir
        )  # Persisting the index to the storage context

    return index  # Returning the index


def chat_with_index(index) -> None:
    """
    Function to chat with a given index using a query engine.

    Parameters:
    index: The index object used to create the query engine.
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
    Function to chat with a given index using a query engine.

    Parameters:
    index: The index object used to create the query engine.
    """
    query_engine = index.as_query_engine()  # Creating a query engine from the index

    print(
        "Welcome to the chat! Select an option to start or type 'exit' or 'quit' to end the chat.\n"
    )
    options = {
        "1": "What is this article about?",
        "2": "List interesting points from the article.",
        "3": "When was this article published?",
        "4": "What is the source of the article?",
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


# Example usage:
# Assuming 'my_index' is an instance of your index
# chat_with_index(my_index)

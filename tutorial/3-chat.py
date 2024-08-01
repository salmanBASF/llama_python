import os

# Import the classes and functions from llama_index
from llama_index.core import (
    Settings,
    VectorStoreIndex,  # used for loading an index from a storage location, allowing the retrieval of an existing index for further processing.
    # used for creating a vector store index, which is a data structure used for efficient storage and retrieval of vectors.
    SimpleDirectoryReader,  # used for reading data from a simple directory structure, which may contain text documents or other data files.
    StorageContext,  # This class may provide a context for storing data or managing storage-related operations within the llama_index framework.
    load_index_from_storage,  # used for loading an index from a storage location, allowing the retrieval of an existing index for further processing.
)
from llama_index.llms.openai import OpenAI
from llama_parse import LlamaParse
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# ---------------- LLAMAINDEX : ENV KEYS----------------#

# Read the API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

Settings.llm = OpenAI(api_key=openai_api_key)

if openai_api_key is None:
    # raises an error that needs to be handled by the calling code or by an exception handler.
    raise ValueError("OPENAI_API_KEY variable not set in .env")

# Read the API key from the environment variable
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")


# ---------------- LLAMA CLOUD : PARSING----------------#


# Specify the origin filename of the document to be parsed. Note: the file must be inside storage_origin folder
ORIGIN_FILE_NAME = "samsung_galaxy.html"

# Split the filename into the base name and extension
origin_basename, extension = os.path.splitext(ORIGIN_FILE_NAME)

# Specify the file path for the parsed document. Note: md is file extension for markdown files. e.g /storage_parse/meta_ai.md
PARSE_FILE_PATH = f"./storage_parse/{origin_basename}.md"

# check if PARSE_FILE_PATH is exists,
if os.path.exists(PARSE_FILE_PATH):
    print(f"Using existing Parse Documents in {PARSE_FILE_PATH} \n")

# if not exists, parse the document
else:
    # Create an instance of the LlamaParse class
    parser = LlamaParse(
        api_key=LLAMA_CLOUD_API_KEY,  # can also be set in your env as LLAMA_CLOUD_API_KEY
        result_type="markdown",  # "markdown" and "text" are available
        parsing_instruction="Extract main content. Remove navigation elements , sidebars, footers, and unrelated content. Set heading level 1 for the title of the content. There is only one heading level 1",  # parsing instructions
    )

    # Load the origin document using the parser's load_data method. e.g /storage_origin/meta_ai.html
    documents = parser.load_data(f"./storage_origin/{ORIGIN_FILE_NAME}")

    # Extract the text content from the first document
    text_doc = documents[0].text

    # Print the extracted text
    print(text_doc)

    # Write the extracted text to the output file
    with open(PARSE_FILE_PATH, "w", encoding="utf-8") as output_file:
        output_file.write(text_doc)

    # Print a message indicating the successful download and save of the parsed document
    print(f"Document parsed and saved to {PARSE_FILE_PATH}")


# ---------------- LLAMA INDEX : INDEXING----------------#


# generate the folder named storage_index/{filename} automatically. e.g storage_index/meta_ai/
STORAGE_INDEX_DIR = f"./storage_index/{origin_basename}"


# if the index storage directory exists, load the existing index
if os.path.exists(STORAGE_INDEX_DIR):
    print(f"Using existing Index in {STORAGE_INDEX_DIR}/ \n")

    storage_context = StorageContext.from_defaults(persist_dir=STORAGE_INDEX_DIR)
    index = load_index_from_storage(storage_context)

# if the index storage directory not exists, create the new index
else:
    print(f"Creating new index in {STORAGE_INDEX_DIR}/ \n")

    # load the data from the PARSE_FILE_PATH
    parse_documents = SimpleDirectoryReader(input_files=[PARSE_FILE_PATH]).load_data()
    # create the index
    index = VectorStoreIndex.from_documents(parse_documents)
    # store the index in the storage_index directory
    index.storage_context.persist(persist_dir=STORAGE_INDEX_DIR)

# index object is being used to create a query engine for searching and retrieving information from the index
chat_engine = index.as_chat_engine(
    chat_mode="context",
    verbose=True,
    context_prompt=(
        "Only answer based on the context of the index. Else just say it was outside of the context"
    ),
)

print(
    "You may start chatting with your data. Enter 'exit' or 'quit' to end the chat. \n"
)


# Chat interaction loop
while True:
    # Get user input from the terminal
    user_input = input("User: ")

    # Check if the user wants to exit the chat
    if user_input.lower() == "exit" or user_input.lower() == "quit":
        print("Exiting chat...")
        break

    # Pass the user input to the chat engine for processing
    response = chat_engine.chat(user_input)

    # Display the response from the chat engine
    print("Chatbot: ", response)
    print("\n")

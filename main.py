# imports the os module, which provides a way to interact with the operating system. The os module in Python allows you to perform various operating system-related tasks, such as accessing the file system, working with environment variables, executing shell commands, and more.
import os


# import the load_dotenv function from the dotenv module.
# The dotenv module is commonly used for loading environment variables from a .env file into the environment where the Python script is running.
from dotenv import load_dotenv

# Import the classes and functions from llama_index
from llama_index.core import (
    VectorStoreIndex,  # used for creating a vector store index, which is a data structure used for efficient storage and retrieval of vectors.
    SimpleDirectoryReader,  # used for reading data from a simple directory structure, which may contain text documents or other data files.
    StorageContext,  # This class may provide a context for storing data or managing storage-related operations within the llama_index framework.
    load_index_from_storage,  # used for loading an index from a storage location, allowing the retrieval of an existing index for further processing.
)

# Load environment variables from .env file
load_dotenv()

# Read the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    # raises an error that needs to be handled by the calling code or by an exception handler.
    raise ValueError("OPENAI_API_KEY variable not set in .env")


# index directory name
INDEX_STORAGE_DIR = "./index_storage"

# check the index storage directory not exists, create the new indwx
if not os.path.exists(INDEX_STORAGE_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader("./data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=INDEX_STORAGE_DIR)

# if the index storage directory exists, load the existing index
if os.path.exists(INDEX_STORAGE_DIR):
    storage_context = StorageContext.from_defaults(persist_dir=INDEX_STORAGE_DIR)
    index = load_index_from_storage(storage_context)


# index object is being used to create a query engine for searching and retrieving information from the index
query_engine = index.as_query_engine()

# You can query any information you want from the document you uploaded
response = query_engine.query("Write a summary for the match.")

# print the response to the console
print(response)

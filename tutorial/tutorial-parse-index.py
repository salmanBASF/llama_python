import os
from llama_parse import LlamaParse
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

# ---------------- LLAMA CLOUD : PARSING----------------#

# Read the API key from the environment variable
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")

parser = LlamaParse(
    api_key=LLAMA_CLOUD_API_KEY,  # can also be set in your env as LLAMA_CLOUD_API_KEY
    result_type="markdown",  # "markdown" and "text" are available
    parsing_instruction="Extract main content. Remove navigation elements , sidebars, footers, and unrelated content. Set heading level 1 for the title of the content. There is only one heading level 1",  # parsing instructions
    show_progress=True,  # show progress bar
)


# Specify the filename for the HTML document to be parsed. Note: exclude the .html extension
html_filename = "samsung_galaxy"

# Load the HTML document using the parser's load_data method
documents = parser.load_data(f"./storage_document/{html_filename}.html")

# Extract the text content from the first document
text_doc = documents[0].text

# Print the extracted text
print(text_doc)

# Specify the output file path for the parsed document. Note: md is file extension for markdown files
parse_file_path = f"./storage_parse/{html_filename}.md"

# Write the extracted text to the output file
with open(parse_file_path, "w", encoding="utf-8") as output_file:
    output_file.write(text_doc)

# Print a message indicating the successful download and save of the parsed document
print(f"Documents downloaded and saved to {parse_file_path}")


# ---------------- LLAMA INDEX : INDEXING----------------#


# generate the folder named storage_index/{filename} automatically
STORAGE_INDEX_DIR = f"./storage_index/{html_filename}"

# check the index storage directory not exists, create the new indwx
if not os.path.exists(STORAGE_INDEX_DIR):
    # TODO load the data from the parse_file_path
    parse_documents = SimpleDirectoryReader(input_files=[parse_file_path]).load_data()
    # create the index
    index = VectorStoreIndex.from_documents(parse_documents)
    # store the index in the storage_index directory
    index.storage_context.persist(persist_dir=STORAGE_INDEX_DIR)

# if the index storage directory exists, load the existing index
if os.path.exists(STORAGE_INDEX_DIR):
    storage_context = StorageContext.from_defaults(persist_dir=STORAGE_INDEX_DIR)
    index = load_index_from_storage(storage_context)


# index object is being used to create a query engine for searching and retrieving information from the index
query_engine = index.as_query_engine()

# You can query any information you want from the document you uploaded
response = query_engine.query("What is the document is about?")

# print the response to the console
print(response)

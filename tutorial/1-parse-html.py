import os
from llama_parse import LlamaParse
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")

parser = LlamaParse(
    api_key=LLAMA_CLOUD_API_KEY,  # can also be set in your env as LLAMA_CLOUD_API_KEY
    result_type="markdown",  # "markdown" and "text" are available
    parsing_instruction="Extract only the main content. Remove navigation,sidebars,footers,ads,related articles,related news,license, copyright and unrelated contents",  # parsing instructions
    show_progress=True,  # show progress bar
)


# Specify the filename for the HTML document to be parsed. Note: exclude the .html extension
html_filename = "samsung_galaxy"

# Load the HTML document using the parser's load_data method
documents = parser.load_data(f"./storage_origin/{html_filename}.html")

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

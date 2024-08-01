import os
from llama_parse import LlamaParse
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("LLAMA_CLOUD_API_KEY")

parser = LlamaParse(
    api_key=api_key,  # can also be set in your env as LLAMA_CLOUD_API_KEY
    result_type="markdown",  # "markdown" and "text" are available
    parsing_instruction="Extract main content. Remove navigation elements , sidebars, footers, and unrelated content. Set heading level 1 for the title of the content. There is only one heading level 1",  # parsing instructions
    show_progress=True,  # show progress bar
)


# Specify the filename for the HTML document to be parsed. Note: exclude the .html extension
html_filename = "samsung_galaxy"

# Load the HTML document using the parser's load_data method
documents = parser.load_data(f"./resources/raw/{html_filename}.html")

# Extract the text content from the first document
text_doc = documents[0].text

# Print the extracted text
print(text_doc)

# Specify the output file path for the parsed document. Note: md is file extension for markdown files
output_file_path = f"./data/parsed/{html_filename}.md"

# Write the extracted text to the output file
with open(output_file_path, "w", encoding="utf-8") as output_file:
    output_file.write(text_doc)

# Print a message indicating the successful download and save of the parsed document
print(f"Documents downloaded and saved to {output_file_path}")

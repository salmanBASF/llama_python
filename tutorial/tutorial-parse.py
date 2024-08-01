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
    parsing_instruction="Remove header, homepage menu, footers, top navigation, links. Just extract the main content. remove unrelated elements or content from the page. Remove all the ads, popups, and other irrelevant content. Remove all the images, videos, and other media content. Remove all the links, buttons, and other interactive elements. Remove all the comments, reviews, and other user-generated content. Remove all the sidebars, footers, and other supplementary content. Remove all the headers, footers, and other navigational elements. Remove all the forms, input fields, and other interactive elements. Remove all the tables, charts, and other data visualizations. Remove all the lists, bullet points, and other list-based content. Remove all the quotes, citations, and other references. Remove all the code snippets, command-line output, and other code-related content. Remove all the timestamps, dates, and other temporal content. Remove all the page numbers, word counts, and other metadata. Remove all the copyright notices, licenses, and other legal content. Remove all the disclaimers, privacy policies, and other legal content. Remove all the contact information, addresses, and other personal data. Remove all the email addresses, phone numbers, and other contact information. Remove all the social media links, share buttons, and other social content. Remove all the advertisements, sponsorships, and other promotional content. Remove all the affiliate links, referral codes, and other monetization content. Remove all the tracking pixels, cookies, and other tracking content. Remove all the analytics scripts, tags, and other tracking content. Remove all the popups, modals, and other interactive elements. Remove all the cookies, GDPR notices, and other privacy content. Remove all the terms of service, privacy policies, and other legal content. Remove all the login forms, signup forms, and other user-related content. Remove all the search bars, filters, and other search-related content. Remove all the breadcrumbs, tags, and other navigational elements. Remove all the categories, tags, and other metadata. Remove all the related articles, recommended content, and other suggestions. Remove all the comments, reviews, and other user-generated content. Remove all the ratings, scores, and other user-generated content. Remove all the user profiles, avatars, and other user-generated content. Remove all the user comments, reviews, and other user-generated content. Remove all the user ratings, scores, and other user-generated content. Remove all the user profiles, avatars, and other user-generated content. Remove all the user-generated content, comments, reviews, and other user",
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

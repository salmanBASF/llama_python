# utis/main.py

import os  # Importing the os module for operating system related functionalities
import shutil  # built-in module that provides that allows you to perform various file-related tasks such as copying, moving, and deleting files and directories.
import requests  # The requests module is widely used in web scraping, API requests, and other web-related tasks.


from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def upload_file():
    """
    Prompt the user to upload a file and move it to the storage_origin directory.
    Returns:
        str: The file name of the uploaded file.
    """
    while True:
        file_path = input("Please enter the path to your file: ").strip()
        if os.path.isfile(file_path):
            # Create storage_origin directory if it doesn't exist
            storage_origin_dir = "./storage_origin"
            if not os.path.exists(storage_origin_dir):
                os.makedirs(storage_origin_dir)

            # Get the basename of the file to move
            file_name = os.path.basename(file_path)
            new_file_path = os.path.join(storage_origin_dir, file_name)

            # Move the file to the storage_origin directory
            shutil.copy(file_path, new_file_path)
            print(f"File moved to {new_file_path}")
            return file_name
        else:
            print("Invalid file path. Please try again.")


def save_website_html(url, file_name=None):
    """
    Save the HTML content of a website to the storage_origin directory.

    Args:
        url (str): The URL of the website to save.
        file_name (str, optional): The name of the file to save the HTML content. If not provided, it will be derived from the URL.

    Returns:
        str: The file name of the saved HTML content.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Create storage_origin directory if it doesn't exist
    storage_origin_dir = "./storage_origin"
    if not os.path.exists(storage_origin_dir):
        os.makedirs(storage_origin_dir)

    # Derive the file name from the URL if not provided
    if file_name is None:
        file_name = url.split("/")[-1] or "index.html"
        if not file_name.endswith(".html"):
            file_name += ".html"

    # Create the full file path
    file_path = os.path.join(storage_origin_dir, file_name)

    # Save the HTML content to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(response.text)

    print(f"Website HTML saved to {file_path}")

    return file_name

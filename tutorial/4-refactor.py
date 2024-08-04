import sys
import os

# Add the project root directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import (
    check_env_vars,
    initialize_openai,
    parse_document,
    create_or_load_index,
    chat_with_index,
)


def main():
    openai_api_key, llama_cloud_api_key = check_env_vars()
    initialize_openai(openai_api_key)

    hardcoded_file_name = "samsung_galaxy.html"
    parse_file_path = parse_document(hardcoded_file_name, llama_cloud_api_key)

    origin_basename, _ = os.path.splitext(hardcoded_file_name)
    index = create_or_load_index(parse_file_path, origin_basename)

    chat_with_index(index)


if __name__ == "__main__":
    main()

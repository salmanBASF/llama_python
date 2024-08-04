import os
from llama_index.core import (
    Settings,
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.llms.openai import OpenAI
from llama_parse import LlamaParse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def check_env_vars():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    llama_cloud_api_key = os.getenv("LLAMA_CLOUD_API_KEY")

    if openai_api_key is None:
        raise ValueError("OPENAI_API_KEY variable not set in .env")
    if llama_cloud_api_key is None:
        raise ValueError("LLAMA_CLOUD_API_KEY variable not set in .env")

    return openai_api_key, llama_cloud_api_key


def initialize_openai(api_key):
    Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0, api_key=api_key)


def parse_document(file_name, api_key):
    origin_basename, extension = os.path.splitext(file_name)
    parse_file_path = f"./storage_parse/{origin_basename}.md"

    if os.path.exists(parse_file_path):
        print(f"Using existing Parse Documents in {parse_file_path} \n")
        return parse_file_path

    parser = LlamaParse(
        api_key=api_key,
        result_type="markdown",
        parsing_instruction=(
            "Extract main content. Remove navigation elements, sidebars, footers, "
            "and unrelated content. Set heading level 1 for the title of the content. "
            "There is only one heading level 1"
        ),
    )

    documents = parser.load_data(f"./storage_origin/{file_name}")
    text_doc = documents[0].text

    with open(parse_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(text_doc)

    print(f"Document parsed and saved to {parse_file_path}")
    return parse_file_path


def create_or_load_index(parse_file_path, origin_basename):
    storage_index_dir = f"./storage_index/{origin_basename}"

    if os.path.exists(storage_index_dir):
        print(f"Using existing Index in {storage_index_dir}/ \n")
        storage_context = StorageContext.from_defaults(persist_dir=storage_index_dir)
        index = load_index_from_storage(storage_context)
    else:
        print(f"Creating new index in {storage_index_dir}/ \n")
        parse_documents = SimpleDirectoryReader(
            input_files=[parse_file_path]
        ).load_data()
        index = VectorStoreIndex.from_documents(parse_documents)
        index.storage_context.persist(persist_dir=storage_index_dir)

    return index


def chat_with_index(index):
    query_engine = index.as_query_engine()

    print(
        "You may start chatting with your data. Enter 'exit' or 'quit' to end the chat. \n"
    )

    while True:
        user_input = input("User: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting chat...")
            break

        response = query_engine.query(user_input)
        print("Bot: ", response)
        print("\n")

import os

# import openai
from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

load_dotenv()

# openai.api_key = os.getenv["OPENAI_API_KEY"]

# check if storage already exists
PERSIST_DIR = "./storage"

if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader("./data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)

if os.path.exists(PERSIST_DIR):
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

# Either way we can now query the index
chat_engine = index.as_chat_engine(
    chat_mode="context",
    verbose=True,
    context_prompt=(
        "Only answer based on the knowledge of the article. Else jus say i dont know"
    ),
)


response = chat_engine.chat("explain point 1 and 10")
print(response)

response = chat_engine.chat("who is Abu?")
print(response)

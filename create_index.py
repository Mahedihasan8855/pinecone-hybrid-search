import os
from dotenv import load_dotenv
import pinecone

# Load environment variables from .env
load_dotenv()

# Read environment variables
api_key = os.getenv('PINECONE_API_KEY')
index_name = os.getenv('INDEX_NAME')
env = os.getenv('ENVIRONMENT')
pinecone.init(api_key=api_key, environment= env)


if index_name in pinecone.list_indexes():
    print(f"Index '{index_name}' already exists. Skipping index creation.")
    index_description = pinecone.describe_index(index_name)
    print(index_description)
else:
    pinecone.create_index(
    index_name,
    dimension = 384,
    metric = "dotproduct",
    pod_type = "s1"
    )
    
    print(f"Index '{index_name}' created successfully.")



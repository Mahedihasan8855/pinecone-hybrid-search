import os
from dotenv import load_dotenv
import pinecone
import openai
import datetime

# Load environment variables from .env
load_dotenv()

# Read environment variables
api_key = os.getenv('PINECONE_API_KEY')
index_name = os.getenv('INDEX_NAME')
openai_api_key = os.getenv('OPENAI_API_KEY')  # Your OpenAI API key from environment variables
env = os.getenv('ENVIRONMENT')
openai.api_key = openai_api_key

# Initialize Pinecone connection
pinecone.init(api_key=api_key, environment= env)

try:
    pinecone.delete_index(index_name)
    print(f"{index_name} deleted")
except Exception as e:
    print(f"{index_name} not found")
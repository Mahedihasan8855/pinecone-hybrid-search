import os
from dotenv import load_dotenv
import pinecone

load_dotenv()

api_key = os.getenv('PINECONE_API_KEY')
index_name = os.getenv('INDEX_NAME')
env = os.getenv('ENVIRONMENT')
pinecone.init(api_key=api_key, environment=env)
index = pinecone.Index(index_name)

# Demo values for a single document
document_id = 'test_101'
sparse_vector_indices = [1, 3]
sparse_vector_values = [0.1, 0.3]

# Ensure dense vector has the correct dimension (384 in this case)
dense_vector = [0.5] * 384

metadata = {'name': 'test'}

# Prepare the data for upsert
sparse_values = {'indices': sparse_vector_indices, 'values': sparse_vector_values}
vectors = [{
    'id': document_id,
    'sparse_values': sparse_values,
    'values': dense_vector,
    'metadata': metadata
}]

# Upload the document to the index
upsert_response = index.upsert(vectors)


print(upsert_response)
from transformers import BertTokenizerFast  # !pip install transformers
from collections import Counter
import pinecone
import os
from dotenv import load_dotenv
from datasets import load_dataset  
import pinecone
from utils.embed_sparse import generate_sparse_vectors
from utils.embed_dense import generate_dense_vectors


load_dotenv()


api_key = os.getenv('PINECONE_API_KEY')
index_name = os.getenv('INDEX_NAME')
env = os.getenv('ENVIRONMENT')
pinecone.init(api_key=api_key, environment= env)
index = pinecone.Index(index_name)






def hybrid_scale(dense, sparse, alpha: float):
    # check alpha value is in range
    if alpha < 0 or alpha > 1:
        raise ValueError("Alpha must be between 0 and 1")
    # scale sparse and dense vectors to create hybrid search vecs
    hsparse = {
        'indices': sparse['indices'],
        'values':  [v * (1 - alpha) for v in sparse['values']]
    }
    hdense = [v * alpha for v in dense]
    return hdense, hsparse


def hybrid_query(question, top_k, alpha):
   # convert the question into a sparse vector
   sparse = generate_sparse_vectors([question])[0]
   # convert the question into a dense vector
   dense_vec = generate_dense_vectors(question)
   # scale alpha with hybrid_scale
   dense_vec, sparse = hybrid_scale(
      dense_vec, sparse, alpha
   )
   indices = sparse['indices']
   values = [float(x) for x in sparse['values']]
   sparse_values = {'indices': indices, 'values': values}
   result = index.query(
      vector=dense_vec,
      sparse_vector=sparse_values,
      top_k=top_k,
      include_metadata=True
   )
   # return search results as json
   return result
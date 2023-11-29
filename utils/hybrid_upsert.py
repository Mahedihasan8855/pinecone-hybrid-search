from tqdm.auto import tqdm
import os
from dotenv import load_dotenv
import pinecone
from utils.embed_sparse import generate_sparse_vectors
from utils.embed_dense import generate_dense_vectors


load_dotenv()

api_key = os.getenv('PINECONE_API_KEY')
index_name = os.getenv('INDEX_NAME')
env = os.getenv('ENVIRONMENT')
pinecone.init(api_key=api_key, environment=env)
index = pinecone.Index(index_name)



def upload_to_pinecone(contexts, pinecone_ids, metadatas,batch_size=32):
    for i in tqdm(range(0, len(contexts), batch_size)):
        pinecone_id = pinecone_ids[i]
        metadata = metadatas[i]
        # find end of batch
        i_end = min(i+batch_size, len(contexts))
        # extract batch
        context_batch = contexts[i:i_end]
        # create unique IDs
        ids = [str(x) for x in range(i, i_end)]
        # add context passages as metadata
        meta = [metadata]
        # create dense vectors
        dense_embeds = generate_dense_vectors(context_batch)
        # create sparse vectors
        sparse_embeds = generate_sparse_vectors(context_batch)

        vectors = []
        # loop through the data and create dictionaries for upserts
        for _id, sparse, dense, metadata in zip(
            ids, sparse_embeds, dense_embeds, meta
        ):
            indices = sparse['indices']
            values = [float(x) for x in sparse['values']]
            sparse_values = {'indices': indices, 'values': values}
            vectors.append({
                'id': pinecone_id,
                'sparse_values': sparse_values,
                'values': dense,
                'metadata': metadata
            })

        # upload the documents to the new hybrid index
        upsert_response = index.upsert(vectors)
        return upsert_response
from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
   'multi-qa-MiniLM-L6-cos-v1'
)

def generate_dense_vectors(context_batch):
    return model.encode(context_batch).tolist()
from collections import Counter
from transformers import BertTokenizerFast


tokenizer = BertTokenizerFast.from_pretrained(
   'bert-base-uncased'
)

def build_dict(input_batch):
 # store a batch of sparse embeddings
   sparse_emb = []
   # iterate through input batch
   for token_ids in input_batch:
       indices = []
       values = []
       # convert the input_ids list to a dictionary of key to frequency values
       d = dict(Counter(token_ids))
       for idx in d:
            indices.append(idx)
            values.append(d[idx])
       sparse_emb.append({'indices': indices, 'values': values})
   # return sparse_emb list
   return sparse_emb


def generate_sparse_vectors(context_batch):
   # create batch of input_ids
   inputs = tokenizer(
           context_batch, padding=True,
           truncation=True,
           max_length=512, add_special_tokens=False
   )['input_ids']
   # create sparse dictionaries
   sparse_embeds = build_dict(inputs)
   return sparse_embeds
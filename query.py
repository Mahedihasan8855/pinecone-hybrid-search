
from utils.hybrid_query import hybrid_query


question = "What causes an equity balancer?"
answer=hybrid_query(question, top_k=3, alpha=1)

print(answer['matches'][0]['metadata']['filename'])
print(answer['matches'][1]['metadata']['filename'])
print(answer['matches'][2]['metadata']['filename'])





# question, documentAnswer1 - filename: - score:  , documentAnswer2 - filename - score, documentAnswer3- filename - score  

from utils.hybrid_upsert import upload_to_pinecone


    
context = ["Single Security - Over view • Occasionally it is convenient to inspect in detail the simulated results for a single instrument • The “Single Security” simulator will produce the values that would result from using the Single Simulation (Base) setup parameters: o The income simulation will cover the same forecast months o Market value, duration & convexity will be calculated as indicated in the Single Simulation setup o To modify those parameters the “Save” button on the Single Simulation form saves the setup without running a simulation"]
ids = ['demo_data_001']
metadata =[{"is_active":0, "priority": 3}]
res = upload_to_pinecone(context, ids, metadata)
print(res)
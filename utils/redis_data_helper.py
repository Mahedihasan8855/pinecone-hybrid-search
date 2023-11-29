from redis import Redis
from utils.hybrid_upsert import upload_to_pinecone
import json
import os




def get_redis_connection():
    host = os.getenv("REDIS_HOST", "172.17.0.2")
    port = os.getenv("REDIS_PORT", "6379")
    password = os.getenv("REDIS_PASSWORD", "HG0Ml6f$")
    db = os.getenv("REDIS_DB", "0")

    # r = Redis(host=host, port=port, password=password, db=db, decode_responses=False)
    r = Redis(host=host, port=port, db=db, decode_responses=False)
    return r


def copy_full_data(redis_conn, partner):
    try:
        keys = redis_conn.keys('*')
        successful_uploads = 0

        if keys:
            for key in keys:
                hash_key = key.decode('utf-8')
                if hash_key.startswith(partner):
                    hash_data = redis_conn.hgetall(key)
                    
                    decoded_data = {key.decode('utf-8', errors='replace'): value.decode('utf-8', errors='replace') for key, value in hash_data.items()}

                    # Check the size of the metadata
                    metadata_size = len(json.dumps(decoded_data))
                    # if metadata_size <= 40000:
                    try:
                        text_data = decoded_data['text_chunk']
                        res = upload_to_pinecone([text_data], [hash_key], [{'filename': hash_key}])
                        print("Success: ", hash_key)
                        successful_uploads += 1
                        
                    except Exception as e:
                        print("Error", hash_key)
                        print("Detail", e)

        print(f"Total successful uploads: {successful_uploads}")
        return decoded_data

    except Exception as e:
        # Handle errors
        print(f"Error: {e}")
        return None




def get_key_data(redis_conn, key):
    try:
        hash_data = redis_conn.hgetall(key)
        decoded_data = {key.decode('utf-8', errors='replace'): value.decode('utf-8', errors='replace') for key, value in hash_data.items()}
        return decoded_data

    except Exception as e:
        # Handle errors
        print(f"Error: {e}")
        return None


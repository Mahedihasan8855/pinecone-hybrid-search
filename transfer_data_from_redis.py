from utils.redis_data_helper import copy_full_data, get_redis_connection
from dotenv import load_dotenv
import os


load_dotenv()

partner = os.getenv("PARTNER_NAME")

redis_client = get_redis_connection()
copy_full_data(redis_client, partner)
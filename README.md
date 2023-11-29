# Create virtual environment
python3 -m venv virtual

# Activate environment (UNIX)
(UNIX) source virtual/bin/activate
(WINDOWS) virtual/scripts/activate

# Install required packages
pip install -r requirements.txt


# Run Commands


python3 create_index.py

python3 csv_generation.py 

python3 insert.py 

python3 query.py

python3 transfer_data_from_redis.py

python3 drop_index.py


.env variables

PINECONE_API_KEY=
INDEX_NAME=
ENVIRONMENT=
PARTNER_NAME=
REDIS_HOST=
REDIS_PORT=
REDIS_PASSWORD=
REDIS_DB=0

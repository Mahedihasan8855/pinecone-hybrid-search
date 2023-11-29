import re
import os
import csv
from utils.hybrid_query import hybrid_query
from utils.redis_data_helper import get_key_data, get_redis_connection
import pandas as pd



redis_client = get_redis_connection()


def concatenate_strings_with_newline(document_answer, filename, score):
    concatenated_string = f"{document_answer} \nFilename: {filename}\nScore: {score}\n"
    return concatenated_string

def replace_base34(data):
    new_html = data['text_chunk']
    if data['has_image'] == '1':
        replacement = '<Base64Image>'
        pattern = r'<img\s+src="data:image/[^;]+;base64,[^"]+"\s+alt="[^"]*"\s+style="[^"]*">'
        new_html = re.sub(pattern, replacement, data['combined_chunk'])
        return new_html
    return new_html

def process_question(question, redis_conn):
    pinecone_answer = hybrid_query(question, top_k=3, alpha=1)

    if pinecone_answer['matches'] and len(pinecone_answer['matches']) > 0:
        id1 = pinecone_answer['matches'][0]['metadata']['filename']
        data_1 = get_key_data(redis_conn, id1)
        document_1 = replace_base34(data_1)
        csv_document1 = concatenate_strings_with_newline(document_1, id1, pinecone_answer['matches'][0]['score'])
    else:
        csv_document1 = None

    if len(pinecone_answer['matches']) > 1:
        id2 = pinecone_answer['matches'][1]['metadata']['filename']
        data_2 = get_key_data(redis_conn, id2)
        document_2 = replace_base34(data_2)
        csv_document2 = concatenate_strings_with_newline(document_2, id2, pinecone_answer['matches'][1]['score'])
    else:
        csv_document2 = None

    if len(pinecone_answer['matches']) > 2:
        id3 = pinecone_answer['matches'][2]['metadata']['filename']
        data_3 = get_key_data(redis_conn, id3)
        document_3 = replace_base34(data_3)
        csv_document3 = concatenate_strings_with_newline(document_3, id3, pinecone_answer['matches'][2]['score'])
    else:
        csv_document3 = None

    return csv_document1, csv_document2, csv_document3

def process_csv_and_write_results(input_csv_path, new_output_csv_path, redis_client):
    # Assuming you have the 'process_question' function defined as described in the question

    # Open the input CSV file
    with open(input_csv_path, 'r') as input_file:
        csv_reader = csv.DictReader(input_file)
        rows = list(csv_reader)

    # Create a list to store results
    results = []

    # Process each question and store the results
    for row in rows:
        question = row['Question']
        print(question)
        
        result1, result2, result3 = process_question(question, redis_client)

        # Append results to the list
        results.append({
            'Question': question,
            'DocumentAnswer1': result1,
            'DocumentAnswer2': result2,
            'DocumentAnswer3': result3,
        })

    # Write the results to a new CSV file
    with open(new_output_csv_path, 'w', newline='') as output_file:
        fieldnames = ['Question', 'DocumentAnswer1', 'DocumentAnswer2', 'DocumentAnswer3']
        csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        
        # Write the header
        csv_writer.writeheader()

        # Write the results
        csv_writer.writerows(results)

    print(f"Results written to {new_output_csv_path}")


input_folder = 'data/input'
output_folder = 'data/output'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
# Iterate over files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        input_csv_path = os.path.join(input_folder, filename)
        output_csv_path = os.path.join(output_folder, filename)
        print(output_csv_path)
        process_csv_and_write_results(input_csv_path, output_csv_path, redis_client)
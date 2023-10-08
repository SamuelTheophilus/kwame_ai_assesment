import os
import csv
import json
import time
import logging
from model import model
from elasticsearch import Elasticsearch
import traceback
from logger import logging_setup
from parsing import read_files, divide_passage_into_chunks

from flask import Flask
from config import get_config

app = Flask(__name__)
app.config.from_object(get_config())
elastic_search_url = app.config["ELASTIC_SEARCH_URL"]


# Set up indexing logger.
logger = logging_setup(logging.DEBUG)


# Set up index name and mapping.
index_name = "passage_embeddings_idx"
index_mapping = {
    "mappings": {
        "dynamic": "true",
        "properties": {
            "passages": {
                "type": "text"
            },
            "metadata": {
                "type": "object"
            },
            "embedding": {
                "type": "dense_vector",
                "dims": 768
            }
        }
    }
}

print("Indexing")
while True:  # Keep pinging the elastic search server until connection is made.
    try:
        logger.debug("Setting up connection to elastic search")
        print("Connecting")
        es = Elasticsearch("http://elasticsearch:9200")
        if es.info():
            logger.info("Succesfully connected to elastic search")
            print("Connection Successful")
            break
    except Exception as e:
        print(f"Exception: {e}")
        print("Error")
        logger.error(f"Connection error: {str(e)}\n")

    time.sleep(5)

def index_document(text: str, metadata: json):
    logger.debug("Indexing document into elastic search")
    try:
        formatted_text = read_files(text)
        chunks = divide_passage_into_chunks(formatted_text)

        for chunk in chunks.values():
            passage_embeddings = model.encode(chunk)
            doc = {
                'passage': chunk,
                'metadata': metadata,
                'embeddings': passage_embeddings

            }
            es.index(index=index_name, body=doc)

        es.indices.refresh(index=index_name)

        logger.info("Documents index")
    except Exception as e:
        logger.error(f"Error ::\n {str(e)}")
        logger.error(f"Error traceback ::\n {str(traceback.print_exc())}")

if __name__ == "__main__":
    # Defining document structure
    if es.indices.exists(index=index_name): es.indices.delete(index=index_name)
    es.indices.create(index=index_name, body=index_mapping)

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    passage_metadata_emb_path = os.path.join(project_root, "docs", "passage_metadata_emb.csv")

    # Open the fixed CSV file
    with open(passage_metadata_emb_path, "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)

        for row in csv_reader:
            Passage, Metadata, Embeddings = row
            if Metadata == "Metadata": continue
            metadata_dict = json.loads(Metadata)
            embeddings = json.loads(Embeddings)

            document = {
                "passage": Passage,
                "metadata": metadata_dict,
                "embedding": embeddings
            }

            es.index(index=index_name, document=document)

    # Refresh the index to make the data available for searching
    es.indices.refresh(index=index_name)
    # Check the document count in the index
    es.cat.count(index=index_name, format="json")

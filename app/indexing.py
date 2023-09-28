import csv
import json
import os
import time
from elasticsearch import Elasticsearch

index_name = "passage_embeddings_idx"
index_mapping = {
    "mappings":{
        "dynamic":"true",
        "properties":{
            "passages": {
                "type": "text"
            },
            "metadata":{
                "type":"object"
            },
            "embedding":{
                "type":"dense_vector",
                "dims": 768
            }
        }
    }
}




while True: #Keep pinging the elastic search server until connection is made.
    try:
        es = Elasticsearch("http://localhost:9200")
        if es.info():
            print("Connection Successful")
            break
    except Exception as e:
        print(f"Connection error: {str(e)}\n")

    time.sleep(5)

if __name__ == "__main__":
    # Defining document structure


    if es.indices.exists(index=index_name): es.indices.delete(index=index_name)
    es.indices.create(index = index_name, body = index_mapping)

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    passage_metadata_emb_path = os.path.join(project_root, "docs", "passage_metadata_emb.csv")

    # Open the fixed CSV file
    with open(passage_metadata_emb_path, "r", encoding = "utf-8") as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)
        
        for row in csv_reader:
            Passage, Metadata, Embeddings = row  
            
            metadata_dict = json.loads(Metadata)
            embeddings = json.loads(Embeddings)
            
            
            document = {
                "passage": Passage,
                "metadata": metadata_dict,
                "embedding": embeddings
            }
        
            es.index(index=index_name, body=document)
           

    # Refresh the index to make the data available for searching
    es.indices.refresh(index=index_name)
    # Check the document count in the index
    es.cat.count(index=index_name, format="json")


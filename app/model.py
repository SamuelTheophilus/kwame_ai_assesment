import json
import csv
import os
from logger import logging_setup
import logging
import traceback
from sentence_transformers import SentenceTransformer

model_name = "all-mpnet-base-v2"
model = SentenceTransformer(model_name)

logger = logging_setup(logging.DEBUG)
if __name__ == "__main__":
    ## Creating and storing embeddings for passages
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    passage_metadata_path = os.path.join(project_root, "docs", "passage_metadata.csv")

    try:
        logger.debug("Passing metadata, passage and calulated embeddings into csv")
        with open(passage_metadata_path, "r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            next(csv_reader, None)

            passage_metadata_emb_path = os.path.join(project_root, "docs", "passage_metadata_emb.csv")
            with open(passage_metadata_emb_path, "a", encoding="utf-8", newline='') as csv_file:
                headers = ["Passage", "Metadata", "Embeddings"]
                writer = csv.DictWriter(csv_file, fieldnames=headers)
                writer.writeheader()

                for row in csv_reader:
                    passage, metadata = row
                    embedding = model.encode(passage)
                    writer.writerow(
                        {"Passage": passage, "Metadata": metadata, "Embeddings": json.dumps(embedding.tolist())})
                    
        logger.info("Completed passing metadat, passage and calulated embeddings into csv")
    except Exception as e:
        logger.error(f"Error :: {str(e)}")
        logger.error(f"Error traceback :: {str(traceback.print_exc)}")



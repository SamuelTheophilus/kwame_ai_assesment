from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os
import json
from indexing import index_name, es
from model import model
from logger import logging_setup
import logging
import traceback


# Set up logging
logger = logging_setup(logging.DEBUG)

# Retrieve relevant passages
def retrieve_passages(index_name, question, top_k=3, model=model):
    query = {
        "query": {
            "match": {
                "passage": question
            }
        }
    }
    try:
        logger.debug(f"Fetching passages with query:: {query}")
        results = es.search(index=index_name, body=query, size=top_k)
        logger.info(f"Successfully fetched passages with query:: {query}")

    except Exception as e:
        logger.error(f"Error ::\n {str(e)}")
        logger.error(f"Error Occured while retrieving passages::\n {str(traceback.print_exc())}")

    question_embedding = model.encode(question)

    passages = []
    relevance_scores = []
    passage_metadata = []
    try:
        logger.debug("Formatting results into passages, scores and metadata")
        for hit in results["hits"]["hits"]:
            passages.append(hit["_source"]["passage"])
            relevance_scores.append(cosine_similarity([question_embedding], [hit["_source"]["embedding"]])[0][0])
            passage_metadata.append(hit["_source"]["metadata"])

        logger.info("Completed formatting results into passages, scores and metadata")
        return passages, relevance_scores, passage_metadata
    except Exception as e:
        logger.error(f"Error ::\n {str(e)}")
        logger.error(f"Error Occured while formatting results::\n {str(traceback.print_exc())}")


if __name__ == "__main__":
    try:
        logger.debug("Testing question retieval with an example")

        question = "What is a valid offer?"
        passages, relevance_scores, meta_data = retrieve_passages(index_name=index_name, question=question)
        csv_data = []
        results_df = pd.DataFrame({"Question": [question]})
        for i in range(len(passages)):
            results_df[f"Passage {i + 1}"] = passages[i],
            results_df[f"Relevance Score {i + 1}"] = relevance_scores[i],
            results_df[f"Passage {i + 1} Metadata"] = json.dumps(meta_data[i])


        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        question_answers_file = os.path.join(project_root, "docs", "question_answering.csv")
        results_df.to_csv(question_answers_file, index=False, encoding="utf-8")

        logger.info("Testing question retieval with an example completed successfully")
    except Exception as e:
        logger.error(f"Error ::\n {str(e)}")
        logger.error(f"Error Occured while testing retrieval results::\n {str(traceback.print_exc())}")

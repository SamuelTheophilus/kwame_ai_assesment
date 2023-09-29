from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os
import json
from indexing import index_name, es
from model import model
# Retrieve relevant passages
def retrieve_passages(index_name,question, top_k = 3, model = model):
    query = {
        "query": {
            "match": {
                "passage": question
            }
        }
    }

    results = es.search(index = index_name, body = query, size = top_k)

    question_embedding = model.encode(question)

    passages = []
    relevance_scores = []
    passage_metadata = []
    for hit in results["hits"]["hits"]:
        passages.append(hit["_source"]["passage"])
        relevance_scores.append(cosine_similarity([question_embedding], [hit["_source"]["embedding"]])[0][0])
        passage_metadata.append(hit["_source"]["metadata"])

    return passages, relevance_scores, passage_metadata

if __name__ == "__main__":
    print("Starting example")
    ## Example 
    question = "What is a valid offer?"
    passages, relevance_scores, meta_data = retrieve_passages(index_name = index_name, question=question)
    csv_data = []
    results_df = pd.DataFrame({"Question": [question]})
    for i in range(len(passages)):
        results_df[f"Passage {i+1}"] = passages[i],
        results_df[f"Relevance Score {i+1}"] =  relevance_scores[i],
        results_df[f"Passage {i+1} Metadata"] = json.dumps(meta_data[i])

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    question_answers_file = os.path.join(project_root, "docs", "question_answering.csv")
    results_df.to_csv(question_answers_file, index= False, encoding = "utf-8")
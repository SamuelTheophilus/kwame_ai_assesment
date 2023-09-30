import os
import csv
import pandas as pd
from logger import logging_setup
import logging
import traceback
from retrieval import retrieve_passages


logger = logging_setup(logging.DEBUG)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
user_quries_path = os.path.join(project_root, "Legal_Files", "user_queries.txt")
evaluation_path = os.path.join(project_root, "docs", "evaluation_rated.csv")
performance_path = os.path.join(project_root, "docs", "performance.csv")

def evaluation() -> None:
    try: 
        logger.debug("Fetching user_queries and retrieveing relevant passages")

        with open(user_quries_path, "r", encoding="utf-8") as queries_file:
            user_queries = queries_file.readlines()

        headers = ["Question",
                    "Passage 1",
                    "Relevance Score 1", 
                    "Passage 1 MetaData",
                    "Is Passage 1 Relevant? (Yes/No)",
                    "Passage 2",
                    "Relevance Score 2", 
                    "Passage 2 MetaData",
                    "Is Passage 2 Relevant? (Yes/No)",
                    "Passage 3",
                    "Relevance Score 3", 
                    "Passage 3 MetaData",
                    "Is Passage 3 Relevant? (Yes/No)"]
        
        for query in user_queries:
            passages, relevance_scores, metadata = retrieve_passages(query)
            if not os.path.exists(evaluation_path):
                with open(evaluation_path, "w", encoding="utf-8", newline= "") as eval_csv:
                    writer = csv.DictWriter(eval_csv , fieldnames= headers)
                    writer.writeheader()
            with open(evaluation_path, "a", encoding= "utf-8", newline="") as eval_csv:
                writer = csv.DictWriter(eval_csv, fieldnames=headers)
                writer.writerow ({
                            "Question": query,
                            "Passage 1": passages[0],
                            "Relevance Score 1": relevance_scores[0], 
                            "Passage 1 MetaData": metadata[0],
                            "Is Passage 1 Relevant? (Yes/No)": "",
                            "Passage 2": passages[1],
                            "Relevance Score 2": relevance_scores[1], 
                            "Passage 2 MetaData": metadata[1],
                            "Is Passage 2 Relevant? (Yes/No)": "",
                            "Passage 3": passages[2],
                            "Relevance Score 3": relevance_scores[2], 
                            "Passage 3 MetaData": metadata[2],
                            "Is Passage 3 Relevant? (Yes/No)": ""
                })
        logger.info("Passages for user queries retrieved with relevance scores and metadata")
    except Exception as e:
        logger.error(f"Error occured while evaluating user queries. {str(e)}")

def performance() -> None:
    try:
        logger.debug("Reading in evaluation csv")
        num_relevant_passages, top_one, top_three = 0, 0 ,0
        with open(evaluation_path, "r", encoding="utf-8") as eval_csv:
            evaluation_df = pd.read_csv(eval_csv)


        logger.debug("Calculating top one and top three accuracies")
        for index in range(1,4):
            for eval in evaluation_df[f"Is Passage {index} Relevant? (Yes/No)"]:
                # print(eval.lower())
                if eval.lower() == ("yes"): num_relevant_passages += 1
        
        top_one  = num_relevant_passages/1*100
        top_three =  num_relevant_passages/3 * 100

        with open(performance_path, "a", encoding="utf-8", newline="") as pf_file:
            headers = ["Top 1 Accuracy", "Top 3 Accuracy"]
            writer = csv.DictWriter(pf_file, fieldnames= headers)
            writer.writeheader()
            writer.writerow({"Top 1 Accuracy": top_one, 
                            "Top 3 Accuracy": f"{top_three:.2f}" # Formatting to two decimal places
                            })
        logger.info("Top one and Top three accuracies completed")
    except Exception as e:
        logger.error(f"Error occured while calculating. {str(e)}.\nMake sure you manually fill Is Passage (number) Relevant? (Yes/No) before running performance()")
        print(e)
        print(traceback.print_exc())
        print("Make sure you manually fill Is Passage (number) Relevant? (Yes/No) before running performance()")




if __name__ == "__main__":
    # Comment performance() when running evaluation() and vice versa
    # evaluation()
    performance() 
import json
import os
import nltk
import csv
nltk.download("punkt")

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
corpus_path = os.path.join(project_root, "Legal_Files", "Corpus")

files = os.listdir(corpus_path)
legal_passages = list(filter(lambda path: "Technical" in path, files))
legal_metadata = list(filter(lambda path: "Metadata" in path, files))


# Format all passages in append into an array
passage_data = []
for passage_file in legal_passages:
    with open(f"{corpus_path}/{passage_file}", 'r', encoding ="utf-8") as technical_file:
        lines = technical_file.readlines()
        sentences = filter(lambda x: x[0] != '_', lines)
    
    formatted_passage_file = ' '.join(word.strip() for word in sentences)
    passage_data.append(formatted_passage_file)


## Arrange each passage into chunks of five.
passage_chunks = []
for index, passage in enumerate(passage_data):
    split_passage , chunk_size, key_index = {}, 5, 0
    tokenized_sentence = nltk.sent_tokenize(passage)
    
    ## Convert each passage into chunks of five sentences
    for i in range(0, len(tokenized_sentence), chunk_size):
        grouped_sentence = ' '.join(tokenized_sentence[i:i+chunk_size])
        split_passage[f"Passage{key_index}"] = grouped_sentence
        key_index += 1
    
    ## Add each processed passage to passage_chunks
    passage_chunks.append(split_passage)


entire_metadata = []
for metadata_file in legal_metadata:
    with open(f"{corpus_path}/{metadata_file}", "r", encoding = "utf-8") as file:
        data = file.read()
    entire_metadata.append(data)


# Writing passages and metadata into passage_metadata.csv 
passage_metadata_path = os.path.join(project_root, "docs", "passage_metadata.csv")
with open(passage_metadata_path, "a", encoding = "utf-8") as csv_file:
    headers = ["Passage", "Metadata"]
    writer = csv.DictWriter(csv_file,fieldnames= headers)
    writer.writeheader()
    for metadata, chunks in zip(entire_metadata, passage_chunks):
        for chunk in list(chunks.values()):
            writer.writerow({ "Passage": chunk, "Metadata": metadata})

## Log over here when done.
print("Done")

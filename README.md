# Question and Answering System Interfaced with a Flask API

## This is an ML challenge project to build a system that answers legal questions based of information stored in an elasticsearch index.

The project sets up an elasticsearch instance and indexes legal documents into the a new index. It has two endpoints that allow the user to ask a legal question and retrieves passages, metadata and relevance scores as a response. It can be run in a virtual environment, or as a docker container.


## How to install and run project.
### - Using Virtual Env (Requirements: python 3.11 or higher, docker)
1. Create a virtual environment using pipenv, venv, or conda.
2. Clone the project into the virtual environment and activate.
3. Create a .env file and a logs/ directory in the root folder of the project.
    * In the .env file create an environemt variable(environment) and set it to either production, development, or testing for preferred configuration.
    * Create a logs file in the logs directory and name it logs.log
4. Run the command `pip install -r requirements.txt`
5. Navigate into the the [app/] directory and run the command `python parsing.py` or `python3 parsing.py`
6. Run the command `python model.py` or `python3 model.py`
7. Run the command `docker run --rm -p 9200:9200 -p 9300:9300 -e "xpack.security.enabled=false" -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.7.0` to start an elastic search instance.
8. Run the command `python indexing.py` or `python3 indexing.py`
9. Run the command `python retrieval.py` or `python3 retrieval.py` (You can view the output of this command in the docs/ directory in the question_answering.csv file)
10. Run the command `gunicorn -w 4 app:app` to start the flask app


### - Using a docker container.
1. Clone the project into a directory on a local machine.
2. Create a .env file and a logs/ directory in the root folder of the project.
    * In the .env file create an environemt variable(environment) and set it to either production, development, or testing for preferred configuration.
    * Create a logs file in the logs directory and name it logs.log
3. Navigate into the the [app/] directory and run the command `python parsing.py` or `python3 parsing.py`
4. Run the command `python model.py` or `python3 model.py`
5. Navigate into the docker/ directory and run the command `docker compose up`

## Testing.
### - Question
* Open an API testing tool, such as Postman/Insomnia
* Create a post request to the endpoint `http://localhost:8000/api/question` with a request body `{"question": your_question}`


### - File Upload
* Open an API testing tool, such as Postman/Insomnia
* Create a post request to the endpoint `http://localhost:8000/api/upload-document` with a request body `{"file": your_file}`
    - File uploads take only files with `.pdf` or `.txt` extenstions. 



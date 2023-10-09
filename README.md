# Question and Answering System Interfaced with a Flask API

## This is an ML challenge project to build a system that answers legal questions based of information stored in an elasticsearch index.

The project sets up an elasticsearch instance and indexes legal documents into the a new index. It has two endpoints that allow the user to ask a legal question and retrieves passages, metadata and relevance scores as a response. It can be run in a virtual environment, or as a docker container.


## How to install and run project.
1. Download the `docker-compose-dev.yml`
2. Run `docker compose -f 'path/to/docker-compose-dev.yml' up`
    * Wait for the container to start successfully, this is the message 'Connection Successful' appears on the terminal.


## Testing.
### - Question
* Open an API testing tool, such as Postman/Insomnia
* Create a post request to the endpoint `http://localhost:8000/api/question` with a request body `{"question": your_question}`


### - File Upload
* Open an API testing tool, such as Postman/Insomnia
* Create a post request to the endpoint `http://localhost:8000/api/upload-document` with a mutipart file request of  `{"file": your_file}`
    - File uploads take only files with `.pdf` or `.txt` extenstions. 



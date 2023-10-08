# Question and Answering System Interfaced with a Flask API

## This is an ML challenge project to build a system that answers legal questions based of information stored in an elasticsearch index.

The project sets up an elasticsearch instance and indexes legal documents into the a new index. It has two endpoints that allow the user to ask a legal question and retrieves passages, metadata and relevance scores as a response. It can be run in a virtual environment, or as a docker container.


## How to install and run project.
1. Run `docker pull samueltheophilus/kwame_ai_assessment` to download the image from dockerhub
2. Run `docker run samueltheophilus/kwame_ai_assessment` to spin a new container based on the image. 
    * Wait for the container to start successfully, this is the message 'Connected Successfully' appears on the terminal.


## Testing.
### - Question
* Open an API testing tool, such as Postman/Insomnia
* Create a post request to the endpoint `http://localhost:8000/api/question` with a request body `{"question": your_question}`


### - File Upload
* Open an API testing tool, such as Postman/Insomnia
* Create a post request to the endpoint `http://localhost:8000/api/upload-document` with a request body `{"file": your_file}`
    - File uploads take only files with `.pdf` or `.txt` extenstions. 



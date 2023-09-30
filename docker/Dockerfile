FROM python:3.11-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONONWRTIEBYTECODE 1

ENV PROJECT=/app
WORKDIR ${PROJECT}

RUN pip install --upgrade pip

COPY ../requirements.txt ${PROJECT}

RUN pip install -r requirements.txt

COPY .. ${PROJECT}

EXPOSE 80

CMD ["sh", "-c", "python ./app/app/parsing.py && python ./app/app/modelling.py && python ./app/app/indexing.py && python ./app/app/retrieval.py && python ./app/app/app.py"]
FROM python:3.11-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONONWRTIEBYTECODE 1

ENV PROJECT=/app
WORKDIR ${PROJECT}

RUN pip install --upgrade pip

COPY ../requirements.txt ${PROJECT}

RUN pip install -r requirements.txt

COPY ../scripts/wait-for-it.sh /usr/local/bin/wait-for-it.sh

RUN chmod +x /usr/local/bin/wait-for-it.sh

COPY .. ${PROJECT}

EXPOSE 8000

ENTRYPOINT ["wait-for-it.sh", "elasticsearch:9200", "--", "bash", "-c", "cd ./app && python indexing.py && python retrieval.py && gunicorn -w 4 app:app"]
FROM python:3.8-slim

ENV PORT 8080
ENV FLASK_APP yamaweb

WORKDIR /work
RUN pip install --no-cache-dir  poetry
COPY ./yamaweb/  /work/yamaweb
COPY ./pyproject.toml /work
COPY ./poetry.lock /work
WORKDIR /work
RUN poetry config virtualenvs.create false
RUN poetry install

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 'yamaweb:create_app()'

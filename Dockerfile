FROM python:3.6
ENV PYTHONBUFFERED 1

WORKDIR /deltai/

COPY Pipfile ./Pipfile
COPY Pipfile.lock ./Pipfile.lock

RUN pip install pipenv
RUN pipenv install --system

COPY . /deltai/

EXPOSE 3002


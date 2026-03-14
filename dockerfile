FROM python:3.13-slim

WORKDIR /IDF_test

COPY IDF_dbt /IDF_test/IDF_dbt
COPY src /IDF_test/src
COPY pyproject.toml /IDF_test/pyproject.toml

RUN pip3 install -e .

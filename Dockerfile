FROM python:3.6-slim

RUN mkdir /apflow
WORKDIR /apflow

# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt

COPY . .
RUN pip install -e '.[testing]'

LABEL maintainer="Nick Janetakis <nick.janetakis@gmail.com>"

CMD gunicorn --paste development.ini -b 0.0.0.0:6543

FROM python:3.11-bookworm

ENV PYTHONUNBUFFERED=1 

WORKDIR /app

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential python3-dev postgresql && \
    apt-get clean

COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt



#COPY ./web .
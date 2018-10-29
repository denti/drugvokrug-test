FROM ubuntu:16.04

ENV DEBIAN_FRONTEND noninteractive

# pip
RUN apt-get update
RUN apt-get -y install python-pip

# requirements
COPY requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

#RUN apt-get -y install vim
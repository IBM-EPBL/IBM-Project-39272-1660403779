# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /flask-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run"]

# FROM python:3.8-slim-buster
# RUN apt-get update
# RUN mkdir /app
# WORKDIR /app
# COPY . /app
# RUN pip install -r requirements.txt
# EXPOSE 5000
# ENTRYPOINT [ "python" ]
# CMD [ "app.py" ]
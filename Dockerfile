
FROM ubuntu:latest

WORKDIR /src
RUN apt update
RUN apt install python3-pip -y && pip3 install poetry

CMD ["python", "app.py"]

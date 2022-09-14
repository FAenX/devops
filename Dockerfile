FROM ubuntu:latest

WORKDIR /app
COPY . .

RUN apt update

# install python
RUN apt install -y python3 python3-pip


CMD ["python", "src/app.py"]


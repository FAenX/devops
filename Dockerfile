FROM ubuntu:20.04

WORKDIR /app
COPY . .

RUN apt update

# install python
RUN apt install --no-install-recommends python3.8 python3-pip -y
# install poetry
RUN pip3 install poetry


CMD ["python", "src/app.py"]


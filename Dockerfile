FROM ubuntu:20.04

WORKDIR /app
COPY . .

RUN apt update

# install python
RUN apt install --no-install-recommends python3.8 python3-pip -y \
    && ln -s /usr/bin/python3.8 /usr/bin/python 
    
# install poetry
RUN pip3 install poetry

USER root


CMD ["python3", "src/app.py"]


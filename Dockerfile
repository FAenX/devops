FROM ubuntu:20.04

WORKDIR /app
COPY . .

RUN apt update

# install python
RUN apt install --no-install-recommends python3.8 python3-pip python3-dev build-essential -y \
    && ln -s /usr/bin/python3.8 /usr/bin/python 
    
# install poetry
RUN pip3 install poetry

# add user and add them to sudoers
RUN useradd -ms /bin/bash user \
    && echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# install dependencies
RUN poetry config virtualenvs.in-project true \
    && poetry export -f requirements.txt --output requirements.txt \
    && pip3 install -r requirements.txt 

# USER user
USER root


CMD ["python3", "src/app.py"]


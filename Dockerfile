FROM ubuntu:20.04

RUN apt update

# install python
RUN apt install --no-install-recommends python3.8 python3-pip python3-dev build-essential -y \
    && ln -s /usr/bin/python3.8 /usr/bin/python 


WORKDIR /app
COPY . .

# install dependencies
RUN pip install poetry \
    && poetry export -f requirements.txt --output requirements.txt \
    && pip install -r requirements.txt 

CMD ["python", "src/app.py"]


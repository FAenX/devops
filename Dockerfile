FROM python:3.8.13-buster

WORKDIR /app
COPY . .

RUN pip install poetry --cache-dir=.pip; \
    poetry export -f requirements.txt  -o requirements.txt --without-hashes; \
    pip install -r requirements.txt --cache-dir=.pip ; 

CMD ["python", "src/app.py"]


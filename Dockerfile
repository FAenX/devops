FROM ubuntu:latest

RUN apt-get update && apt-get install -y curl vim wget software-properties-common ssh net-tools ca-certificates python3 python3-pip
RUN pip install poetry

RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1

COPY . .

RUN pip install flask 

CMD ["python", "src/app.py"]


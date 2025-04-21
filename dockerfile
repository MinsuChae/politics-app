FROM ubuntu:22.04

RUN apt-get update && apt-get install -y  python3 python3-pip git openssl

WORKDIR /app
RUN git clone https://github.com/MinsuChae/politics-app.git /app

RUN pip3 install -r requirements.txt

RUN echo SECRET_KEY=$(openssl rand -hex 32) > .env

CMD ["python3", "app.py"]
FROM python:3.7-alpine3.7
LABEL maintainer="linlanxi7552659@gmail.com"
ENV host="127.0.0.1"
ENV port="8080"
ENV username="admin"
ENV password="123456"
ENV token="111111111:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
COPY . /opt/bot
WORKDIR /opt/bot
RUN  apk --no-cache --virtual build  add build-base libffi-dev openssl-dev && pip install pipenv && pipenv install && rm -rf ~/.pip/ && apk del build 
CMD ["pipenv","run", "python", "run.py"]


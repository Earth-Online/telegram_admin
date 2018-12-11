FROM python:3.6.7-alpine3.7
LABEL maintainer="linlanxi7552659@gmail.com"
ENV host="127.0.0.1"
ENV port="8080"
ENV token="111111111:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
COPY . /opt/bot
WORKDIR /opt/bot
RUN  apk --no-cache --virtual build  add build-base libffi-dev openssl-dev && pip install -r requirements.txt && rm -rf ~/.pip/ && apk del build 
CMD ["python","run.py"]


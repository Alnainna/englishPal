FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
COPY requirements.txt /tmp
COPY ./app/ /app/
RUN pip3 install -U pip -i https://mirrors.aliyun.com/pypi/simple/
RUN pip3 install -r /tmp/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

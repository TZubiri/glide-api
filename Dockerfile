FROM python:3.8-slim-buster

ADD requirements.txt /src/requirements.txt

RUN pip3 install -r /src/sudrequirements.txt

ADD . /src/.

ENTRYPOINT python3 /src/app.py
FROM python:3.8-slim-buster

#RUN pip3 install -r /src/requirements.txt

#Not using requirements.txt to improve development caching for Docker build. If an external tool needs requirements.txt,
# we can switch to it later at the expense of redownloading the packages.
RUN pip3 install flask
RUN pip3 install requests

ADD . /src/.

ENTRYPOINT python3 /src/app.py
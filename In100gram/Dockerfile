FROM python:3.10


COPY ./in100gram/requirements.txt /temp/requirements.txt
COPY in100gram /in100gram

WORKDIR /in100gram

EXPOSE 8000:8000

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password in100gram-user

USER in100gram-user

FROM python:slim

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD python flask_luma_app.py

EXPOSE 5000
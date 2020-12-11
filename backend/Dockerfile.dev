FROM python:3.6.10

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
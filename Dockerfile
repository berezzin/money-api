FROM python:3.10

RUN mkdir 'money_app'

WORKDIR /money_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
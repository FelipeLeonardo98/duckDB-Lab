FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install duckdb
RUN pip install requests
# RUN pip install -r requirements.txt


CMD [ "python", "main.py"]
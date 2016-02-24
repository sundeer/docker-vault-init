FROM python:3.5

RUN apt-get update && apt-get install gnupg

ADD . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app/app

ENTRYPOINT ["python3", "main.py"]

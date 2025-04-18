FROM python:3.13.3-alpine

WORKDIR /safe-chat

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . app

CMD [ "fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0" ]

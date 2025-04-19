FROM python:3.13.3-alpine

WORKDIR /safe-chat

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . bot

CMD ["python", "bot/main.py"]
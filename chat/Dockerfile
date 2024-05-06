# Dockerfile
FROM python:3.11

WORKDIR /rentafriend-chat

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8001

COPY app/ ./app/
CMD [ "uvicorn", "chat.chat_server:app", "--port", "8001", "--host", "0.0.0.0" ]
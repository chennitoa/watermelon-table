# Dockerfile
FROM python:3.11

WORKDIR /rentafriend-backend

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000

COPY app/ ./app/
CMD [ "uvicorn", "app.main:app", "--port", "5000", "--host", "0.0.0.0" ]
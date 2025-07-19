FROM python:3.10-slim

WORKDIR /app

copy requirements.txt requirements.txt

RUN pip install -r requirements.txt

copy . .

CMD ["python3", "app.py"]

# docker build -t flask .
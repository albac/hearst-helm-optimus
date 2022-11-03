FROM python:3.10-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY prime.py .

EXPOSE 5000

ENTRYPOINT [ "python", "./prime.py"]


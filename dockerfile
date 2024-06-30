FROM --platform=linux/amd64 python:3.8-slim-buster as build 


WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py /app/
COPY index.html /app/
COPY style.css /app/
COPY script4.js /app/ 

EXPOSE 5200

# Mount the persistent volume
VOLUME ["/data"]


CMD ["python", "app.py"]
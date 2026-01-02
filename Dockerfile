FROM python:3.9-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    --default-timeout=100 \
    -r requirements.txt

COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]

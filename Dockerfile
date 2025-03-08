FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
RUN ["python","gen_secret_key.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

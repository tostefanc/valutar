FROM python:3.9-slim
WORKDIR /usr/valutar
COPY ./ ./
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "main.py"]
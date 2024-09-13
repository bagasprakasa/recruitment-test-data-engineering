FROM python:3.8-slim
WORKDIR /app
COPY ./data /app/data
COPY ./load_data.py /app/load_data.py
RUN pip install mysql-connector-python pandas
CMD ["python", "load_data.py"]
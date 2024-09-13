FROM python:3.8-slim
WORKDIR /app
COPY ./output_summary.py /app/output_summary.py
RUN pip install mysql-connector-python
CMD ["python", "output_summary.py"]
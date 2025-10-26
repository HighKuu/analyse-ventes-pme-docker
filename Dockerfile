FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install requests pandas
CMD python hello.py && python import_data.py && python analyses.py


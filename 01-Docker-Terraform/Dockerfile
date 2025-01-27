FROM python:3.9

RUN pip install pandas sqlalchemy pyarrow psycopg2-binary

WORKDIR /app

COPY pipeline.py pipeline.py

ENTRYPOINT [ "python","pipeline.py" ]
FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app

COPY ./checkpoints /code/checkpoints

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "${PORT}"]
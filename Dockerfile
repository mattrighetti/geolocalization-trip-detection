FROM python:3.6.9-stretch

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENV PYTHONPATH="."

RUN pytest

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
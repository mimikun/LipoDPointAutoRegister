FROM python:alpine

WORKDIR /home/

COPY src/Pipfile src/Pipfile.lock ./

RUN pip install pipenv --no-cache-dir
RUN pipenv install --system

COPY src/main.py ./

CMD ["python main.py"]

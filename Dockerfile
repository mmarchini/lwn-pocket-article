FROM python:3

WORKDIR /lwn-pocket-article
COPY . /lwn-pocket-article

RUN pip install --no-cache-dir --trusted-host pypi.python.org pipenv && \
    pipenv install

ENTRYPOINT ["pipenv", "run", "python", "entrypoint.py"]

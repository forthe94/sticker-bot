FROM python:3.11.4

WORKDIR /app
ENV PATH=/root/.local/bin:$PATH \
    PYTHONPATH=/app

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main
RUN python3 -m pip install setuptools --upgrade

COPY . .

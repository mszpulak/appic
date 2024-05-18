FROM python:3.11-bookworm as build

RUN pip install --no-cache-dir poetry==1.4.2

COPY pyproject.toml poetry.lock ./

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

ENV VIRTUAL_ENV=/.venv \
    PATH="/.venv/bin:$PATH"

RUN poetry install --no-root --no-cache

FROM python:3.11-slim-bookworm as runtime

ENV VIRTUAL_ENV=/.venv \
    PATH="/.venv/bin:$PATH"

COPY --from=build ${VIRTUAL_ENV} ${VIRTUAL_ENV}

RUN mkdir -p /appic/
COPY ./appic/ /appic/
WORKDIR /appic/
EXPOSE 8000


FROM runtime as web
CMD ["python", "manage.py","runserver"]
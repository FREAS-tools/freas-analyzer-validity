FROM python:3.10-slim as base

WORKDIR /app

FROM base as build

ENV POETRY_VERSION=1.7.0

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock README.md ./
COPY src ./src

RUN poetry config virtualenvs.in-project true && \
    poetry build

FROM base as final

COPY --from=build /app/dist .
COPY --from=build /app/src ./src
RUN pip install *.whl

EXPOSE 5000
CMD ["uvicorn", "src.api.api:app", "--host", "0.0.0.0", "--port", "5000"]
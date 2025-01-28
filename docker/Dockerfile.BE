FROM python:3.10.11

ARG SECRET_KEY
ARG DATABASE_URL
ARG DB_HOST
ARG DB_USER
ARG DB_PASSWORD
ARG DB_PORT
ARG DB_NAME
ARG CORPY_FRONTEND

ENV SECRET_KEY=${SECRET_KEY}
ENV DATABASE_URL=${DATABASE_URL}
ENV DB_HOST=${DB_HOST}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_PORT=${DB_PORT}
ENV DB_NAME=${DB_NAME}
ENV CORPY_FRONTEND=${CORPY_FRONTEND}

RUN mkdir app
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY ./backend/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# for migrations
COPY ./backend/migrations .
COPY ./backend/pyproject.toml .

COPY ./backend/src ./src

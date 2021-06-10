FROM python:3.7.9-slim-buster as builder

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

FROM python:3.7.9-slim-buster

# create the appropriate directories
RUN mkdir -p /srv/app/
RUN addgroup --system app && adduser --system --group app
ENV HOME=/srv/app
WORKDIR $HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# add app
COPY site_checker .
COPY scripts/*.sh .

# chown all the files to the app user
RUN chown -R app:app $HOME

# change to the app user
USER app

FROM python:3.8-slim-buster

ARG BUILD_ENV=production

# set env variable for the python
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/${BUILD_ENV}.txt

# copy entrypoint.sh into image
COPY ./compose/flask_app/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./compose/flask_app/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

COPY . /app

WORKDIR /app

ENTRYPOINT [ "/entrypoint.sh" ]
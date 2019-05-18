# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.7

RUN pip install pipenv

COPY Pipfile /
COPY Pipfile.lock /

RUN pipenv install --dev --system --deploy

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Remove --reload in production.
CMD pipenv run gunicorn --reload --bind :$PORT --workers 1 --threads 8 app:app
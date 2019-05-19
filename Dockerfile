FROM python:3.7

RUN pip install pipenv

COPY Pipfile /
COPY Pipfile.lock /
COPY .pylintrc /

RUN pipenv install --dev --system --deploy

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
CMD pipenv run gunicorn --reload --bind :$PORT --workers 3 --threads 1 --log-level=debug app:app
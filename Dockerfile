FROM gcr.io/uwit-mci-axdd/django-container:1.3.7 as app-container

USER root
RUN apt-get update && apt-get install mysql-client libmysqlclient-dev vim -y
USER acait

ADD --chown=acait:acait catalyst_utils/VERSION /app/catalyst_utils/
ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/
RUN . /app/bin/activate && pip install -r requirements.txt

RUN . /app/bin/activate && pip install mysqlclient

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ project/

RUN . /app/bin/activate && python manage.py collectstatic --noinput

FROM gcr.io/uwit-mci-axdd/django-test-container:1.3.7 as app-test-container

COPY --from=app-container /app/ /app/
COPY --from=app-container /static/ /static/

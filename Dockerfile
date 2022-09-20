
FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /project
ADD /project /project

RUN pip install -r requirements.txt

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

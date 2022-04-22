FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get -y install cron && apt-get -y install vim

RUN pip install -r requirements.txt

RUN pip install psycopg2-binary==2.9.2

EXPOSE 5002

COPY hello-cron /etc/cron.d/hello-cron

RUN chmod 0644 /etc/cron.d/hello-cron

RUN crontab /etc/cron.d/hello-cron

RUN touch /var/log/cron.log

RUN mkdir /app/log

CMD cron && tail -f /var/log/cron.log

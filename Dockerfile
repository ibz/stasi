FROM debian:buster-slim

RUN apt-get update && apt-get install -y cron python3-rrdtool rsync ssh sudo

COPY scripts /scripts

RUN useradd -m stasi
RUN mkdir -p /home/stasi/.ssh
RUN chown -R stasi:stasi /home/stasi/.ssh

COPY stasi-cron /etc/cron.d/stasi-cron
RUN chmod 0644 /etc/cron.d/stasi-cron && crontab /etc/cron.d/stasi-cron
RUN touch /var/log/cron.log
RUN echo 'stasi ALL=NOPASSWD: /usr/sbin/cron' >> /etc/sudoers

USER stasi

CMD sudo cron && tail -f /var/log/cron.log


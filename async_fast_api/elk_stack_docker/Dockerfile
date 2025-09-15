FROM docker.elastic.co/beats/filebeat:8.5.1
USER root
COPY filebeat.yml /usr/share/filebeat/filebeat.yml
RUN chmod 600 /usr/share/filebeat/filebeat.yml
USER filebeat

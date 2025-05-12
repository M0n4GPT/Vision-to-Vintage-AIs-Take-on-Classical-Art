FROM prom/prometheus:latest

COPY prometheus.yml /etc/prometheus/prometheus.yml

USER root
RUN chown -R nobody:nogroup /etc/prometheus
USER nobody 
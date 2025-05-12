FROM grafana/grafana:latest

COPY grafana.ini /etc/grafana/grafana.ini
COPY provisioning/datasources/prometheus.yml /etc/grafana/provisioning/datasources/
COPY provisioning/dashboards/dashboards.yml /etc/grafana/provisioning/dashboards/
COPY provisioning/dashboards/style_transfer.json /etc/grafana/provisioning/dashboards/

USER root
RUN chown -R grafana:grafana /etc/grafana/provisioning
USER grafana 
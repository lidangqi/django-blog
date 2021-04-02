FROM elasticsearch:7.12.0

COPY ./docker-compose/production/elasticsearch/elasticsearch-analysis-ik-7.12.0.zip /usr/share/elasticsearch/plugins/
RUN cd /usr/share/elasticsearch/plugins/ && mkdir ik && unzip elasticsearch-analysis-ik-7.12.0.zip -d ik/
RUN rm /usr/share/elasticsearch/plugins/elasticsearch-analysis-ik-7.12.0.zip

USER root
COPY ./docker-compose/production/elasticsearch/elasticsearch.yml /usr/share/elasticsearch/config/
RUN chown elasticsearch:elasticsearch /usr/share/elasticsearch/config/elasticsearch.yml

USER elasticsearch
FROM postgres:11

ENV POSTGRES_USER postgres_docker
ENV POSTGRES_PASSWORD dockerPass
ENV POSTGRES_DB db_vacancies

ADD CreateDB.sql /docker-entrypoint-initdb.d/

RUN echo "host all  all    0.0.0.0/0  md5" >> /usr/share/postgresql/pg_hba.conf
RUN echo "listen_addresses='*'" >> /usr/share/postgresql/postgresql.conf
EXPOSE 5432
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

#CMD ["/usr/lib/postgresql/11/bin/postgres", "-D", "/var/lib/postgresql/11/main", "-c", "config_file=/etc/postgresql/11/main/postgresql.conf"]

FROM ubuntu:latest

RUN apt-get update && apt-get install -y gnupg2

# sign the following postgresql repository
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8

# please, check the name of the latest version of ubuntu (change 'bionic' if it's not the latest)
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main" > /etc/apt/sources.list.d/pgdg.list

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common postgresql-11

USER postgres

RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER postgres_docker WITH SUPERUSER PASSWORD 'dockerPass';" &&\
    psql --command "CREATE DATABASE db_vacancies;" && \
    psql --command "GRANT ALL PRIVILEGES ON DATABASE db_vacancies TO postgres_docker;" && \
    psql -l
# now db_vacancies is a name of a database owned by postgres_docker

#add access from all ip addresses
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/11/main/pg_hba.conf

#listen to all addresses
RUN echo "listen_addresses='*'" >> /etc/postgresql/11/main/postgresql.conf

#expose the port to the outside world
EXPOSE 5432

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# RUN psql --command "\c postgres_docker" && psql --command "CREATE TABLE vacancies (id int, name varchar(60));"

ADD create_user.sh /

USER root

RUN ./create_user.sh

USER postgres

#
#RUN /usr/lib/postgresql/11/bin/postgres -D /var/lib/postgresql/11/main -c config_file=/etc/postgresql/11/main/postgresql.conf
#
#USER postgres_docker
#
#RUN psql --command "CREATE TABLE vacancies (id int, name varchar(60));"

# Set the default command to run when starting the container (is overwritten if pass any command with "docker run ... command")
CMD ["/usr/lib/postgresql/11/bin/postgres", "-D", "/var/lib/postgresql/11/main", "-c", "config_file=/etc/postgresql/11/main/postgresql.conf"]

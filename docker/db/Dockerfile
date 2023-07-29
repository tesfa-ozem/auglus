FROM postgres:13
LABEL maintainer="Hide <padocon@naver.com>"

# Optionally, if you want to initialize the PostgreSQL database with custom scripts,
# place your SQL scripts in the "docker-entrypoint-initdb.d" directory. The scripts
# in this directory will be executed when the container starts for the first time.
#ADD ./postgres-init-scripts /docker-entrypoint-initdb.d

ENV POSTGRES_DB=taskdb
ENV POSTGRES_USER=tesfa
ENV POSTGRES_PASSWORD=admin
EXPOSE 5432

CMD ["postgres"]

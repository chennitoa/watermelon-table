# Dockerfile
FROM mysql:latest

COPY setup.sql /docker-entrypoint-initdb.d/

CMD ["mysqld"]
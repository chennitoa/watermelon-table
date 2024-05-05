# Dockerfile
FROM mysql:latest as release

COPY 00-setup.sql /docker-entrypoint-initdb.d/

# Test build
FROM release as debug

COPY 01-populate_tables.sql /docker-entrypoint-initdb.d/

CMD ["mysqld"]
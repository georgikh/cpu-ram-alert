#FROM - this directive is used to identify the image from which we want to build the new image.
# I choose postgres:latest which is the official Docker Image with the tag latest that indicates the latest version (13).

FROM postgres:latest

# with this directive, we are able to specify various environment variables. 
# For this image I specified POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_DB
ENV POSTGRES_PASSWORD=secret
ENV POSTGRES_USER=someuser
ENV POSTGRES_DB=alertdb
COPY create_fixtures.sql /docker-entrypoint-initdb.d/create_fixtures.sql
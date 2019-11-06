# Proj name
Pull the repository with

``

## Build PostgreSQL Docker
To build PostgreSQL Docker (from PostgreSQL-Docker direcrory):
*Please, be noticed that in the Dockerfile the current latest version of ubuntu is bionic. Edit the Dockerfile according to your current situation.*

`$ docker build -t your-dockerImage-name .`

Run an instance of the docker image you have just created

`docker run --rm -P --name PostgreSQL-Docker your-dockerImage-name`

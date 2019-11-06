# Monitor open vacancies with headhunter API
This project aims to store open vacancies to the PostgreSQL database in a docker container. If a vacancy is no longer present at the website it's marked as 'closed' in the database. Monitoring is issued once per 24 hours.

## Build containers with docker-compose
Pull the repository with

`git clone https://github.com/undadasea/headhunter-monitor.git`

*Please, be noticed that in the Dockerfile of PostgreSQL-Docker the current latest version of ubuntu is bionic. Edit the Dockerfile according to your current situation.*

For Linux OS:

`$ cd website-monitoring`

`$ sudo apt-get install docker-compose`

`$ docker-compose build`

`$ docker-compose up`

If you change any file you should start with "build" command again.

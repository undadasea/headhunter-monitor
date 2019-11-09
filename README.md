# Monitor open vacancies with headhunter API
This project aims to store open vacancies to the PostgreSQL database in a docker container. If a vacancy is no longer present at the website it's marked as 'closed' in the database. Monitoring is issued once per 24 hours.

## Build containers with docker-compose
Pull the repository with
```
git clone https://github.com/undadasea/headhunter-monitor.git
```
*Please, be noticed that in the Dockerfile of PostgreSQL-Docker the current latest version of ubuntu is bionic. Edit the Dockerfile according to the current situation.*

For GNU/Linux OS:
```
$ cd website-monitoring
$ sudo apt-get install docker-compose
$ docker-compose build
$ docker-compose up
```

To delete or rebuild:
```
$ docker-compose rm  
```
after finishing working with containers.

If you change any file you should start with "build" command again. It's possible that you may need to delete previously created images, containers and networks if some problem occurs. Try:
```
$ docker system prune
```

or delete images, containers and networks manually with:

```
$ docker ps -a
$ docker rm ID_or_Name
```

```
$ docker images -a
$ docker rmi image
```

```
$ docker network ls
$ docker network rm net_name
```

To set a scheduled monitoring work you should set a daemon as:
```
$ echo "02 15	* * *	root    docker-compose -f /path/to/website-monitoring/docker-compose.yml" >> /etc/crontab
```

PostgreSQL-Docker continues working after Application-Docker finishes its work. You can stop the PostgreSQL-Docker at this point.

To enter the docker while it's running you can use:
```
$ docker ps
$ docker exec -it <ID container> bash
root@<ID container>:/# psql -h localhost -p 5432 -U postgres_docker -d db_vacancies
```

Table vacancies example:

```
name                                                                                             |   job    | developer_experience
-------------------------------------------------------------------------------------------------+----------+----------------------
Manual QA engineer                                                                               | engineer | No Match
Менеджер по работе с клиентами (м. Садовая, набережная реки Фонтанки)                            | manager  | No Match
Специалист по тестированию/Manual QA                                                             | No Match | No Match
Контент-менеджер                                                                                 | manager  | No Match
Менеджер B2B продаж в IT (AR/VR/MR)                                                              | manager  | No Match
HR-менеджер                                                                                      | manager  | No Match
Таргетолог социальных медиа (Social Advertising Manager)                                         | manager  | No Match
Менеджер по работе с клиентами (м. Проспект Ветеранов, проспект Ветеранов)                       | manager  | No Match
Руководитель портала                                                                             | engineer | No Match
Офис-менеджер/Помощник бухгалтера                                                                | manager  | No Match
IT рекрутер                                                                                      | engineer | middle
Веб-дизайнер / UI UX дизайнер - в студию                                                         | No Match | No Match
Оператор call-центра                                                                             | No Match | No Match
Software testing engineer (BI, ETL, DB)                                                          | engineer | No Match
Менеджер по работе с клиентами (м. Проспект Ветеранов, ул. Доблести)                             | manager  | No Match
Web-дизайнер ⁢/ Веб-дизайнер                                                                      | No Match | No Match
IOS разработчик                                                                                  | engineer | middle
```

CREATE TABLE vacancies (id int not null,
                        name varchar(60),
                        premium boolean,
                        has_test boolean,
                        letter_required boolean,
                        salary_from int,
                        salary_to int,
                        currency varchar(10),
                        type varchar(30),
                        employer_id int not null,
                        address_id int,
                        created time,
                        published time,
                        requirements text,
                        responsibilities text,
                        contact_id int,
                        last_update time
                       );

CREATE TABLE employers (id int not null,
                        name varchar(60),
                        address_id int,
                        contact_id int
                       );

CREATE TABLE addresses (id serial unique,
                        city varchar(20),
                        street varchar(50),
                        building varchar(10),
                        metro varchar(30),
                        employer_id int
                       );

CREATE TABLE contact_person (id serial unique,
                             name varchar(40),
                             employer_id int,
                             email varchar(40),
                             phone varchar(15)
                            );

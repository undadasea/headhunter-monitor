CREATE TABLE vacancies (id int not null,
                        name varchar(60),
                        premium boolean,
                        has_test boolean,
                        letter_required boolean,
                        salary_from int,
                        salary_to int,
                        currency varchar(10),
                        gross boolean,
                        type varchar(30),
                        employer_id int not null,
                        address_id int,
                        created_at time,
                        published_at time,
                        requirement text,
                        responsibility text,
                        contact_id int,
                        last_update time
                       );

CREATE TABLE employers (id int not null,
                        name varchar(60),
                        address_id int,
                        contact_id int
                       );

CREATE TABLE addresses (id serial unique,
                        address text,
                        metro varchar(30),
                        employer_id int
                       );

CREATE TABLE contact_person (id serial unique,
                             name varchar(40),
                             employer_id int,
                             email varchar(40),
                             phone varchar(15),
                             comment varchar(60)
                            );

CREATE TABLE vacancies (id int unique not null,
                        name text,
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
                        created_at timestamptz,
                        published_at timestamptz,
                        requirement text,
                        responsibility text,
                        contact_id int,
                        last_update timestamptz,
                        job varchar(10),
                        developer_experience varchar(10)
                       );

CREATE TABLE employers (id int CONSTRAINT id_constr UNIQUE,
                        name text
                       );

CREATE TABLE addresses (id serial unique,
                        address text,
                        metro varchar(30),
                        employer_id int
                       );

CREATE TABLE contact_person (id serial unique,
                             name text,
                             employer_id int,
                             email text,
                             phone text,
                             comment text
                            );

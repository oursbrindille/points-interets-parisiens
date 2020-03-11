-- DROP TABLE dvf;
CREATE TABLE evenement
(
	id_event SERIAL PRIMARY KEY NOT NULL,
    evenement CHARACTER VARYING,
    startYear DECIMAL(9,2),
    endYear DECIMAL(9,2),
    commentaire CHARACTER VARYING,
    prod CHARACTER VARYING
)
TABLESPACE pg_default;

CREATE TABLE personnage
(
	id_personnage SERIAL PRIMARY KEY NOT NULL,
    wikiID CHARACTER VARYING,
    nom CHARACTER VARYING,
    dateOfBirth date default NULL,
    placeOfBirthLabel CHARACTER VARYING,
    dateOfDeath date default NULL,
    placeOfDeathLabel CHARACTER VARYING,
    mannersOfDeath CHARACTER VARYING,
    placeOfBurialLabel CHARACTER VARYING,
    fatherLabel CHARACTER VARYING,
    motherLabel CHARACTER VARYING,
    spouses CHARACTER VARYING,
    startTime date default NULL,
    endTime date default NULL,
    startYear DECIMAL(9,2) default NULL,
    endYear DECIMAL(9,2) default NULL,
    birthYear DECIMAL(9,2) default NULL,
    deathYear DECIMAL(9,2) default NULL,
    urlImage CHARACTER VARYING,
    cat CHARACTER VARYING,
    prod CHARACTER VARYING
)
TABLESPACE pg_default;

CREATE TABLE lieu
(
	id_lieu SERIAL PRIMARY KEY NOT NULL,
    nom CHARACTER VARYING,
    lon NUMERIC(14, 11),
    lat NUMERIC(14, 11),
    inception CHARACTER VARYING,
    height DECIMAL(9,2),
    constructionYear DECIMAL(9,2),
    prod CHARACTER VARYING
)
TABLESPACE pg_default;


CREATE TABLE objet
(
	id_objet SERIAL PRIMARY KEY NOT NULL,
    nom CHARACTER VARYING,
    startYear DECIMAL(9,2) default NULL,
    endYear DECIMAL(9,2) default NULL,
    urlImage CHARACTER VARYING,
    prod CHARACTER VARYING
)
TABLESPACE pg_default;


CREATE TABLE instance_object
(
	id_instance_object SERIAL PRIMARY KEY NOT NULL,
    id_external_object CHARACTER VARYING,
    type_object CHARACTER VARYING,
    lon NUMERIC(14,11),
    lat NUMERIC(14,11)
)
TABLESPACE pg_default;


CREATE TABLE instance_object_user
(
	id_instance_object_user SERIAL PRIMARY KEY NOT NULL,
    id_external_object CHARACTER VARYING,
    id_user CHARACTER VARYING,
    type_object CHARACTER VARYING,
    lon NUMERIC(14,11),
    lat NUMERIC(14,11)
)
TABLESPACE pg_default;


CREATE TABLE user_info
(
	id_user SERIAL PRIMARY KEY NOT NULL,
    pseudo CHARACTER VARYING
)
TABLESPACE pg_default;
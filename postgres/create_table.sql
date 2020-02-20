-- DROP TABLE dvf;
CREATE TABLE evenement
(
	id_event SERIAL PRIMARY KEY NOT NULL,
    evenement CHARACTER VARYING,
    startYear DECIMAL(9,2),
    endYear DECIMAL(9,2),
    commentaire CHARACTER VARYING
)
TABLESPACE pg_default;

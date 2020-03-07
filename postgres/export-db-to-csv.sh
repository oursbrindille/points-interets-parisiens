sudo chown -R postgres:postgres /home/geof/projects/monuments-paris/csv/postgres/
sudo -u postgres psql -d paris -c "\copy evenement(evenement, startYear, endYear, commentaire, prod) TO '/home/geof/projects/monuments-paris/csv/postgres/evenement.csv' DELIMITER ',' CSV HEADER;"
sudo -u postgres psql -d paris -c "\copy personnage(wikiID, nom, dateOfBirth, placeOfBirthLabel, dateOfDeath, placeOfDeathLabel, mannersOfDeath, placeOfBurialLabel, fatherLabel, motherLabel, spouses, startTime, endTime, startYear, endYear, birthYear, deathYear,urlImage, prod) TO '/home/geof/projects/monuments-paris/csv/postgres/personnage.csv' DELIMITER ',' CSV HEADER;"
sudo -u postgres psql -d paris -c "\copy lieu(nom, lon, lat, inception, height, constructionYear, prod) TO '/home/geof/projects/monuments-paris/csv/postgres/lieu.csv' DELIMITER ',' CSV HEADER;"
sudo -u postgres psql -d paris -c "\copy objet(nom, startYear, endYear, urlImage, prod) TO '/home/geof/projects/monuments-paris/csv/postgres/objet.csv' DELIMITER ',' CSV HEADER;"
sudo -u postgres psql -d paris -c "\copy user_info(pseudo) TO '/home/geof/projects/monuments-paris/csv/postgres/user.csv' DELIMITER ',' CSV HEADER;"
sudo chown -R geof:geof /home/geof/projects/monuments-paris/csv/postgres/

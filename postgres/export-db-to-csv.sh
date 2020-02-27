sudo chown -R postgres:postgres /home/geof/projects/monuments-paris/csv/postgres/
sudo -u postgres psql -d paris -c "\copy evenement(evenement, startYear, endYear, commentaire) TO '/home/geof/projects/monuments-paris/csv/postgres/evenement.csv' DELIMITER ',' CSV HEADER;"
sudo -u postgres psql -d paris -c "\copy roi(wikiID, nom, dateOfBirth, placeOfBirthLabel, dateOfDeath, placeOfDeathLabel, mannersOfDeath, placeOfBurialLabel, fatherLabel, motherLabel, spouses, startTime, endTime, startYear, endYear, birthYear, deathYear) TO '/home/geof/projects/monuments-paris/csv/postgres/roi.csv' DELIMITER ',' CSV HEADER;"
sudo -u postgres psql -d paris -c "\copy lieu(nom, lon, lat, inception, height, constructionYear) TO '/home/geof/projects/monuments-paris/csv/postgres/lieu.csv' DELIMITER ',' CSV HEADER;"
sudo -u postgres psql -d paris -c "\copy personnage(nom, dateOfBirth, placeOfBirthLabel, dateOfDeath, placeOfDeathLabel, positions, birthYear, deathYear) TO '/home/geof/projects/monuments-paris/csv/postgres/personnage.csv' DELIMITER ',' CSV HEADER;"
sudo chown -R geof:geof /home/geof/projects/monuments-paris/csv/postgres/

sudo -u postgres psql -d paris -c "\copy evenement TO '/home/geof/projects/monuments-paris/csv/postgres/evenement.csv' DELIMITER ',' CSV HEADER;"
sudo -u postgres psql -d paris -c "\copy roi TO '/home/geof/projects/monuments-paris/csv/postgres/roi.csv' DELIMITER ',' CSV HEADER;"
sudo -u postgres psql -d paris -c "\copy lieu TO '/home/geof/projects/monuments-paris/csv/postgres/lieu.csv' DELIMITER ',' CSV HEADER;"
sudo -u postgres psql -d paris -c "\copy personnage TO '/home/geof/projects/monuments-paris/csv/postgres/personnage.csv' DELIMITER ',' CSV HEADER;"


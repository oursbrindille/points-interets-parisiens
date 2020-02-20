sudo -u postgres psql -c "DROP DATABASE IF EXISTS paris;"
sudo -u postgres psql -c "CREATE DATABASE paris;"
sudo -u postgres psql -d paris -f "create_table.sql"
sudo -u postgres psql -d paris -c "\copy evenement(evenement, startYear, endYear, commentaire) FROM '/home/geof/projects/monuments-paris/csv/concat/evenements-paris.csv' delimiter ',' csv header encoding 'UTF8';"
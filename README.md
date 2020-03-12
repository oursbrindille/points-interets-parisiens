# Résumé

Plusieurs éléments :
- jupyter notebook dans le dossier notebooks ==> Sert à récupérer les données et à les modifier
- Dossier backend pour le backend (en Flask)
- Dossier frontend pour le frontend (en ReactJS)

## Mise en route :

0. sudo service postgresql start
1. cd backend
2. python app.py
3. cd ../frontend
3. npm install
5. npm start
6. se rendre sur http://localhost:3000/

## API

Pour l'instant, plusieurs API :
- http://localhost:5000/king/year/<ANNEE-DEMANDEE>
- ==> Retourne en json les infos sur le roi en cours
- même chose pour monument et evenement


## EC2
lancer instance ec2
ouvrir port 22 3000 et 5000
```
sudo yum install git
sudo yum install python3
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
sudo yum install postgresql-server postgresql-contrib
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo passwd postgres
# config postgres
sudo su
nano /var/lib/pgsql/data/pg_hba.conf
#change IPv4 local connections to trust in pg_hba.conf.
# IPv4 local connections:
# ==> host    all         all         127.0.0.1/32          trust
cd /tmp
git clone https://github.com/oursbrindille/points-interets-parisiens.git
# create database yaml file
pip3 install -r requirements.txt
python3 app.py

curl -sL https://rpm.nodesource.com/setup_10.x | sudo bash -
sudo yum install nodejs
cd /tmp/points-interets-parisiens/frontend
npm install
npm start

```


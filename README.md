# Opetussovellus
> [!NOTE]
> Paikallinen repo hajosi (jälleen) joten commitit saattaa olla väärässä järjestyksessä/puuttua/olla duplikaattina/muuten sekasin, korjasin suurimman osan mutta jotain saattoi jäädä.

(perustuu materiaalin esimerkkiin)

Sovelluksen avulla voidaan järjestää verkkokursseja, joissa on materiaalia ja tehtäviä. 

Sovelluksen ominaisuuksia:
- Mahdollisuus tunnistautua/ luoda tunnus.
- Käyttäjät näkevät listan kursseista ja voivat liittyä kurssille omatoimisesti.
- Kurssien näkyvyyttä mahdollista säädellä (esim. materiaali näkyy avoimesti vaikkei käyttäjä ole tunnistautunut / vaatii koodin kurssille liittymiseen)
- Opiskelija voi lukea kurssin tekstimateriaalia sekä ratkoa kurssin tehtäviä.
- Opiskelija pystyy näkemään tilaston, mitkä kurssin tehtävät hän on ratkonut.
- Opettaja pystyy luomaan uuden kurssin, muuttamaan olemassa olevaa kurssia.
- Opettaja pystyy lisäämään kurssille tekstimateriaalia ja tehtäviä. Tehtävä voi olla ainakin monivalinta tai tekstikenttä, johon tulee kirjoittaa oikea vastaus.
- Opettaja pystyy näkemään kurssistaan tilaston, keitä opiskelijoita on kurssilla ja mitkä kurssin tehtävät kukin on ratkonut.


# Running
> [!NOTE]
> These instructions should work on most Linux distributions, but have been only tested on Debian (testing, amd64) and Arch (amd64). The database (and user) may need to be created in a different way on Cubli. 

1. Clone this repo 
```bash
git clone https://github.com/e11-0a/hy-tsoha.git
```
2. Create a python venv in the cloned repo's directory and install the dependencies. 
```bash
python -m venv .
source bin/activate
pip install -r requirements.txt
```
3. Create database in postgres for the application
> [!WARNING]
> These instructions may not be applicable for all distributions/ installations of postgres.
> https://www.postgresql.org/docs/current/manage-ag-createdb.html

Create the user and database for application:
```bash
su postgres
createuser <user for the database>
createdb <database for the application>
```
To set the application's user password and grant privileges to the created database (run these in the psql shell): 
```psql
alter user <user> with encrypted password '<password for the user>';
grant all privileges on database <database for application> to <user>;
```
4. Create a new configuration file from the provided example: 
```bash
cp example.ini config.ini
```
5. Edit the configuration as instructed in the example configuration file.

6. Import the provided schema to your database. For example:
```bash
psql -U <your postgres user> -d <your database> -a -f sql/create-db.sql
```

7. (optional) import test data from `sql/create-test.sql`.
> [!NOTE]
> The test data is severely outdated and might not work expectedly on the lastest version, it is recommended to not use it and just start with an empty db.
```bash 
psql -U <your postgres user> -d <your database> -a -f sql/create-test.sql
```

If you want to wipe the database after using test data you can run wipe-db.sql and reimport the schema. (useful for developement/debugging)

```bash
psql -U <your postgres user> -d <your database> -a -f sql/wipe-db.sql
psql -U <your postgres user> -d <your database> -a -f sql/create-db.sql
```

8. Run the server
```bash
flask --app app.py run
```

9. Create superuser
If test data was not used, the server allows the first user to be registered as superuser.
Registration available by default at: [http://127.0.0.1:5000/register](http://127.0.0.1:5000/register)

# Testing
If test data used, you should be able to log in with:
```
Teacher:
user_1:abcde
Student:
user_2:abcde
```

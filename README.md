# Opetussovellus
> [!WARNING]  
> Oli ongelmia paikallisen repon kanssa, tiedostoja voi puuttua tai olla väärä versio


(perustuu materiaalin esimerkkiin)

Sovelluksen avulla voidaan järjestää verkkokursseja, joissa on materiaalia ja tehtäviä. 

Sovelluksen ominaisuuksia:
- Mahdollisuus tunnistautua/ luoda tunnus.
- Käyttäjät näkevät listan kursseista ja voivat liittyä kurssille omatoimisesti.
- Kurssien näkyvyyttä mahdollista säädellä (esim. materiaali näkyy avoimesti vaikkei käyttäjä ole tunnistautunut / vaatii koodin kurssille liittymiseen)
- Opiskelija voi lukea kurssin tekstimateriaalia sekä ratkoa kurssin tehtäviä.
- Opiskelija pystyy näkemään tilaston, mitkä kurssin tehtävät hän on ratkonut.
- Opettaja pystyy luomaan uuden kurssin, muuttamaan olemassa olevaa kurssia ja poistamaan kurssin.
- Opettaja pystyy lisäämään kurssille tekstimateriaalia ja tehtäviä. Tehtävä voi olla ainakin monivalinta tai tekstikenttä, johon tulee kirjoittaa oikea vastaus.
- Opettaja pystyy näkemään kurssistaan tilaston, keitä opiskelijoita on kurssilla ja mitkä kurssin tehtävät kukin on ratkonut.


# Running

1. Create database and user in postgres
2. Create a new config file from the provided example: 
```bash
cp example.ini config.ini
```
3. At least configure `session_secret`, `connection_string` and `debug`
4. Create base tables with `sql/create-db.sql` 
5. (optional) import test data from `sql/create-test.sql`
6. Run the server
```bash
python app.py

# or

flask --app app.py run
```


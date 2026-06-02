# Elokuva-arvostelu

## Sovelluksen kuvaus

Sovelluksessa käyttäjät pystyvät jakamaan elokuva-arvostelujaan muiden käyttäjien nähtäville. Arvostelussa lukee elokuvan perustiedot: nimi, ohjaaja, julkaisuvuosi, genre sekä käyttäjän kirjoittama arvio elokuvasta.

- käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.

- käyttäjä pystyy lisäämään elokuva-arvosteluja sekä muokkaamaan ja poistamaan niitä.

- käyttäjä näkee sovellukseen lisätyt arvostelut.

- käyttäjä pystyy etsimään arvosteluja hakusanalla, kuten elokuvan nimen, ohjaajan tai julkaisuvuoden perusteella.

- käyttäjäsivu näyttää, montako arvostelua käyttäjä on lisännyt ja listan käyttäjän lisäämistä arvosteluista.

- käyttäjä pystyy valitsemaan arvostelulle yhden tai useamman luokittelun (esim. klassikko, synkkä, dystopia tai taiteellinen).

- käyttäjät pystyvät kommentoimaan muiden käyttäjien arvosteluja ja antamaan arvosanan elokuvasta. arvostelusta näytetään kommentit ja elokuvan keskimääräinen arvosana.

- sovelluksen pääasiallinen tietokohde on elokuva-arvostelu ja toissijainen tietokohde on arvostelun kommentti.


## Sovelluksen toiminnot tällä hetkellä:
- käyttäjä voi rekisteröityä ja kirjautua sisään sovellukseen
- tietokohteiden eli elokuva-arvostelujen lisääminen, muokkaaminen ja poistaminen
- lisättyjen arvostelujen selaaminen
- arvostelujen etsiminen hakusanalla
- käyttäjäsivut näyttävät listan käyttäjän lisäämistä arvosteluista
- käyttäjä pystyy valitsemaan arvostelulle luokitteluita


## Sovelluksen käynnistäminen:

### 1. Asenna Python

Suositus Python 3.10

### 2. Kloonaa repositorio

Avaa terminaali ja siirry projektikansioon: 
```
git clone (githubin SSH- tai HTTPS-linkki )
cd elokuva-arvostelu
```

### 3. Luo virtuaaliympäristö 

Windows: 
```
python -m venv venv
venv\Scripts\activate
```

Mac/Linux: 
```
python3 -m venv venv
source venv/bin/activate
```

### 4. Asenna Python-kirjasto: 
```
pip install flask
```

### 5. Luo tietokanta SQL-tiedoston avulla 
```
sqlite3 database.db < schema.sql
```

### 6. Käynnistä sovellus 
```
flask run
```

### 7. Avaa sovellus osoitteessa http://127.0.0.1:5000

Luo uusi käyttäjä etusivulla ja kirjaudu sisään.

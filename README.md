# Elokuva-arvostelu

## Sovelluksen kuvaus

Sovelluksessa käyttäjät pystyvät jakamaan elokuva-arvostelujaan muiden käyttäjien nähtäville. Arvostelussa lukee elokuvan perustiedot: nimi, ohjaaja, julkaisuvuosi, genre sekä käyttäjän kirjoittama arvio elokuvasta.

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.

- Käyttäjä pystyy lisäämään elokuva-arvosteluja sekä muokkaamaan ja poistamaan niitä.

- Käyttäjä näkee sovellukseen lisätyt arvostelut.

- Käyttäjä pystyy etsimään arvosteluja hakusanalla, kuten elokuvan nimen, ohjaajan tai julkaisuvuoden perusteella.

- Käyttäjäsivu näyttää, montako arvostelua käyttäjä on lisännyt ja listan käyttäjän lisäämistä arvosteluista.

- Käyttäjä pystyy valitsemaan arvostelulle yhden tai useamman luokittelun (esim. klassikko, synkkä, dystopia tai taiteellinen).

- Käyttäjät pystyvät kommentoimaan muiden käyttäjien arvosteluja ja antamaan arvosanan elokuvasta. Arvostelusta näytetään kommentit ja elokuvan keskimääräinen arvosana.

- Sovelluksen pääasiallinen tietokohde on elokuva-arvostelu ja toissijainen tietokohde on arvostelun kommentti.



## Sovelluksen käynnistäminen:

### 1. Asenna Python

Sovellus toimi Python 3 -versiolla

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

### 6. Lisää luokittelut
```
sqlite3 database.db < init.sql
```

### 7. Käynnistä sovellus 
```
flask run
```

### 8. Avaa sovellus osoitteessa http://127.0.0.1:5000

Luo uusi käyttäjä etusivulla ja kirjaudu sisään.

# OtaRoads

## Esittely

Otaroads -ohjelma lukee Digiroad -formaatissa olevan .csv -tiedoston Otaniemen kevyen ja raskaan liikenteen väylistä, ja laatii sen pohjalta tiekartan.

Visuaalisessa käyttöliittymässä on tarjolla mahdollisuus katsella luotua tiekarttaa, napsautella hiirellä pisteitä, sekä laskea valittujen pisteiden välille lyhyimpiä tai nopeimpia reittejä. Pisteiden koordinaatit voi syöttää hiiren napsautuksen lisäksi myös käsin (numeroina) tai valitsemalla valmiiksi annetuista oikotie -napeista joitain Otaniemen suosituimmista paikoista. Reitit lasketaan käyttäen Dijkstran algoritmia, ja lasketusta reitistä kerrotaan sen pituus ja siihen kuluva aika, ja lopullinen reitti myös visualisoidaan kartalle.

## Tiedosto- ja kansiorakenne

Kaikki tarvittavat tiedostot löytyvät Koodit -kansiosta. Python-tiedostojen lisäksi samassa kansiossa sijaitsee myös tarvittava .csv -tiedosto.

Dokumentit -kansiosta löytyy projektin suunnitelmaa, kulkua ja toteutusta havainnollistavia dokumentteja.


## Asennusohje

Ainoa pythonin omien kirjastojen ulkopuolinen kirjasto, jota tässä projektissa on käytetty on PyQt6, joka mahdollistaa visuaalisen käyttöliittymän.

## Käyttöohje

Ohjelma ajetaan suorittamalla main.py -tiedosto Pythonilla. Esimerkiksi komentorivillä suorittamalla komento: "python main.py", kunhan on ensiksi navigoitu kyseisen tiedoston sisältävään kansioon. 

Komennon suorituttua avautuu ohjelman visuaalinen käyttöliittymä -ikkuna, josta pitäisi lyötyä kaikki tarvittava informaatio ohjelman käyttämiseksi. Ohjelman toimintoja on selvennetty tarkemmin dokumentaatiossa.




import csv
import math

from etaisyyslaskuri import Etaisyyslaskuri
from tie import Tie
from dijkstrapiste import Dijkstrapiste
from koordinaatti import Koordinaatti


class Roadreader:
    """
    Tämän luokan tarkoituksena on lukea Digiroad -muotoinen .csv -tiedosto, ja luoda sen pohjalta tietorakenteet, joilla
    on mahdollista piirtää tiet ja laskea niiden välille erilaisia reittejä.
    """
    def __init__(self):
        self.roads = []
        self.naapuruus_sanakirja = {}

        # Näiden avulla on helpompi varmistaa minkä kokoinen karttaikkuna halutaan.
        self.pienin_x = None
        self.suurin_x = None
        self.pienin_y = None
        self.suurin_y = None

        self.dijkstrapisteet = []   # näitä käytetään Dijkstran algoritmin kanssa

    def lue_pilkuin_eroteltu_tiedosto(self, csv_file):
        """
        Tämä metodi lukee annetun CSV-tiedoston, ottaa talteen tarvittavat tiedot, luo Tie-oliot tietojen
        pohjalta, ja tallettaa luodut Tiet self.roads -listaan.

        """
        with open(csv_file) as roadfile:
            csv_reader = csv.reader(roadfile, delimiter=";")

            rivinro = 0
            for rivi in csv_reader:

                # tämä käy läpi kaikki rivit. Yksi rivi vastaa yhtä tietä.
                if (rivinro > 4):               #  tämä ohittaa turhat rivit alusta
                    raakadata = "".join(rivi)
                    raakadata = raakadata[35:]      # [35:] poistaa turhaa dataa

                    split_at_colon = raakadata.split(":")     # erottelee datasta kaksoispisteellä erotellut elementit

                    if(len(split_at_colon) == 1):    # tämä lopettaa läpikäymisen kun tulee vastaan liian lyhyt lista (aineiston viimeinen elementti)
                        break

                    # Toiminnallinen luokka löytyy indeksistä [3][1]
                    toiminnallinen = int(split_at_colon[3][1].strip())

                    autoiltava = self.set_autoiltavuus(toiminnallinen)

                    # Nopeus löytyy indeksistä [6][0:3]
                    # nopeus = self.set_nopeus(split_at_colon[6][0:3].strip())

                    if (autoiltava):  # nopeuden säätö ei jostain syystä toimi, joten käytetään tätä oikotienä:
                        nopeus = 40
                    else:
                        nopeus = 10

                    #koordinaatit löytyvät indeksistä [9], mutta sitä on syytä siistiä hieman.
                    koordinaatit = split_at_colon[9].strip().replace("[", "").replace("]", "").replace("}", "")
                    koordinaatit = koordinaatit.split(",")

                    tien_koordit = self.prosessoi_koordinaatit(koordinaatit)
                    tien_pituus = self.etaisyydet_yhteensa(tien_koordit)

                    # etsitään tien päätepisteet
                    paate_a = tien_koordit[0]
                    paate_b = tien_koordit[len(tien_koordit)-1]

                    # Luodaan Tie -olio
                    this_tie = Tie(autoiltava, nopeus, tien_koordit, tien_pituus, paate_a, paate_b)

                    if (paate_a in self.naapuruus_sanakirja.keys()):
                        self.naapuruus_sanakirja[paate_a].append(this_tie)
                    else:
                        self.naapuruus_sanakirja[paate_a] = [this_tie]
                    if (paate_b in self.naapuruus_sanakirja.keys()):
                        self.naapuruus_sanakirja[paate_b].append(this_tie)
                    else:
                        self.naapuruus_sanakirja[paate_b] = [this_tie]

                    self.roads.append(this_tie)

                rivinro += 1

            # lisätään lopuksi vielä naapurit jokaiselle tielle:
            self.add_neighbors()

    def add_neighbors(self):
        """
        Käy läpi naapuruus-sanakirjan, ja sen perusteella lisää Tie-olioille naapurit.
        """
        for i in self.naapuruus_sanakirja.keys():
            verkosto = self.naapuruus_sanakirja[i]
            for tie in verkosto:
                for tie2 in verkosto:
                    if (tie != tie2):
                        tie.add_naapuri(tie2)

    def set_autoiltavuus(self, luokka):
        """
        Määrittää toiminnallisen luokan perusteella, onko tie kevyen liikenteen väylä vai autoiltavissa.
        Palauttaa Boolean-arvon.
        """

        # Kävelyn ja pyöräilyn tiet luokassa 8, autotiet luokissa 1-7.
        if (luokka == 8):
            autoiltava = False
        elif (luokka >= 1 and luokka <= 7):
            autoiltava = True
        else:
            print("Exception should raise here")
        return autoiltava

    def set_nopeus(self, nopeus):
        """
        kävelylle ja pyöräilylle oletusnopeus 10 km/h, muussa tapauksessa annettu arvo. Palauttaa kokonaisluvun.
        """
        if (nopeus.isnumeric()):
            nopeus = 40         # numeromuotoisten teiden nopeudet ovat 40 km/h
        else:
            nopeus = 10         # jos tielle ei ole annettuna nopeutta, se oletetaan kevyen liikenteen väyläksi
                                # ja nopeudeksi asetetaan 10 km/h
            return nopeus

    def prosessoi_koordinaatit(self,koordinaatit):
        """
        Tämä metodi ottaa parametrinään listan koordinaatteja string -muodossa,
        muuttaa ne float -muotoon ja palauttaa listan, joka sisältää tielle kuuluvat koordinaatit kahden
        numeron (x,y) listoina, esimerkiksi:
        [[24.822613, 60.1817545], [24.8224843, 60.1817671]]
        """

        pairs = 1
        koordinaattitupla = []
        tien_koordit = []

        for i in koordinaatit:
            i = i.strip()
            try:
                this_koord = float(i)
                koordinaattitupla.append(this_koord)
                pairs += 1

                if (pairs > 3):
                    x = koordinaattitupla[0]       # huom! EUREFTM35 -järjestelmässä x ja y 'väärinpäin'
                    y = koordinaattitupla[1]
                    z = koordinaattitupla[2]

                    self.etsi_rajat(x, y)

                    oikea_koordinaatti = Koordinaatti(x, y)

                    tien_koordit.append(oikea_koordinaatti)
                    koordinaattitupla = []
                    pairs = 1

            except ValueError:
                pass

        return tien_koordit

    def etaisyydet_yhteensa(self, koordinaattilista):
        """
            Tämä metodi laskee ja palauttaa yhteenlasketun pituuden annetulle koordinaattilistalle
        """

        edellinen = None
        summa = 0
        etaisyyslaskuri = Etaisyyslaskuri("laskuri")

        for i in koordinaattilista:
            if (edellinen):
                summa = summa + etaisyyslaskuri.laske(edellinen, i)
            else:
                edellinen = i

        return summa

    def get_roads(self):
        return self.roads

    def etsi_rajat(self,x,y):
        if (self.pienin_x):
            if (x < self.pienin_x):
                self.pienin_x = x
        else:
            self.pienin_x = x

        if (self.suurin_x):
            if (x > self.suurin_x):
                self.suurin_x = x
        else:
            self.suurin_x = x

        if (self.pienin_y):
            if (y < self.pienin_y):
                self.pienin_y = y
        else:
            self.pienin_y = y

        if (self.suurin_y):
            if (y > self.suurin_y):
                self.suurin_y = y
        else:
            self.suurin_y = y

    def laske_rajojen_erot(self):
        x_diff = self.suurin_x - self.pienin_x
        y_diff = self.suurin_y - self.pienin_y

        return x_diff, y_diff

    def get_extent(self):

        max_x = self.suurin_x
        max_y = self.suurin_y
        min_x = self.pienin_x
        min_y = self.pienin_y

        return max_x, min_x, max_y, min_y

    def luo_dijkstrat(self):
        """
        Tällä metodilla luodaan Dijkstrapisteet Dijkstran algoritmia varten.
        """
        # käydään läpi kaikki tiet, otetaan niiden koordinaatit ja luodaan niiden pohjalta dijkstrapisteet
        el = Etaisyyslaskuri('a')

        for i in self.roads:
            for j in i.get_koordinaatit():
                d = Dijkstrapiste(j)
                self.dijkstrapisteet.append(d)

        for k in self.dijkstrapisteet:
            point_a = k.get_koord()
            for l in self.roads:
                tien_pisteet = l.get_koordinaatit()
                for n in tien_pisteet:
                    matka = el.laske(point_a,n)
                    if (matka <= 0.001):
                        aika = matka / l.get_nopeus()
                        luokka = l.get_autoiltava()
                        k.add_neigbour(n, matka, aika, luokka)

                if point_a in tien_pisteet:
                    for m in tien_pisteet:
                        matka = el.laske(point_a, m)
                        aika = matka / l.get_nopeus()
                        luokka = l.get_autoiltava()
                        k.add_neigbour(m, matka, aika, luokka)

        return self.dijkstrapisteet


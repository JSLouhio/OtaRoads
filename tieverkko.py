from etaisyyslaskuri import Etaisyyslaskuri
from priojono import Priojono


class Tieverkko:

    def __init__(self, roads):
        self.roads = roads

    def get_roads(self):
        return self.roads

    def get_len(self):
        return len(self.roads)

    def find_closest_road(self, point):
        """
        etsii annettua pistettä lähimmän tien päätepisteen.
        Oletusarvoisesti tielle voi mennä ainoastaan sen päätepisteistä.

        Point on Koordinaatti.
        """

        laskuri = Etaisyyslaskuri("lasku")
        closest = [None, None, None]      # [tie, pituus, päätepiste]

        for i in self.roads:

            closer = None
            distance = None
            piste_a = i.get_paatepiste_a()
            piste_b = i.get_paatepiste_b()

            etaisyys_a = laskuri.laske(point, piste_a)
            etaisyys_b = laskuri.laske(point, piste_b)


            if (etaisyys_a < etaisyys_b):
                closer = piste_a
                distance = etaisyys_a
            else:
                closer = piste_b
                distance = etaisyys_b

            if (closest[0] == None):
                closest[0] = i
                closest[1] = distance
                closest[2] = closer

            if (distance < closest[1]):
                closest[0] = i
                closest[1] = distance
                closest[2] = closer

        return closest

    def dijkstra(self, aloituspiste, paino):
        """
        Ohjelma ei käytä tätä versiota Dijkstran algoritmin toteutuksesta.
        Tämä oli ensimmäinen yritys toteuttaa Dijkstran algoritmi ennenkuin päädyin käyttämään hieman erilaista tietorakennetta.
        """

        pisteet_ja_tiet = {}

        for tie in self.roads:
            pisteet_ja_tiet[tie.get_paatepiste_a()] = tie

        kaydyt = set()          # tähän pisteet, joissa on jo vierailtu
        edsgerin_polku = {}     # tähän rakentuu kuljettu tie, ts. vanhemmat, muotoa {piste : tie}
        pisteiden_hinnat = {}   # tähän pienimmät tunnetut hinnat pisteille

        #lisäätään kaikki verkon pisteet ylläolevaan, ja alusta niiden hinnaksi ääretön.
        for i in self.roads:
            piste = i.get_paatepiste_a()
            pisteiden_hinnat[piste] = float('inf')

        pisteiden_hinnat[aloituspiste] = 0 # alustetaan alkupisteelle hinnaksi 0
        priojono = Priojono()               # alustetaan prioriteettijono, ja lisätään sinne aloituspiste prioriteetteineen
        priojono.lisaa({aloituspiste: 0})

        while(True):
            if priojono.is_empty():
                break
            else:
                this_piste = priojono.get()
                kaydyt.add(this_piste)

                this_tie = pisteet_ja_tiet[this_piste]

                for naapuri in this_tie.get_naapuripisteet():
                    if naapuri in kaydyt:
                        continue

                    if(paino == 0):
                        naapurin_hinta = pisteet_ja_tiet[naapuri].get_pituus()
                    else:
                        naapurin_hinta = pisteet_ja_tiet[naapuri].get_pituus() / pisteet_ja_tiet[naapuri].get_nopeus()

                    uusihinta = pisteiden_hinnat[this_piste] + naapurin_hinta

                    if uusihinta < pisteiden_hinnat[naapuri]:
                        edsgerin_polku[naapuri] = pisteet_ja_tiet[naapuri]
                        pisteiden_hinnat[naapuri] = uusihinta
                        priojono.lisaa({naapuri: uusihinta})

        return edsgerin_polku, pisteiden_hinnat

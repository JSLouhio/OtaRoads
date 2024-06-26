import unittest
from etaisyyslaskuri import Etaisyyslaskuri
from koordinaatti import Koordinaatti
from priojono import Priojono


class testeja(unittest.TestCase):
    # Tämä testaa etäisyyslaskurin toimintaa tunnettujen koordinaattien ja niiden etäisyyksien avulla.

    # Tämä testaa lyhyttä etäisyyttä Polin ja Dipolin välillä
    def test_etaisyyslaskuri_lyhyt(self):
        laskuri = Etaisyyslaskuri("el")
        poli = Koordinaatti(60.16422, 24.93217)
        dipoli = Koordinaatti(60.18487, 24.83287)
        poli_dipoli_etaisyys = round(laskuri.laske(poli,dipoli), 2)

        self.assertEqual(poli_dipoli_etaisyys,5.95)

    # Tämä testaa pitkää välimatkaa Shanghain ja New Yorkin välillä.
    def test_etaisyyslaskuri_pitka(self):
        laskuri = Etaisyyslaskuri("el")
        shanghai = Koordinaatti(31.23332, 121.50543)
        newyork = Koordinaatti(40.74839, -73.98569)
        shanghai_ny_etaisyys = round(laskuri.laske(shanghai, newyork), 2)

        self.assertEqual(shanghai_ny_etaisyys, 11854.04)

    def test_priojono(self):
        # Tämä testi testaa, että prioriteettijono palauttaa sille annetut esineet oikeassa järjestyksessä
        # (pienimmästä suurimpaan)

        pj = Priojono()

        pj.lisaa({'a': 2000})
        pj.lisaa({'b': 5})
        pj.lisaa({'c': 500})
        pj.lisaa({'d': 1000000})
        pj.lisaa({'e': 24})
        pj.lisaa({'f': 1})
        pj.lisaa({'g': 777})

        lista = []

        while (True):
            if (pj.is_empty()):
                break
            else:
                esine, prioriteetti = pj.get()
                lista.append(prioriteetti)

        vertailulista = [1, 5, 24, 500, 777, 2000, 1000000]

        self.assertEqual(lista, vertailulista)



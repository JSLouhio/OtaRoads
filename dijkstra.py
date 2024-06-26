from dijkstrapiste import Dijkstrapiste
from priojono import Priojono

class Dijkstra:
    """
    Tässä luokassa on toteutettuna Dijkstran algoritmi, jolla lasketaan verkolle virityspuu annetun lähtöpisteen perusteella.
    Virityspuusta voidaan etsiä lyhyin reitti lähtöpisteen ja jonkin toisen pisteen välille.

    """
    def __init__(self, verkko):
        self.verkko = verkko        # Dijkstrapisteverkko listana: pisteellä xy, naapurit:matka-aika-luokka, vanhempi, etäisyys ja käsittelystatus


    def algoritmi(self, aloituspiste, paino=0, luokka=0):
        # paino 0 = lyhin, muutoin pituus / nopeus
        # jos luokka = 0, kaikki tiet, 1 auto, 2 kevyt

        pisteet = {}    # muodossa Koordinaatti: Dijkstrapiste

        # käydään läpi verkon pisteet, ja lisätään ne edelliseen sanakirjaan.
        # Tässä myös poistetaan halutut luokat, mutta tämän toteutuksen kanssa oli ongelmia, joten lopullinen
        # ohjelma ei ota huomioon tietyyppejä.

        for i in self.verkko:
            if (luokka == 1):
                i.remove_neighbours(1)
            elif(luokka == 2):
                i.remove_neighbours(2)

            pisteet[i.get_koord()] = i

        pisteet[aloituspiste.get_koord()].set_eta(0)

        jono = Priojono()               # alustetaan prioriteettijono ja lisätään sinne aloituspiste prioriteetilla 0.
        jono.lisaa({aloituspiste: 0})

        while (True):
            if jono.is_empty():     # jos prioriteetti jono on tyhjä, lopetetaan algoritmin läpikäyminen
                break
            else:
                this_piste, prio = jono.get()       # otetaan pienimmän prioriteetin omaava piste jonosta
                if pisteet[this_piste.get_koord()].get_kasitelty():     # jos tämä piste on jo käsitelty, jätetään huomioimatta.
                    continue

            pisteet[this_piste.get_koord()].set_kasitelty()     # merkitään piste käsitellyksi

            for naapuri in pisteet[this_piste.get_koord()].get_neighbours().keys():     # käydään läpi pisteen naapurit

                if pisteet[naapuri].get_kasitelty():        # jo-käsiteltyjä naapureita ei käsitellä enää uudestaan.
                    continue

                naapurusto = pisteet[this_piste.get_koord()].get_neighbours()       # etsitään tämän pisteen naapurit
                etaisyys = naapurusto[naapuri][0]                               # selvitetään etäisyys tähän naapuriin
                aika = naapurusto[naapuri][1]                                   # ... ja matka-aika
                tieluokka = naapurusto[naapuri][2]                              # ...ja kuljetun tien tieluokka

                if (paino == 1):        # jos painotukseksi on asetettu matka-aika reitin pituuden sijaan,
                    etaisyys = aika     # etäisyytenä käytetään matka-aikaa.

                uusi_etaisyys = prio + etaisyys     # etäisyyteen lasketaan mukaan prioriteetti, eli etäisyys lähtöpisteeseen.

                if (uusi_etaisyys < pisteet[naapuri].get_eta()):    #etäisyyden ollessa pienempi kuin virityspuuhun merkitty,

                    pisteet[naapuri].set_eta(uusi_etaisyys)         # asetetaan uusi etäisyys
                    pisteet[naapuri].set_vanhempi(this_piste)       # asetetaan tämä piste naapuripisteen vanhemmaksi (eli kauttakulkupisteeksi)
                    pisteet[naapuri].set_tieluokka_vanhempaan(tieluokka)    # asetetaan tieluokka vanhempaan kulkiessa
                    pisteet[naapuri].set_aika_vanhempaan(aika)      #asetetaan matka-aika vanhempaan
                    jono.lisaa({pisteet[naapuri]: uusi_etaisyys})   #lisätään piste prioriteettijonoon uudella etäisyydellä.

        return pisteet

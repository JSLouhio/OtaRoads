class Dijkstrapiste:
    """
    Tämän luokan tarkoituksena on helpottaa Dijkstran algoritmin käyttöä.

    Luokan olioilla on koordinaatit ja sanakirjat, jotka sisältävät avaiminaan niiden naapurit ja tietosisältönä
    matkan, ajan ja tieluokan kuljettaessa kyseiseen naapuriin.

    Lisäksi luokan olioilla on 'vanhemmat' eli tieto siitä, minkä pisteen kautta kuljettaessa matka on lyhyin.

    """

    def __init__(self, koordinaatti):

        self.koordinaatti = koordinaatti
        self.tie = None
        self.naapurit = {} # sanakirja muodosssa {naapuri:[matka, aika, luokka]}
        self.kasitelty = False  # nämä tulevat tarpeeseen algoritmia pyörittäessä
        self.vanhempi = None        # Tämä viittaa pisteesen, jonka kautta on lyhyin reitti kulkea tähän pisteeseen.
        self.etaisyys_vanhempaan = float('inf') # tämä alustetaan äärettömään, jotta voitaisiin helposti vertailla etäisyyttä muihin pisteisiin.
        self.tieluokka_vanhempi = True
        self.aika_vanhempaan = None

    def add_neigbour(self,neighbour, matka, aika, luokka):
        self.naapurit[neighbour] = [matka, aika, luokka]

    def remove_neighbours(self, type):
        # type 1: poista kevyet, 2: poista raskaat

        keys_to_remove = []

        for i in self.naapurit:
            luokka = self.naapurit[i][2]  # True, jos autoiltava

            if (type == 1):
                if (not luokka):
                    keys_to_remove.append(i)

            if (type == 2):
                if (luokka):
                    keys_to_remove.append(i)

        for j in keys_to_remove:
            self.naapurit.pop(j)

    def set_vanhempi(self, van):
        self.vanhempi = van

    def get_vanhempi(self):
        return self.vanhempi

    def set_aika_vanhempaan(self, aika):
        self.aika_vanhempaan = aika

    def get_aika_vanhempaan(self):
        return self.aika_vanhempaan

    def set_tieluokka_vanhempaan(self, boole):
        self. tieluokka_vanhempi = boole

    def get_tieluokka_vanhempaan(self):
        return self.tieluokka_vanhempi

    def get_eta(self):
        return self.etaisyys_vanhempaan

    def set_eta(self, eta):
        self.etaisyys_vanhempaan = eta

    def get_koord(self):
        return self.koordinaatti

    def get_neighbours(self):
        return self.naapurit

    def set_kasitelty(self):
        self.kasitelty = True

    def get_kasitelty(self):
        return self.kasitelty

    def reset(self):
        """
        Tällä metodilla palautetaan olio 'tehdasasetuksille', jotta algoritmi voidaan suorittaa uudestaan.
        """
        self.kasitelty = False
        self.vanhempi = None
        self.etaisyys_vanhempaan = float('inf')

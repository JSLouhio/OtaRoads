class Tie:
    """
    Olio, joka kuvaa yksittäistä tietä
    """

    tienumerot = []                             # oliomuuttujalista, josta luodaan tienumerot (eli id:t) jokaiselle tielle.
    def __init__(self, autoiltava, nopeus, koordinaatilista, pituus, paate_a, paate_b):

        if Tie.tienumerot:                        # ottaa oliomuuttujalistasta ensimmäisen (eli tässä tapauksessa viimeksi lisätyn)
            viimeinen = Tie.tienumerot[0]           # numeron, kasvattaa sitä yhdellä ja asettaa uuden id:n Tien id:ksi
            uusi = viimeinen + 1                    # saatu uusi id lisätään oliomuuttujalistaan kohdalle 0.
            Tie.tienumerot.insert(0, uusi)
            self.id = uusi
        else:
            Tie.tienumerot.append(0)              # oliomuuttujalistan ollessa tyhjä alustetaan se nollalla.
            self.id = 0

        self.autoiltava = autoiltava        # Totuusarvo, True: autotie, False: kevyen liikenteen väylä
        self.nopeus = nopeus
        self.koordinaatit = koordinaatilista
        self.pituus = pituus
        self.paatepiste_a = paate_a
        self.paatepiste_b = paate_b
        self.naapurit = []

    def get_numero(self):
        return self.id

    def get_autoiltava(self):
        return self.autoiltava

    def get_nopeus(self):
        return self.nopeus

    def get_koordinaatit(self):
        return self.koordinaatit

    def get_pituus(self):
        return self.pituus

    def get_paatepiste_a(self):
        return self.paatepiste_a

    def get_paatepiste_b(self):
        return self.paatepiste_b

    def get_naapurit(self):
        return self.naapurit

    def get_naapuripisteet(self):
        # palauttaa pisteet, joihin pääsee tämän tien kautta (naapuriteiden alkupisteet)

        neighbours = []
        for i in self.naapurit:
            piste = i.get_paatepiste_a()
            neighbours.append(piste)

        return neighbours

    def add_naapuri(self, naapuritie):
        self.naapurit.append(naapuritie)

    def __repr__(self):

        if self.autoiltava:
            kulku = "autotie"
        else:
            kulku = "kävelytie"

        yhteydet = ""
        for i in self.naapurit:
            yhteydet += "Tie: {} ".format(i.get_numero())

        palaute = "Tienumero: {} Pituus: {} Nopeusrajoitus: {} Tyyppi: {} yhteydet: {}".format(self.id, self.pituus, self.nopeus, kulku, yhteydet)
        # tämä esitys ei osoittautunut käytännölliseksi, joten päätin esittää tiet pelkän tienumeron kautta.

        return "Tienumero: {}".format(self.id)

    # nämä kolme metodia auttavat koordinaattien vertailussa toisiin koordinaatteihin
    def __key(self):
        return (self.id)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Tie):
            return self.__key() == other.__key()

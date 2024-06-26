from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsLineItem, QLabel, QWidget, \
    QPushButton, QVBoxLayout, QHBoxLayout, QRadioButton, QCheckBox, QLineEdit
from PyQt6.QtGui import QPen, QColor

from koordinaatti import *
from etaisyyslaskuri import Etaisyyslaskuri
from dijkstra import Dijkstra


class Window(QMainWindow):

    def __init__(self, min_x, min_y, max_x,max_y, verkko, d_verkko):

        super().__init__()

        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.verkko = verkko             # tieverkko
        self.dijkstra_verkko = d_verkko  # Dijkstrapiste -verkko

        # nämä vastaavat reitin päätöspisteitä. Alustetaan ne 0,0 -koordinaateilla.
        self.piste_1 = Koordinaatti(0, 0)
        self.piste_2 = Koordinaatti(0, 0)
        self.piste_1_x_set = False
        self.piste_2_x_set = False
        self.piste_1_y_set = False
        self.piste_2_y_set = False

        # nämä elementit ilmoittavat annettujen pisteiden koordinaatit, ja mahdollistavat koordinaattien antamisen käsin.
        self.button1_x_label = QLabel('Piste A: N:')
        self.button1_x_edit = QLineEdit("24.00")
        self.button1_y_label = QLabel("E:")
        self.button1_y_edit = QLineEdit("60.00")

        self.button2_x_label = QLabel('Piste B: N:')
        self.button2_x_edit = QLineEdit("24.00")
        self.button2_y_label = QLabel("E:")
        self.button2_y_edit = QLineEdit("60.00")

        # lisätään edellisille painikkeille toiminnallisuudet
        self.button1_x_edit.editingFinished.connect(self.piste_1_input_x)
        self.button1_y_edit.editingFinished.connect(self.piste_1_input_y)
        self.button2_x_edit.editingFinished.connect(self.piste_2_input_x)
        self.button2_y_edit.editingFinished.connect(self.piste_2_input_y)

        self.button3 = QLabel('Viimeisimmän napsautuksen koordinaatit')

        # luodaan napit, joilla kontrolloidaan ohjelman toimintaa.
        self.button4 = QPushButton("Tyhjennä")
        self.button5 = QPushButton("Laske!")
        self.button6 = QRadioButton("Lyhyin reitti")
        self.button6.setChecked(True)
        self.button7 = QRadioButton("Nopein reitti")

        self.button8 = QCheckBox("Kevyen liikenteen väylät")
        self.button8.setChecked(True)
        self.button9 = QCheckBox("Raskaan liikenteen väylät")
        self.button9.setChecked(True)

        # koska lopulta osoittautui, ettei ollut mahdollista toteuttaa tietyyppien huomioonottoa kunnolla toimivasti,
        # poistetaan tästä versiosta toiminnallisuus muuttaa tietyyppejä.
        self.button8.setEnabled(False)
        self.button9.setEnabled(False)

        # luodaan label -elementit, jotka ilmaisevat mitä pisteitä on valittuna, sekä napit shortcutteja varten
        self.button10 = QLabel('Valitut pisteet:')
        self.button11 = QLabel('Piste A: ')
        self.button12 = QLabel('Piste B: ')

        self.button13 = QLabel('Oikotiet:')             # indeksit self.shortcut -listassa:
        self.button14 = QPushButton("Dipoli")           # 0
        self.button15 = QPushButton("Amfi")             # 1
        self.button16 = QPushButton("TF")               # 2
        self.button17 = QPushButton("Otakaari 20")      # 3
        self.button18 = QPushButton("Smökki")           # 4
        self.button19 = QPushButton("Rantasauna")       # 5
        self.button20 = QPushButton("A Block")          # 6
        self.button21 = QPushButton("Miinusmaa")        # 7
        self.button22 = QPushButton("TUAS")             # 8
        self.button23 = QPushButton("Desing Factory")   # 9

        self.shortcuts = [(24.8325637, 60.1847159), (24.8281029, 60.1862488), (24.8330297, 60.1859155), (24.8332960, 60.1865820), (24.8364918, 60.1883149), (24.8386888, 60.1880149), (24.8261056, 60.1847825),(24.8190483, 60.1867819),(24.8285689, 60.1890480), (24.8311655, 60.1808835)]

        # lisätään toiminnallisuudet ylläoleviin nappeihin:
        self.button14.clicked.connect(lambda: self.shortcut(0))
        self.button15.clicked.connect(lambda: self.shortcut(1))
        self.button16.clicked.connect(lambda: self.shortcut(2))
        self.button17.clicked.connect(lambda: self.shortcut(3))
        self.button18.clicked.connect(lambda: self.shortcut(4))
        self.button19.clicked.connect(lambda: self.shortcut(5))
        self.button20.clicked.connect(lambda: self.shortcut(6))
        self.button21.clicked.connect(lambda: self.shortcut(7))
        self.button22.clicked.connect(lambda: self.shortcut(8))
        self.button23.clicked.connect(lambda: self.shortcut(9))

        self.button24 = QLabel("Laskettu reitti:")  # näillä kerrotaan lasketun reitin tilastoja
        self.button25 = QLabel("")

        self.button4.clicked.connect(self.clear)            # yhdistetään tyhjennä -nappi toiminnalisuuteen
        self.button5.clicked.connect(self.dijkstraa)

        self.main_widget = QWidget()

        self.main_layout = QVBoxLayout()        # päälayouttina pysty-laatikko
        self.hbox_layout = QHBoxLayout()        # vaakalaatikko layout
        self.setting_layout = QHBoxLayout()     # layout asetuksille myös vaakalaatikkona
        self.central_layout = QHBoxLayout()     # layout muotoa [ valitut - view - oikotiet]
        self.valittu_layout = QVBoxLayout()     # layout valituille pisteille ja reitille
        self.oikotie_layout = QVBoxLayout()     # layout oikotienapeille

        self.setMouseTracking(True)             # seurataan hiiren napsautuksia

        self.scene = QGraphicsScene()           # luodaan scene
        self.view = QGraphicsView(self.scene)   # luodaan view, ja asetetaan sille scene

        self.main_layout.addWidget(self.button5)  # laske -nappi

        self.main_layout.addLayout(self.setting_layout)  # lisätään layout valinta-napeille, ja napit sinne
        self.setting_layout.addWidget(self.button6)
        self.setting_layout.addWidget(self.button7)
        self.setting_layout.addWidget(self.button8)
        self.setting_layout.addWidget(self.button9)

        self.main_layout.addLayout(self.central_layout)     #lisätään keskus layout, ja sisältöä sinne.
        self.central_layout.addLayout(self.valittu_layout)
        self.valittu_layout.addWidget(self.button10)
        self.valittu_layout.addWidget(self.button11)
        self.valittu_layout.addWidget(self.button12)
        self.valittu_layout.addWidget(self.button24)
        self.valittu_layout.addWidget(self.button25)
        self.valittu_layout.addStretch()    # loppuun strech, jotta napit asettuisivat ylälaitaan.

        self.central_layout.addWidget(self.view)

        self.central_layout.addLayout(self.oikotie_layout)  # asetetaan oikotie nappien layout, ja napit sinne.
        self.oikotie_layout.addWidget(self.button13)
        self.oikotie_layout.addWidget(self.button14)
        self.oikotie_layout.addWidget(self.button15)
        self.oikotie_layout.addWidget(self.button16)
        self.oikotie_layout.addWidget(self.button17)
        self.oikotie_layout.addWidget(self.button18)
        self.oikotie_layout.addWidget(self.button19)
        self.oikotie_layout.addWidget(self.button20)
        self.oikotie_layout.addWidget(self.button21)
        self.oikotie_layout.addWidget(self.button22)
        self.oikotie_layout.addWidget(self.button23)
        self.oikotie_layout.addStretch()

        self.main_layout.addLayout(self.hbox_layout)        # asetetaan pää-layouttiin vielä vaakalaatikko layout
        self.setCentralWidget(self.main_widget)             # koordinaatti laatikoita ja painikkeita varten

        self.hbox_layout.addWidget(self.button1_x_label)
        self.hbox_layout.addWidget(self.button1_y_edit)
        self.hbox_layout.addWidget(self.button1_y_label)
        self.hbox_layout.addWidget(self.button1_x_edit)

        self.hbox_layout.addWidget(self.button2_x_label)
        self.hbox_layout.addWidget(self.button2_y_edit)
        self.hbox_layout.addWidget(self.button2_y_label)
        self.hbox_layout.addWidget(self.button2_x_edit)

        self.hbox_layout.addWidget(self.button4)
        self.main_layout.addWidget(self.button3)

        self.main_widget.setLayout(self.main_layout)

        self.setWindowTitle('OtaRoads')
        self.setGeometry(0, 0, 1080, 1920)

        self.show()


    def shortcut(self, destination):

        pari = self.shortcuts[destination]

        x = pari[0]
        y = pari[1]

        self.set_point_xy(x,y)

    def clear(self):
        """
        Tämä metodi poistaa valitut reittipisteet ja piirretyt reitit sekä nollaa tarvittavat elementit
        """

        for i in self.dijkstra_verkko:
            i.reset()

        self.scene.clear()
        self.button1_x_edit.setText("anna E")
        self.button1_y_edit.setText("anna N")

        self.button2_x_edit.setText("anna E")
        self.button2_y_edit.setText("anna N")

        self.button11.setText("Piste A: ")
        self.button12.setText("Piste B:")

        self.button25.setText("")

        self.piste_1.set_x(0)
        self.piste_1.set_y(0)

        self.piste_2.set_x(0)
        self.piste_2.set_y(0)

        self.piste_1_x_set = False
        self.piste_1_y_set = False
        self.piste_2_x_set = False
        self.piste_2_y_set = False

        self.paint_all_roads()
        self.paint_borders()

    # seuraavat neljä metodia käsittelevät kirjoittamalla annettuja koordinaatteja.
    def piste_1_input_x(self):
        if (not self.piste_1_x_set):
            x = float(self.button1_x_edit.text())
            x = round(x, 7)
            self.piste_1.set_x(x)
            self.piste_1_x_set = True
            y = self.piste_1.get_xy()[1]
            self.button11.setText("Piste A: \n N: {} \n E: {}".format(y, x))

    def piste_1_input_y(self):
        if (not self.piste_1_y_set):
            y = float(self.button1_y_edit.text())
            y = round(y, 7)
            self.piste_1.set_y(y)
            self.piste_1_y_set = True


    def piste_2_input_x(self):
        if (not self.piste_2_x_set):
            x = float(self.button2_x_edit.text())
            x = round(x, 7)
            self.piste_2.set_x(x)
            self.piste_2_x_set = True
            y = self.piste_2.get_xy()[1]
            self.button12.setText("Piste B: \n N: {} \n E: {}".format(y, x))
    def piste_2_input_y(self):
        if (not self.piste_2_y_set):
            y = float(self.button2_y_edit.text())
            y = round(y, 7)
            self.piste_2.set_y(y)
            self.piste_2_y_set = True


    def set_point_xy(self, x, y):
        """
        Tällä asetetaan x ja y arvot valituksi pisteeksi A tai B, jos niitä ei ole vielä asetettu.
        """
        x = round(x, 7)
        y = round(y, 7)

        while(True):

            if (self.piste_1_x_set and self.piste_1_y_set and self.piste_2_x_set and self.piste_2_y_set):
                break

            if ((not self.piste_1_x_set) and (not self.piste_1_y_set)):
                self.button1_x_edit.setText(str(x))
                self.button1_y_edit.setText(str(y))
                self.piste_1.set_x(x)
                self.piste_1.set_y(y)
                self.piste_1_x_set = True
                self.piste_1_y_set = True
                self.button11.setText("Piste A: \n N: {} \n E: {}".format(y, x))
                break

            if ((not self.piste_2_x_set) and (not self.piste_2_y_set)):
                self.button2_x_edit.setText(str(x))
                self.button2_y_edit.setText(str(y))
                self.piste_2.set_x(x)
                self.piste_2.set_y(y)
                self.piste_2_x_set = True
                self.piste_2_y_set = True
                self.button12.setText("Piste B: \n N: {} \n E: {}".format(y, x))
                break

    def mousePressEvent(self, e):
        """
        tämä metodi käsittelee hiiren napsautuksia punaisella suorakulmiolla merkityn alueen sisällä.
        Onnistuneet napsautukset asetetaan valituiksi A tai B pisteiksi, jos niitä ei ole ennestään asetettu.
        """
        # pikseliarvot välillä 815 > x > 465 ja -130 > y > -527 ovat hyväksyttäviä, ja ne muunnetaan koordinaateiksi.
        # mitattu x pikseli-väli = 350, y pixeli-väli 397 pikseliä.
        # muulloin x = 0, y = 0

        # x kasvaa merkityllä alueella 0.023302300000000997 astetta, y kasvaa 0.013229799999997738 astetta
        x_deg_per_px = 0.023302300000000997 / 350 # == 0.000066578
        y_deg_per_px = 0.013229799999997738 / 397 # == 0.00003332443325

        x = int(e.position().x())
        y = int(e.position().y()) * (-1)    # hiiren y-arvot kasvavat ylhäältä alas, kun taas koordinaatit päinvastoin
                                            # joten y-arvot kerrotaan -1:llä.

        # nollataan klikkauksen koordinaatit alueen ulkopuolella
        if (x < 465) or (x > 815):
            x = 0
            y = 0
        elif (y < -527) or (y > -131):
            y = 0
            x = 0

        # asetetaan klikkauksen koordinaatit kaavalla (koordinaatit -/+ rajakoordinaatit) * astetta per pikseli + alueen x/y minimiarvot
        else:
            x = (x - 465) * x_deg_per_px + self.min_x
            y = (y + 527) * y_deg_per_px + self.min_y

        y = round(y, 7)
        x = round(x, 7)

        text = 'Viimeisimmän napsautuksen koordinaatit N: {0},  E: {1}'.format(y, x)
        self.button3.setText(text)

        # napsautuksesn ollessa sallituilla arvoilla asetetaan xy-arvot valituksi pisteeksi.
        if (x == 0 or y == 0):
            pass
        else:
            self.set_point_xy(x,y)

    def etsi_lahin_piste(self):
        """
        etsii annettua pistettä lähimmän tien päätepisteen.
        Oletusarvoisesti tielle voi mennä ainoastaan sen päätepisteistä.
        """

        a = self.piste_1
        b = self.piste_2

        laskuri = Etaisyyslaskuri("lasku")
        closest_a = None
        closest_b = None

        smallest_a = float('inf')
        smallest_b = float('inf')

        for i in self.dijkstra_verkko:
            xy = i.get_koord()

            etaisyys_a = laskuri.laske(xy, a)
            etaisyys_b = laskuri.laske(xy, b)

            if (etaisyys_a < smallest_a):
                closest_a = i
                smallest_a = etaisyys_a
            if (etaisyys_b < smallest_b):
                closest_b = i
                smallest_b = etaisyys_b

        return closest_a, closest_b, smallest_a, smallest_b

    def dijkstraa(self):
        """
        Tässä etsitään reitit valittujen pisteiden välille käyttäen Dijkstran algoritmia.

        """
        if (not self.piste_1_x_set) or (not self.piste_1_y_set) or (not self.piste_2_x_set) or (not self.piste_2_y_set):
            print('pisteet tulee valita ennen reitin laskemista!')
            return 0

        # Alkuun asetetaan parametrit valintojen perusteella.

        kevyt = self.button8.isChecked()
        raskas = self.button9.isChecked()
        lyhyin = self.button6.isChecked()
        nopein = self.button7.isChecked()

        if (not kevyt) and (not raskas):
            print("väylistä on oltava edes yksi valittuna!")
            return 0

        if (lyhyin):
            paino = 0
        elif(nopein):
            paino = 1
        else:
            paino = 99

        if (kevyt and raskas):
            luokka = 0

        elif (kevyt and not raskas):
            luokka = 2

        elif (not kevyt and raskas):
            luokka = 1
        else:
            luokka = 99

        piste_a, piste_b, eta_a, eta_b = self.etsi_lahin_piste()

        # Seuraavaksi suoritetaan algoritmi sille tehdyllä oliolla.

        edsger = Dijkstra(self.dijkstra_verkko)     # Nimetty algoritmin kehittäneen Edsger Dijkstran mukaan

        virityspuu = edsger.algoritmi(piste_a, paino, luokka)  # virityspuu on muotoa {Koordinaatti: dijkstrapiste}

        viimeinen_piste = virityspuu[piste_b.get_koord()]

        edsgerin_polku = []

        this_piste = viimeinen_piste

        # käydään läpi virityspuu aloittaen viimeisestä pisteestä loikaten aina pisteelle annettuun vanhempaan.
        # saavutettua aloituspisteen, lopetetaan läpikäynti ja reitti on valmis.

        while(True):

            if (this_piste == piste_a):
                break
            if (this_piste == None):
                break

            edsgerin_polku.append(this_piste)

            if (not virityspuu[this_piste.get_koord()].get_vanhempi == None):
                this_piste = virityspuu[this_piste.get_koord()].get_vanhempi()
            else:
                break

        # korostetaan reitti kartasta, ja ilmoitetaan reitin tiedot käyttäjälle.
        self.paint_dijkstrat(edsgerin_polku)

        pituus = 0
        aika = 0

        for i in edsgerin_polku:
            pituus = pituus + (i.get_eta() / 10)
            aika = aika + (i.get_aika_vanhempaan() * 60)

        pituus = round(pituus, 2)
        aika = round(aika, 2)

        teksti = "Reitin pituus: {} km \n Reitin aika: {} minuuttia".format(pituus, aika)

        self.button25.setText(teksti)

    def paint_all_roads(self, poikkeukset=0, tiet=None):
        """
        Tällä piirretään kaikki tiet kartalle.
        poikkeukset ja tiet -paramtreilla voisi värittää jotkin tiet eri värisiksi, mutta se on toteutettu toisilla tavoin.
        """

        for i in self.verkko.get_roads():
            edellinen = None

            for n in i.get_koordinaatit():

                if (edellinen):
                    if (poikkeukset > 0):
                        if (i in tiet):
                            self.paint_road_seg(edellinen, n, i.get_autoiltava(), 1)
                        else:
                            self.paint_road_seg(edellinen, n, i.get_autoiltava())
                    else:
                        self.paint_road_seg(edellinen, n, i.get_autoiltava())
                    edellinen = n
                else:
                    edellinen = n

    def paint_dijkstrat(self, edsgerin_polku):
        """
        Tällä väritetään Dijkstran algoritmilla löydetty lyhyin polku. Valitettavasti lopputulos vaatii käyttäjältä
        hieman 'Mielikuvituksen käyttöä'

        """
        edellinen = None

        for i in edsgerin_polku:

            if (edellinen):
                koord_a = edellinen.get_koord()
                koord_b = i.get_koord()
                self.paint_road_seg(koord_a, koord_b, True, 1,2)
                edellinen = i
            else:
                edellinen = i

    def paint_road_seg(self, koord_a, koord_b, luokka, vari=0, lev=1):
        """
        piirtää tiesegmentin koordinaattien pisteiden a ja b välille

        vari on tien väriin vaikuttava vapaaehtoinen parametri, jonka arvon ollessa muu kuin 0, tie väritetään punaisella.
        default arvo tälle on 0, jolloin autotiet mustalla ja kevyenliikenteen väylät vihreällä.

        """
        a = koord_a.skaalaa_koordinaatit()      # X * 15000
        b = koord_b.skaalaa_koordinaatit()      # Y * 30000

        a_x = (self.min_x - a[0]) * -1       # x -koordinaatit pitää kääntää johtuen pyqt:n erilaisesta koordinaatistosta
        a_y = (self.min_y - a[1])

        b_x = (self.min_x - b[0]) * -1
        b_y = (self.min_y - b[1])

        line = QGraphicsLineItem(a_x, a_y, b_x, b_y)
        pen = QPen()  # luodaan kynä

        if (vari == 0):
            if (luokka):                    # väritetään kevyenliikenteen väylät vihreällä
                color = QColor(0, 0, 0)
            else:
                color = QColor(0, 200, 0)
        else:
            color = QColor(200,0,0)

        pen.setColor(color)
        pen.setWidthF(lev)  # asetetaan sille leveys
        line.setPen(pen)  # asetetaan viivalle kynä
        self.scene.addItem(line)

    def paint_borders(self):
        """
        Tällä piirretään punainen laatikko tarkasteltavan alueen ympärille.
        Tämä mahdollisti koordinaattien käytön hieman paremmin.
        """
        top_left = Koordinaatti(self.min_x, self.max_y)
        top_right = Koordinaatti(self.max_x, self.max_y)
        bot_left = Koordinaatti(self.min_x, self.min_y)
        bot_right = Koordinaatti(self.max_x, self.min_y)

        a = top_left.skaalaa_koordinaatit()      # X * 15000
        b = top_right.skaalaa_koordinaatit()      # Y * 30000
        c = bot_right.skaalaa_koordinaatit()
        d = bot_left.skaalaa_koordinaatit()

        ax = self.min_x - a[0] * (- 1) - 50     # jostain syystä x-arvot heittää 50 pikseliä
        ay = self.min_y - a[1]

        bx = self.min_x - b[0] * (- 1) - 50
        by = self.min_y - b[1]

        cx = self.min_x - c[0] * (- 1) - 50
        cy = self.min_y - c[1]

        dx = self.min_x - d[0] * (- 1) - 50
        dy = self.min_y - d[1]

        topline = QGraphicsLineItem(ax, ay, bx, by)
        rightline = QGraphicsLineItem(bx, by, cx, cy)
        botline = QGraphicsLineItem(cx, cy, dx, dy)
        leftline = QGraphicsLineItem(ax, ay, dx, dy)
        pen = QPen()  # luodaan kynä

        color = QColor(200,0,0)

        pen.setColor(color)
        pen.setWidthF(1)  # asetetaan sille leveys
        topline.setPen(pen)  # asetetaan viivalle kynä
        botline.setPen(pen)  # asetetaan viivalle kynä
        rightline.setPen(pen)  # asetetaan viivalle kynä
        leftline.setPen(pen)  # asetetaan viivalle kynä

        self.scene.addItem(topline)
        self.scene.addItem(botline)
        self.scene.addItem(rightline)
        self.scene.addItem(leftline)

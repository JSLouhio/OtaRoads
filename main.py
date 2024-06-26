from roadreader import *
import sys
from PyQt6.QtWidgets import QApplication
from tieverkko import Tieverkko
from otaroadsGUI import *


def main():

    lukija = Roadreader()

    lukija.lue_pilkuin_eroteltu_tiedosto('otaniemi_roads.csv')

    tiet = Tieverkko(lukija.get_roads())

    min_x = lukija.get_extent()[1]
    min_y = lukija.get_extent()[3]
    max_x = lukija.get_extent()[0]
    max_y = lukija.get_extent()[2]

    dijkstrat = lukija.luo_dijkstrat()

    app = QApplication(sys.argv)
    window = Window(min_x, min_y, max_x, max_y, tiet, dijkstrat)

    window.paint_all_roads()
    window.paint_borders()

    sys.exit(app.exec())


main()


class Koordinaatti:
    """
    Yksinkertainen olio-luokka kuvastamaan koordinaattipisteitä.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_xy(self):
        tupla = (self.x, self.y)
        return tupla

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def __repr__(self):
        x = str(self.x)
        y = str(self.y)

        return "X:{},Y:{}".format(x, y)

    def skaalaa_koordinaatit(self):
        """
            Koordinaatteja pitää skaalata isommiksi, jotta ne näkyisivät järkevästi piirrettyinä.
        """
        new_x = self.x * 15000  # X-arvoa skaalataan puolet Y:n arvosta, sillä 60-leveyspiirin tienoilla X-arvo
        new_y = self.y * 30000  # kasvaa Y:n suhteen suunnilleen tahtia cos(60) = 0.5

        return (new_x, new_y)

    # nämä kolme metodia auttavat koordinaattien vertailussa toisiin koordinaatteihin
    def __key(self):
        return (self.x, self.y)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Koordinaatti):
            return self.__key() == other.__key()



import math

class Etaisyyslaskuri:
    """
    Tämän luokan avulla voidaan laskea etäisyyksiä kahden pisteen välillä.
    """
    def __init__(self, nimi):
        self.nimi = nimi        # Nimeä ei oikeasti tarvita, mutta olkoon kuitenkin.

    def laske(self, koord_a, koord_b):
        """
        Laskee ja palauttaa etäisyyden kahden pisteen välillä (Kilometreinä)
        """

        a = koord_a.get_xy()
        x1 = a[0]
        y1 = a[1]

        b = koord_b.get_xy()
        x2 = b[0]
        y2 = b[1]

        lat1 = x1 * math.pi / 180
        lon1 = y1 * math.pi / 180
        lat2 = x2 * math.pi / 180
        lon2 = y2 * math.pi / 180

        rads = math.acos(0.5 * ((1.0 + math.cos(lon1 - lon2)) * math.cos(lat1 - lat2) - (1.0 - math.cos(lon1 - lon2)) *
                                math.cos(lat1 + lat2)))
        dist = 6371 * rads

        return dist
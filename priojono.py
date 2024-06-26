class Priojono:
    """
    Tämä luokka toteuttaa prioriteettijono -tietorakenteen. Annetuille esineille on asetettu jokin prioriteetti
    (tässä tapauksessa numero).

    get -metodilla olio palauttaa pienimmän prioriteetin omaavan esineen prioriteetteineen, ja poistaa ne listaltaan.

    """
    def __init__(self):

        self.jono = [] # [esine, prioriteetti]

    def lisaa(self, jonotettava):
        self.jono.append(jonotettava)

    def get(self):
        min = float('inf')
        pienin = None

        index = 0
        index_to_delete = 0

        for i in self.jono:
            for a in i.keys():
                avain = a
            if i[avain] < min:
                pienin = avain
                min = i[avain]
                index_to_delete = index
            index += 1

        del self.jono[index_to_delete]

        return pienin, min

    def is_empty(self):

        return len(self.jono) == 0




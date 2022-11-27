
from . import regles
from . import ligne

class Revenu:
    def __init__(self, montant):
        self.montant = montant


class TraitementBrut(Revenu):
    def __init__(self, indice):
        super().__init__(indice * regles.valeur_point_indice)
        self.indice = indice

        

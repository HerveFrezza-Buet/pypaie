
from . import regles
from . import ligne

class Revenu(ligne.Ligne):
    def __init__(self, label, montant):
        super().__init__(label)
        self.montant = montant


class TraitementBrut(Revenu):
    def __init__(self, montant):
        super().__init__('Traitement brut', montant)
        
    def _brut(self):
        return self.montant
    
class TraitementIndiciaireBrut(TraitementBrut):
    def __init__(self, indice):
        super().__init__(indice * regles.valeur_point_indice)
        self.indice = indice


    

        

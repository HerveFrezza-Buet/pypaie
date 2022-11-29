from . import regles
from . import ligne

class Retrait(ligne.Ligne):
    def __init__(self, label, montant):
        super().__init__(label)
        self.montant = montant
        
    def cotise(self, assiettes, mode):
        pass
    
    def _cotisation_salariale(self):
        return self.montant

    def lignes(self):
        return [{'label': 'Régularisation accompte',
                 'salarial': self.montant}]

class RegularisationAccompte(Retrait):
    def __init__(self, montant):
        super().__init__('Régulatisation accompte', montant)
    

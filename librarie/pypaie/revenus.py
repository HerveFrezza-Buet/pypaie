
from . import regles
from . import ligne

class Revenu(ligne.Ligne):
    def __init__(self, label, montant):
        super().__init__(label)
        self.montant = montant


class TraitementBrut(Revenu):
    def __init__(self, montant):
        super().__init__('Traitement brut', montant)

    def cotise(self, assiettes):
        assiettes.cotisation_traitement_brut(self._brut(), mode)
        
    def _brut(self):
        return self.montant
    
class TraitementIndiciaireBrut(TraitementBrut):
    def __init__(self, indice):
        super().__init__(indice * regles.valeur_point_indice)
        self.indice = indice

class IndemniteResidence(Revenu):
    def __init__(self, taux, traitement_brut):
        self.taux = taux * .01
        super().__init__('Indemnité de résidence', traitement_brut._brut() * self.taux)
        
    def cotise(self, assiettes):
        assiettes.cotisation_traitement_brut(self._brut(), mode)
        
    def _brut(self):
        return self.montant
    
class IndemniteDifficultesAdministratives(Revenu):
    def __init__(self, indice):
        super().__init__('Indemnité difficultés administratives', regles.indemnite_difficultes_administratives(indice))
        
    def cotise(self, assiettes):
        assiettes.cotisation_traitement_brut(self._brut(), mode)
        
    def _brut(self):
        return self.montant
        
class IndemniteCompensationHausseCSG(Revenu):
    def __init__(self, montant):
        super().__init__('Indemnité de compensation hausse CSG', montant)
        
    def cotise(self, assiettes):
        assiettes.cotisation_traitement_brut(self._brut(), mode)
        
    def _brut(self):
        return self.montant

class RemboursementPSC(Revenu):
    def __init__(self):
        super().__init__('Remboursement forfaitaire de la protection sociale complémentaire', regles.remboursement_forfaitaire_psc)
        
    def cotise(self, assiettes):
        assiettes.cotisation_psc(self._brut(), mode)
        
    def _brut(self):
        return self.montant

        

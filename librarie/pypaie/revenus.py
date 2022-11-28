
from . import regles
from . import ligne

class Revenu(ligne.Ligne):
    def __init__(self, label, montant):
        super().__init__(label)
        self.montant = montant


class TraitementBrut(Revenu):
    def __init__(self, montant):
        super().__init__('Traitement brut', montant)

    def cotise(self, assiettes, mode):
        assiettes.cotisation_traitement_brut(self._brut())
        
    def _brut(self):
        return self.montant
    
class TraitementIndiciaireBrut(TraitementBrut):
    def __init__(self, indice):
        super().__init__(indice * regles.valeur_point_indice)
        self.indice = indice

class SupplementFamilial(Revenu):
    def __init__(self, montant):
        super().__init__('Supplément familial de traitement', montant)

    def cotise(self, assiettes, mode):
        assiettes.cotisation_indemnites(self._brut(), mode)
        
    def _brut(self):
        return self.montant

class RemboursementTransport(Revenu):
    def __init__(self, montant):
        self.montant = montant
        super().__init__(f'Remboursement Domicile-Travail', self.montant)
        
    def cotise(self, assiettes, mode):
        assiettes.cotisation_remboursement_transport(self._brut())
        
    def _brut(self):
        return self.montant

        
class IndemniteResidence(Revenu):
    def __init__(self, taux, traitement_brut):
        self.taux = taux * .01
        super().__init__(f'Indemnité de résidence (taux={taux}%)', traitement_brut._brut() * self.taux)
        
    def cotise(self, assiettes, mode):
        assiettes.cotisation_indemnites(self._brut(), mode)
        
    def _brut(self):
        return self.montant
    
class IndemniteDifficultesAdministratives(Revenu):
    def __init__(self, indice):
        super().__init__('Indemnité difficultés administratives', regles.indemnite_difficultes_administratives(indice))
        
    def cotise(self, assiettes, mode):
        assiettes.cotisation_indemnites(self._brut(), mode)
        
    def _brut(self):
        return self.montant
        
class IndemniteCompensationHausseCSG(Revenu):
    def __init__(self, montant):
        super().__init__('Indemnité de compensation hausse CSG', montant)
        
    def cotise(self, assiettes, mode):
        assiettes.cotisation_indemnites(self._brut(), mode)
        
    def _brut(self):
        return self.montant

class RemboursementPSC(Revenu):
    def __init__(self):
        super().__init__('Remboursement forfaitaire de la protection sociale complémentaire', regles.remboursement_forfaitaire_psc)
        
    def cotise(self, assiettes, mode):
        assiettes.cotisation_psc(self._brut())
        
    def _brut(self):
        return self.montant


class Prime(Revenu):
    def __init__(self, label, montant, mode):
        super().__init__(label, montant)
        self.mode = mode
        
    def cotise(self, assiettes, mode):
        assiettes.cotisation_prime(self._brut(), self.mode)
        
    def _brut(self):
        return self.montant
    
class PrimePublic(Prime):
    def __init__(self, label, montant):
        super().__init__(label, montant, regles.MODE_PUBLIC)
        
class IndemniteFonctions(PrimePublic):
    def __init__(self, montant):
        super().__init__('Indemnité de fonctions', montant)
    

class TransfertPrimesPoints(Revenu):
    def __init__(self, montant):
        super().__init__('Transfert primes/points', montant)

    def cotise(self, assiettes, mode):
        assiettes.cotisation_transfert_primes_points(self.montant)
        
    def _cotisation_salariale(self):
        return self.montant

    def lignes(self):
        return [{'label': self.label,
                 'salarial' : self.montant}]

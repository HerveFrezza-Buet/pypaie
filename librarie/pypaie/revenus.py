
from . import regles

TYPE_BRUT_SALARIAL = 'brut salarial'
TYPE_INDEMNITE = 'indemnite'

TAG_TRAITEMENT_BRUT = 'traitement brut'
TAG_INDEMNITE_RESIDENCE = 'indemnité de résidence'
TAG_INDEMNITE_DIFFICULTES_ADMINISTRATIVES = 'indemnité pour difficultés administratives'
TAG_INDEMNITE_COMPENSATION_HAUSSE_CSG = 'indemnité de compensation de la hausse CSG'
TAG_REMBOURSEMENT_FORFAITAIRE_PSC = 'remboursement forfaitaire de la protection sociale complémentaire'



# Traitement brut
def traitement_brut(montant=None, indice=None):
    """
    Préciser l'un ou l'autre:
    - montant: montant du traitement brut salarial
    - indice: l'indice de la fonction publique
    """
    if montant is None:
        if indice is None:
            raise ValueError('pypaie.revenu.traitement_brut: le montant ou la paire (indice, valeur_point) doivent être précisés.')
        montant = regles.valeur_point_indice* indice
    return {'type': TYPE_BRUT_SALARIAL,
            'libelle': TAG_TRAITEMENT_BRUT,
            'montant': montant}

def prime_brute(montant, libelle):
    return {'type': TYPE_BRUT_SALARIAL,
            'libelle': libelle,
            'montant': montant}

# Indemnite pour difficultés administratives
def indemnite_pour_difficultes_administratives(indice):
    return {'type': TYPE_BRUT_SALARIAL,
            'libelle': TAG_INDEMNITE_DIFFICULTES_ADMINISTRATIVES,
            'montant': regles.ind_diff_adm(indice)}

def indemnite_de_residence():
    return {'type': TYPE_BRUT_SALARIAL,
            'libelle': TAG_INDEMNITE_RESIDENCE}

def indemnite_hausse_CSG(montant):
    return {'type': TYPE_BRUT_SALARIAL,
            'libelle': TAG_INDEMNITE_COMPENSATION_HAUSSE_CSG,
            'montant': montant}

def remboursement_psc():
    return {'type': TYPE_INDEMNITE,
            'libelle': TAG_REMBOURSEMENT_FORFAITAIRE_PSC,
            'montant': regles.remboursement_forfaitaire_psc}



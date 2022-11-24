
from . import regles

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
    return {'libelle': TAG_TRAITEMENT_BRUT,
            'montant': montant,
            'categorie': regles.CATEGORIE_REVENU_TRAITEMENT_BRUT}

def prime(montant, libelle):
    return {'libelle': libelle,
            'montant': montant,
            'categorie': regles.CATEGORIE_REVENU_PRIME}

# Indemnite pour difficultés administratives
def indemnite_pour_difficultes_administratives(indice):
    return {'libelle': TAG_INDEMNITE_DIFFICULTES_ADMINISTRATIVES,
            'montant': regles.ind_diff_adm(indice),
            'categorie': regles.CATEGORIE_REVENU_AUTRE}

def indemnite_de_residence():
    return {'libelle': TAG_INDEMNITE_RESIDENCE,
            'categorie': regles.CATEGORIE_REVENU_AUTRE}

def indemnite_hausse_CSG(montant):
    return {'libelle': TAG_INDEMNITE_COMPENSATION_HAUSSE_CSG,
            'montant': montant,
            'categorie': regles.CATEGORIE_REVENU_AUTRE}

def remboursement_psc():
    return {'libelle': TAG_REMBOURSEMENT_FORFAITAIRE_PSC,
            'montant': regles.remboursement_forfaitaire_psc,
            'categorie': regles.CATEGORIE_REVENU_PSC}



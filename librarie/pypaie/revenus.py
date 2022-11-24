
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
            'assiette' : True}

def prime(montant, libelle, inclus_dans_assiette):
    return {'libelle': libelle,
            'montant': montant,
            'assiette' : inclus_dans_assiette}

# Indemnite pour difficultés administratives
def indemnite_pour_difficultes_administratives(indice, inclus_dans_assiette=False):
    return {'libelle': TAG_INDEMNITE_DIFFICULTES_ADMINISTRATIVES,
            'montant': regles.ind_diff_adm(indice),
            'assiette' : inclus_dans_assiette}

def indemnite_de_residence(inclus_dans_assiette=False):
    return {'libelle': TAG_INDEMNITE_RESIDENCE,
            'assiette' : inclus_dans_assiette}

def indemnite_hausse_CSG(montant, inclus_dans_assiette=False):
    return {'libelle': TAG_INDEMNITE_COMPENSATION_HAUSSE_CSG,
            'montant': montant,
            'assiette' : inclus_dans_assiette}

def remboursement_psc(inclus_dans_assiette=False):
    return {'libelle': TAG_REMBOURSEMENT_FORFAITAIRE_PSC,
            'montant': regles.remboursement_forfaitaire_psc,
            'assiette' : inclus_dans_assiette}



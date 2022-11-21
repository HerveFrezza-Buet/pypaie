from . import regles

# Cotisations
VIEILLESSE_PRIVE = 'cotisation vieillesse prive'

# Ensemble des cotisations connues par pypaie
cotisations = set([VIEILLESSE_PRIVE])

TYPE_COTISATION_SOCIALE = 'cotisation sociale'

TAG_VIEILLESSE = 'cotisation vieillesse'

def vieillesse_prive(brut_salarial):
    tranche_1, tranche_2, _ = regles.calcul_tranches_cotisation_vieillesse(brut_salarial)
    cotisations = []

    tag = ' '.join([TAG_VIEILLESSE, 'plafonnée'])
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                       'libelle': tag,
                       'salarial': regles.taux_vieillesse_salarial_plafonnee * tranche_1,
                       'patronal': regles.taux_vieillesse_patronal_plafonnee * tranche_1})
    
    tag = ' '.join([TAG_VIEILLESSE, 'deplafonnée'])
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': tag,
                        'salarial': regles.taux_vieillesse_salarial_deplafonnee * brut_salarial,
                        'patronal': regles.taux_vieillesse_patronal_deplafonnee * brut_salarial})

    return cotisations
    
    


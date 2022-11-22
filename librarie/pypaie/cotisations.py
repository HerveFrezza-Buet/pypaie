from . import regles

# Cotisations
VIEILLESSE_PRIVE = 'cotisation vieillesse prive'
AGIRC_ARRCO = 'complementaire vieillesse AGIRC-ARRCO'
IRCANTEC = 'complementaire vieillesse IRCANTEC'
CSG_CRDS = 'CSG CRDS'
MALADIE_REGIME_GENERAL = 'cotisation maladie'
MALADIE_REGIME_LOCAL = 'cotisation maladie (local)'
ALLOCATIONS_FAMILIALES = 'allocations familiales'

# Ensemble des cotisations connues par pypaie
cotisations = set([VIEILLESSE_PRIVE, AGIRC_ARRCO, IRCANTEC, CSG_CRDS, MALADIE_REGIME_GENERAL, MALADIE_REGIME_LOCAL, ALLOCATIONS_FAMILIALES])

TYPE_COTISATION_SOCIALE = 'cotisation sociale'

TAG_VIEILLESSE = 'cotisation vieillesse'
TAG_AGIRC_ARRCO = 'cotisation compl. vieillesse AGIRC-ARRCO'
TAG_IRCANTEC = 'cotisation compl. vieillesse IRCANTEC'
TAG_CSG_NONIMP = 'CSG déductible'
TAG_CSG_IMP = 'CSG imposable'
TAG_CRDS = 'CRDS'
TAG_MALADIE_GENERAL = 'cotisation maladie'
TAG_MALADIE_LOCAL = 'cotisation maladie ALS/MOS'
TAG_ALLOCATIONS_FAMILIALES = 'allocations familiales'



def vieillesse_prive(brut_salarial):
    tranche_1, tranche_2 = regles.calcul_tranches_cotisation_vieillesse(brut_salarial)
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
    
    
def agirc_arrco(brut_salarial):
    tranche_1, tranche_2 = regles.calcul_tranches_agirc_arrco(brut_salarial)
    cotisations = []

    tag = ' '.join([TAG_AGIRC_ARRCO, 'T1'])
    
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': tag,
                        'salarial': regles.taux_agirc_arrco_tranche_1 * regles.part_salariale_agirc_arrco * tranche_1,
                        'patronal': regles.taux_agirc_arrco_tranche_1 * regles.part_patronale_agirc_arrco * tranche_1})
    
    tag = ' '.join([TAG_AGIRC_ARRCO, 'T2'])
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': tag,
                        'salarial': regles.taux_agirc_arrco_tranche_2 * regles.part_salariale_agirc_arrco * tranche_2,
                        'patronal': regles.taux_agirc_arrco_tranche_2 * regles.part_patronale_agirc_arrco * tranche_2})

    return cotisations


def ircantec(brut_salarial):
    tranche_1, tranche_2 = regles.calcul_tranches_ircantec(brut_salarial)
    cotisations = []

    tag = ' '.join([TAG_IRCANTEC, 'TA'])
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': tag,
                        'salarial': regles.taux_ircantec_salarial_tranche_a * tranche_1,
                        'patronal': regles.taux_ircantec_patronal_tranche_a * tranche_1})
    
    tag = ' '.join([TAG_IRCANTEC, 'TB'])
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': tag,
                        'salarial': regles.taux_ircantec_salarial_tranche_b * tranche_2,
                        'patronal': regles.taux_ircantec_patronal_tranche_b * tranche_2})

    return cotisations

def csg_crds(brut_salarial):
    assiette = regles.calcul_assiette_csg_crds(brut_salarial)
    cotisations = []
    
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': TAG_CSG_IMP,
                        'salarial': regles.taux_csg_imp_salarial * assiette,
                        'patronal': 0.0})
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': TAG_CSG_NONIMP,
                        'salarial': regles.taux_csg_nonimp_salarial * assiette,
                        'patronal': 0.0})
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': TAG_CRDS,
                        'salarial': regles.taux_crds_salarial * assiette,
                        'patronal': 0.0})

    return cotisations

def maladie_regime_general(brut_salarial):
    cotisations = []
    tag = TAG_ALLOCATIONS_FAMILIALES
    if reduit:
        taux = regles.taux_allocations_familiales_patronal_reduit
        tag += ' (taux reduit)'
    else:
        taux = regles.taux_allocations_familiales_patronal
        tag += ' (taux plein)'
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': TAG_MALADIE_GENERAL,
                        'salarial': 0.0,
                        'patronal': regles.taux_maladie_patronal_general * brut_salarial})
    return cotisations
    

def maladie_regime_local(brut_salarial):
    cotisations = maladie_regime_general(brut_salarial)
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': TAG_MALADIE_LOCAL,
                        'salarial': regles.taux_maladie_salarial_local * brut_salarial,
                        'patronal': 0.0})
    return cotisations


def allocations_familiales(brut_salarial, reduit):
    cotisations = []
    tag = TAG_ALLOCATIONS_FAMILIALES
    if reduit:
        taux = regles.taux_allocations_familiales_patronal_reduit
        tag += ' (taux reduit)'
    else:
        taux = regles.taux_allocations_familiales_patronal
        tag += ' (taux plein)'
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': tag,
                        'salarial': 0.0,
                        'patronal': taux * brut_salarial})
    return cotisations

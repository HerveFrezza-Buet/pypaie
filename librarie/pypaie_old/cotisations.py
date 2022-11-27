from . import regles

# Cotisations
VIEILLESSE_PRIVE = 'cotisation vieillesse prive'
CRNACL = 'crnacl'
RAFP = 'rafp'
PC = 'pc'
AGIRC_ARRCO = 'complementaire vieillesse AGIRC-ARRCO'
IRCANTEC = 'complementaire vieillesse IRCANTEC'
CSG_CRDS = 'CSG CRDS'
MALADIE_REGIME_GENERAL = 'maladie'
MALADIE_REGIME_LOCAL = 'maladie Loc'
ALLOCATIONS_FAMILIALES = 'allocations familiales'
ACCIDENTS_TRAVAIL = 'accidents travail'
FNAL = "fond national d'aide au logement"
CNSA = "cnsa"
MOBILITE = "mobilité"
CHOMAGE = 'chômage'
TRANSFERT_PRIMES_POINTS = 'transfert pp'
ATI = 'ati'

# Ensemble des cotisations connues par pypaie
cotisations = set([VIEILLESSE_PRIVE, CRNACL, RAFP, PC, AGIRC_ARRCO, IRCANTEC, CSG_CRDS, MALADIE_REGIME_GENERAL, MALADIE_REGIME_LOCAL, ALLOCATIONS_FAMILIALES, ACCIDENTS_TRAVAIL, FNAL, CNSA, MOBILITE, CHOMAGE, TRANSFERT_PRIMES_POINTS, ATI])

TYPE_COTISATION_SOCIALE = 'cotisation sociale'

TAG_VIEILLESSE = 'cotisation vieillesse'
TAG_CRNACL = 'cotisation retraite CRNACL'
TAG_RAFP = 'cotisation retraite compl. RAFP'
TAG_PC = 'cotisation pension civile (PC)'
TAG_AGIRC_ARRCO = 'cotisation compl. vieillesse AGIRC-ARRCO'
TAG_IRCANTEC = 'cotisation compl. vieillesse IRCANTEC'
TAG_CSG_NONIMP = 'CSG déductible'
TAG_CSG_IMP = 'CSG imposable'
TAG_CRDS = 'CRDS'
TAG_MALADIE_GENERAL = 'cotisation maladie'
TAG_MALADIE_LOCAL = 'cotisation maladie régime local'
TAG_ALLOCATIONS_FAMILIALES = 'cotisation allocations familiales'
TAG_ACCIDENTS_TRAVAIL = 'cotisation accidents du travail'
TAG_FNAL = "cotisation fond national d'aide au logement"
TAG_CNSA = "cotisation caisse nationale de solidarité pour l'autonomie"
TAG_MOBILITE = "versement mobilité"
TAG_CHOMAGE = "cotisation assurance chômage"
TAG_AGS = "cotisation AGS garantie des salaires"
TAG_TRANSFERT_PRIMES_POINTS = 'transfert primes / points'
TAG_ATI = 'contribution ATI'



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
    
def crnacl(brut_salarial):
    cotisations = []
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': TAG_CRNACL,
                        'salarial': regles.taux_crnacl_salarial * brut_salarial,
                        'patronal': regles.taux_crnacl_patronal * brut_salarial})
    return cotisations

def ati(brut_salarial):
    cotisations = []
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': TAG_ATI,
                        'salarial': 0.0,
                        'patronal': regles.taux_ati_patronal * brut_salarial})
    return cotisations

def rafp(traitement_brut, autres_revenus):
    assiette = regles.calcul_assiette_RAFP(traitement_brut, autres_revenus)
    cotisations = []
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': TAG_RAFP,
                        'salarial': regles.taux_rafp_salarial * assiette,
                        'patronal': regles.taux_rafp_patronal * assiette})
    return cotisations
    
def pc(traitement_brut):
    cotisations = []
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': TAG_PC,
                        'salarial': regles.taux_pc_salarial * traitement_brut,
                        'patronal': regles.taux_pc_patronal * traitement_brut})
    return cotisations

def transfert_primes_points(montant):
    cotisations = []
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': TAG_TRANSFERT_PRIMES_POINTS,
                        'salarial': montant,
                        'patronal': 0.0})
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

def maladie_regime_general(brut_salarial, public):
    cotisations = []
    if public:
        cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                            'libelle': TAG_MALADIE_GENERAL,
                            'salarial': 0.0,
                            'patronal': regles.taux_maladie_patronal_public * brut_salarial})
    else:
        cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                            'libelle': TAG_MALADIE_GENERAL,
                            'salarial': 0.0,
                            'patronal': regles.taux_maladie_patronal_prive_reduit * brut_salarial})
        if brut_salarial > regles.seuil_majoration_maladie:
            cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                                'libelle': TAG_MALADIE_GENERAL + ' majoré',
                                'salarial': 0.0,
                                'patronal': regles.taux_maladie_patronal_prive_majoration * brut_salarial})
    return cotisations
    

def maladie_regime_local(brut_salarial):
    cotisations = maladie_regime_general(brut_salarial, False)
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': TAG_MALADIE_LOCAL,
                        'salarial': regles.taux_maladie_salarial_local * brut_salarial,
                        'patronal': 0.0})
    return cotisations


def allocations_familiales(brut_salarial, reduit):
    cotisations = []
    tag = TAG_ALLOCATIONS_FAMILIALES
    if reduit :
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

def accidents_travail(brut_salarial, taux):
    cotisations = []
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': TAG_ACCIDENTS_TRAVAIL,
                        'salarial': 0.0,
                        'patronal': taux * brut_salarial})
    return cotisations

def fnal(brut_salarial, nb_salaries):
    cotisations = []
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': TAG_FNAL,
                        'salarial': 0.0,
                        'patronal': regles.calcul_cotis_fnal(brut_salarial, nb_salaries)})
    return cotisations

def cnsa(brut_salarial):
    cotisations = []
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': TAG_CNSA,
                        'salarial': 0.0,
                        'patronal': regles.taux_cnsa_patronal * brut_salarial})
    return cotisations
    
def mobilite(brut_salarial, taux):
    cotisations = []
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': TAG_MOBILITE,
                        'salarial': 0.0,
                        'patronal': taux * brut_salarial})
    return cotisations

def chomage(brut_salarial):
    cotisations = []
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': TAG_CHOMAGE,
                        'salarial': 0.0,
                        'patronal': regles.taux_chomage_patronal * brut_salarial})
    cotisations.append({'type': TYPE_COTISATION_SOCIALE,
                        'libelle': TAG_AGS,
                        'salarial': 0.0,
                        'patronal': regles.taux_ags_patronal * brut_salarial})
    return cotisations

# SMIC
smic_mensuel_brut = 1645.48

# La valeur en brut salarial du point d'incice.
valeur_point_indice = 4.85003

# calcul de l'indemnite pour difficultés administratives
def ind_diff_adm(indice):
    if indice <= 341:
        return 1.83
    if indice <= 770:
        return 2.28
    return 3.05

# Un remboursement mensuel forfaitaire de la protection sociale complémentaire
remboursement_forfaitaire_psc = 15.00
    
# Plafond mensuel de la Sécurité sociale (brut salarial)
plafond_securite_sociale = 3428

# calcul retraite privé securite sociale
def calcul_tranches_cotisation_vieillesse(brut_salarial):
    tranche_1 = min(brut_salarial, plafond_securite_sociale)
    tranche_2 = 0 # comme ça ça fait vraiment 0, pas de soucis d'arrondis.
    if brut_salarial > plafond_securite_sociale:
        tranche_2 = min(brut_salarial, 8*plafond_securite_sociale) - tranche_1
    return tranche_1, tranche_2

taux_vieillesse_salarial_plafonnee   = 0.069
taux_vieillesse_patronal_plafonnee   = 0.0855

taux_vieillesse_salarial_deplafonnee = 0.004
taux_vieillesse_patronal_deplafonnee = 0.019

# calcul retraite privée complementaire AGIRC-ARRCO

def calcul_tranches_agirc_arrco(brut_salarial):
    return calcul_tranches_cotisation_vieillesse(brut_salarial)

taux_agirc_arrco_tranche_1 = 0.0787
taux_agirc_arrco_tranche_2 = 0.2159
part_salariale_agirc_arrco = 0.4
part_patronale_agirc_arrco = 1 - part_salariale_agirc_arrco


# calcul retraite pubplique complementaire IRCANATEC

def calcul_tranches_ircantec(brut_salarial):
    return calcul_tranches_cotisation_vieillesse(brut_salarial)

taux_ircantec_salarial_tranche_a = 0.028
taux_ircantec_patronal_tranche_a = 0.042

taux_ircantec_salarial_tranche_b = 0.0695
taux_ircantec_patronal_tranche_b = 0.1255

# calcul CSG-CRDS

taux_csg_abattement      = 0.9825
taux_csg_imp_salarial    = 0.024
taux_csg_nonimp_salarial = 0.068
taux_crds_salarial       = 0.005
def calcul_assiette_csg_crds(brut_salarial):
    tranche_1 = min(brut_salarial, 4*plafond_securite_sociale)
    tranche_2 = 0 # comme ça ça fait vraiment 0, pas de soucis d'arrondis.
    if brut_salarial > 4*plafond_securite_sociale:
        tranche_2 = brut_salarial - tranche_1
    return tranche_1 * taux_csg_abattement + tranche_2


# calcul maladie
taux_maladie_patronal_general_reduit     = .07
taux_maladie_patronal_general_majoration = .06
taux_maladie_salarial_local              = .013
seuil_majoration_maladie                 = 2.5 * smic_mensuel_brut

# calcul familial
taux_allocations_familiales_patronal        = .0525
taux_allocations_familiales_patronal_reduit = taux_allocations_familiales_patronal - 0.018

# calcul accident
taux_accident_travail_patronal        = .0525

# calcul FNAL
seuil_nb_salaries_fnal = 50
def calcul_cotis_fnal(brut_salarial, nb_salaries):
    if nb_salaries < 50:
        return 0.001 * min(brut_salarial, plafond_securite_sociale)
    return 0.005 * brut_salarial

# calcul Solidarité autonomie
taux_cnsa_patronal = 0.003


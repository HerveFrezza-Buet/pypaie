MODE_PRIVE = 'privé'
MODE_PUBLIC = 'public'

REGIME_GENERAL = 'général'
REGIME_LOCAL   = 'local'


# Plafond mensuel de la Sécurité sociale (brut salarial)
plafond_securite_sociale = 3428

# SMIC
smic_mensuel_brut = 1645.48

# La valeur en brut salarial du point d'incice.
valeur_point_indice = 4.85003

# Indemnite pour difficultés administratives
def indemnite_difficultes_administratives(indice):
    if indice <= 341:
        return 1.83
    if indice <= 770:
        return 2.28
    return 3.04

# Un remboursement mensuel forfaitaire de la protection sociale complémentaire
remboursement_forfaitaire_psc = 15.00


# calcul CSG-CRDS
taux_csg_abattement      = 0.9825
taux_csg_imp_salarial    = 0.024
taux_csg_nonimp_salarial = 0.068
taux_crds_salarial       = 0.005

def calcul_assiette_csg_crds(assiette):
    tranche_1 = min(assiette, 4*plafond_securite_sociale)
    tranche_2 = 0 # comme ça ça fait vraiment 0, pas de soucis d'arrondis.
    if assiette > 4*plafond_securite_sociale:
        tranche_2 = assiette - tranche_1
    return tranche_1 * taux_csg_abattement + tranche_2


# calcul maladie
taux_maladie_patronal_prive_reduit     = .07
taux_maladie_patronal_prive_majoration = .06
taux_maladie_patronal_public           = .097
taux_maladie_salarial_local            = .013
seuil_majoration_maladie               = 2.5 * smic_mensuel_brut

def calcul_cotis_maladie(assiette, mode, regime):
    cotis_majoree = None
    cotis_salariale = None
    if mode == MODE_PUBLIC:
        cotis_non_majoree = assiette * taux_maladie_patronal_public
    else:
        cotis_non_majoree = assiette * taux_maladie_patronal_prive_reduit
        if assiette > seuil_majoration_maladie:
            cotis_majoree = assiette * taux_maladie_patronal_prive_majoration

    if regime != REGIME_GENERAL:
        cotis_salariale = assiette * taux_maladie_salarial_local
        
    return cotis_non_majoree, cotis_majoree, cotis_salariale

# calcul chomage
taux_chomage_patronal = 0.0405
taux_ags_patronal     = 0.0015
def calcul_assiette_chomage(assiette):
    return min(assiette, 4*plafond_securite_sociale)

# calcul retraite privé securite sociale

taux_vieillesse_salarial_plafonnee   = 0.069
taux_vieillesse_patronal_plafonnee   = 0.0855

taux_vieillesse_salarial_deplafonnee = 0.004
taux_vieillesse_patronal_deplafonnee = 0.019

def calcul_tranches_vieillesse(assiette):
    tranche_1 = min(assiette, plafond_securite_sociale)
    tranche_2 = 0 # comme ça ça fait vraiment 0, pas de soucis d'arrondis.
    if assiette > plafond_securite_sociale:
        tranche_2 = min(assiette, 8*plafond_securite_sociale) - tranche_1
    return tranche_1, tranche_2

def calcul_cotis_vieillesse(assiette):
    A, B = calcul_tranches_vieillesse(assiette)
    AB   = A+B
    return A  * taux_vieillesse_salarial_plafonnee,  \
           A  * taux_vieillesse_patronal_plafonnee,  \
           AB * taux_vieillesse_salarial_deplafonnee,\
           AB * taux_vieillesse_patronal_deplafonnee

# calcul retraite pubplique complementaire IRCANTEC

taux_ircantec_salarial_tranche_a = 0.028
taux_ircantec_patronal_tranche_a = 0.042

taux_ircantec_salarial_tranche_b = 0.0695
taux_ircantec_patronal_tranche_b = 0.1255

def calcul_tranches_ircantec(assiette):
    return calcul_tranches_vieillesse(assiette)

def calcul_cotis_ircantec(assiette):
    A, B = calcul_tranches_ircantec(assiette)
    return A  * taux_ircantec_salarial_tranche_a, \
           A  * taux_ircantec_patronal_tranche_a, \
           B  * taux_ircantec_salarial_tranche_b, \
           B  * taux_ircantec_patronal_tranche_b 

# calcul retraite privée complementaire AGIRC-ARRCO

taux_agirc_arrco_tranche_1 = 0.0787
taux_agirc_arrco_tranche_2 = 0.2159
part_salariale_agirc_arrco = 0.4
part_patronale_agirc_arrco = 1 - part_salariale_agirc_arrco

def calcul_tranches_agirc_arrco(assiette):
    return calcul_tranches_vieillesse(assiette)

def calcul_cotis_agirc_arrco(assiette):
    A, B = calcul_tranches_agirc_arrco(assiette)
    return A  * part_salariale_agirc_arrco * taux_agirc_arrco_tranche_1, \
           A  * part_patronale_agirc_arrco * taux_agirc_arrco_tranche_1, \
           B  * part_salariale_agirc_arrco * taux_agirc_arrco_tranche_2, \
           B  * part_patronale_agirc_arrco * taux_agirc_arrco_tranche_2

# calcul allocations familiales
taux_allocations_familiales_patronal        = .0525
taux_allocations_familiales_patronal_reduit = taux_allocations_familiales_patronal - 0.018

def calcul_cotis_allocations_familiales(assiette, employeur_beneficie_taux_reduit):
    if employeur_beneficie_taux_reduit and (assiette < 2.5 * smic_mensuel_brut):
        return True, taux_allocations_familiales_patronal_reduit * assiette
    else:
        return False, taux_allocations_familiales_patronal * assiette

# calcul FNAL
seuil_nb_salaries_fnal = 50
def calcul_cotis_fnal(assiette, nb_salaries):
    if nb_salaries < seuil_nb_salaries_fnal:
        return 0.001 * min(assiette, plafond_securite_sociale)
    return 0.005 * assiette

# calcul CNSA (solidarité autonomie)
taux_cnsa_patronal = 0.003

# Assiettes

class Assiettes:
    def __init__(self):
        self.securite_sociale = 0.0
        self.csg              = 0.0
        self.tout             = 0.0
        
    def cotisation_traitement_brut(self, montant):
        self.securite_sociale += montant
        self.csg              += montant
        self.tout             += montant
        
        
    def cotisation_indemnites(self, montant, mode):
        if mode != MODE_PUBLIC:
            self.securite_sociale += montant
        self.csg              += montant
        self.tout             += montant
        
    def cotisation_psc(self, montant):
        self.csg  += montant
        self.tout += montant
        
    def cotisation_prime(self, montant, mode):
        if mode != MODE_PUBLIC:
            self.securite_sociale += montant
        self.csg              += montant
        self.tout             += montant
        
    def cotisation_transfert_primes_points(self, montant):
        self.csg -= montant

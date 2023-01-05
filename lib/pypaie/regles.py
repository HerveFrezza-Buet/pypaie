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

# Rapartition par tranches en tenant compte des heures sup.
def tranches_avec_hs(assiette_non_hs, assiette_hs, seuil_tranche):
    tranche_1 = min(assiette_non_hs, seuil_tranche)
    tranche_2 = 0 # comme ça ça fait vraiment 0, pas de soucis d'arrondis.
    if assiette_non_hs > seuil_tranche:
        tranche_2 = assiette_non_hs - tranche_1

    if tranche_2 > 0:
        tranche_1_hs = 0
        tranche_2_hs = assiette_hs
    else:
        a = assiette_non_hs + assiette_hs
        tranche_1_hs = min(a, seuil_tranche)
        tranche_2_hs = 0
        if a > seuil_tranche:
            tranche_2_hs = a - tranche_1
        tranche_1_hs -= assiette_non_hs
    return tranche_1, tranche_2, tranche_1_hs, tranche_2_hs
        
    

# calcul CSG-CRDS
taux_csg_abattement      = 0.9825
taux_csg_imp_salarial    = 0.024
taux_csg_nonimp_salarial = 0.068
taux_csg_total_salarial  = taux_csg_imp_salarial + taux_csg_nonimp_salarial
taux_crds_salarial       = 0.005

def calcul_assiette_csg_crds(assiette, assiette_hs):
    tranche_1, tranche_2, tranche_1_hs, tranche_2_hs = tranches_avec_hs(assiette, assiette_hs, 4*plafond_securite_sociale)
    base = tranche_1 * taux_csg_abattement + tranche_2
    base_hs = tranche_1_hs * taux_csg_abattement + tranche_2_hs
    return base, base_hs


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

def calcul_tranches_vieillesse(assiette, assiette_hs):
    seuil_max = 8*plafond_securite_sociale
    if assiette > seuil_max:
        t1, t2, t1hs, t2hs = tranches_avec_hs(seuil_max, 0, plafond_securite_sociale)
    elif assiette + assiette_hs > seuil_max:
        t1, t2, t1hs, t2hs = tranches_avec_hs(assiette, seuil_max - assiette, plafond_securite_sociale)
    else:
        t1, t2, t1hs, t2hs = tranches_avec_hs(assiette, assiette_hs, plafond_securite_sociale)
    return t1, t2, t1hs, t2hs

def calcul_cotis_vieillesse(assiette, assiette_hs):
    A, B, Ahs, Bhs = calcul_tranches_vieillesse(assiette, assiette_hs)
    AB   = A + B
    ABhs = Ahs + Bhs
    return A    * taux_vieillesse_salarial_plafonnee,  \
           Ahs  * taux_vieillesse_salarial_plafonnee,  \
           A    * taux_vieillesse_patronal_plafonnee,  \
           Ahs  * taux_vieillesse_patronal_plafonnee,  \
           AB   * taux_vieillesse_salarial_deplafonnee,\
           ABhs * taux_vieillesse_salarial_deplafonnee,\
           AB   * taux_vieillesse_patronal_deplafonnee,\
           ABhs * taux_vieillesse_patronal_deplafonnee

# calcul retraite pubplique complementaire IRCANTEC

taux_ircantec_salarial_tranche_a = 0.028
taux_ircantec_patronal_tranche_a = 0.042

taux_ircantec_salarial_tranche_b = 0.0695
taux_ircantec_patronal_tranche_b = 0.1255

def calcul_tranches_ircantec(assiette, assiette_hs):
    return calcul_tranches_vieillesse(assiette, assiette_hs)

def calcul_cotis_ircantec(assiette, assiette_hs):
    A, B, Ahs, Bhs = calcul_tranches_ircantec(assiette, assiette_hs)
    return A   * taux_ircantec_salarial_tranche_a, \
           Ahs * taux_ircantec_salarial_tranche_a, \
           A   * taux_ircantec_patronal_tranche_a, \
           Ahs * taux_ircantec_patronal_tranche_a, \
           B   * taux_ircantec_salarial_tranche_b, \
           Bhs * taux_ircantec_salarial_tranche_b, \
           B   * taux_ircantec_patronal_tranche_b, \
           Bhs * taux_ircantec_patronal_tranche_b 

# calcul retraite privée complementaire AGIRC-ARRCO

taux_agirc_arrco_tranche_1 = 0.0787
taux_agirc_arrco_tranche_2 = 0.2159
part_salariale_agirc_arrco = 0.4
part_patronale_agirc_arrco = 1 - part_salariale_agirc_arrco

def calcul_tranches_agirc_arrco(assiette, assiette_hs):
    return calcul_tranches_vieillesse(assiette, assiette_hs)

def calcul_cotis_agirc_arrco(assiette, assiette_hs):
    A, B, Ahs, Bhs = calcul_tranches_agirc_arrco(assiette, assiette_hs)
    return A   * part_salariale_agirc_arrco * taux_agirc_arrco_tranche_1, \
           Ahs * part_salariale_agirc_arrco * taux_agirc_arrco_tranche_1, \
           A   * part_patronale_agirc_arrco * taux_agirc_arrco_tranche_1, \
           Ahs * part_patronale_agirc_arrco * taux_agirc_arrco_tranche_1, \
           B   * part_salariale_agirc_arrco * taux_agirc_arrco_tranche_2, \
           Bhs * part_salariale_agirc_arrco * taux_agirc_arrco_tranche_2, \
           B   * part_patronale_agirc_arrco * taux_agirc_arrco_tranche_2, \
           Bhs * part_patronale_agirc_arrco * taux_agirc_arrco_tranche_2

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

# Calcul contribution ATI
taux_ati_patronal = 0.0032

# calcul retraite publique CNRACL
taux_cnracl_salarial = 0.111
taux_cnracl_patronal = 0.3065

# calcul retraite publique pension civile (PC)
taux_pc_salarial = 0.111
taux_pc_patronal = 0.7428

# calcul retraite complémentaire RAFP
taux_rafp_seuil = .2
taux_rafp_salarial = .05
taux_rafp_patronal = .05

# Assiettes

class Assiettes:
    def __init__(self):
        self.securite_sociale    = 0.0 
        self.securite_sociale_hs = 0.0
        self.csg                 = 0.0 
        self.csg_hs              = 0.0 
        self.ircantec            = 0.0
        self.ircantec_hs         = 0.0
        self._rafp               = 0.0
        self.tout                = 0.0

    def __str__(self):
        return f'[secu={self.securite_sociale}, secu_hs={self.securite_sociale_hs}, csg={self.csg}, csg_hs={self.csg_hs}, ircantec={self.ircantec}, ircantec_hs={self.ircantec_hs}, rafp={self.rafp}]={self.tout}'

    @property
    def rafp(self):
        return min(self._rafp, taux_rafp_seuil * self.securite_sociale)
        
    def cotisation_heures_sup_brut(self, montant):
        self.securite_sociale_hs += montant
        self.ircantec_hs         += montant
        self.csg_hs              += montant
        self.tout                += montant
        
    def cotisation_traitement_brut(self, montant):
        self.securite_sociale += montant
        self.ircantec         += montant
        self.csg              += montant
        self.tout             += montant

    def cotisation_remboursement_transport(self, montant):
        self.tout             += montant

    
    def cotisation_familial(self, montant, mode):
        if mode != MODE_PUBLIC:
            self.securite_sociale += montant
        else:
            self._rafp += montant
        self.csg              += montant
        self.tout             += montant
        
    def cotisation_indemnites(self, montant, mode):
        self.cotisation_familial(montant, mode)
        self.ircantec         += montant
        
    def cotisation_psc(self, montant):
        self.csg  += montant
        self.tout += montant
        
    def cotisation_prime(self, montant, mode):
        if mode != MODE_PUBLIC:
            self.securite_sociale += montant
        else:
            self._rafp += montant
        self.ircantec         += montant
        self.csg              += montant
        self.tout             += montant
        
    def cotisation_transfert_primes_points(self, montant):
        self.csg   -= montant
        self._rafp -= montant

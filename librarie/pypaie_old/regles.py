
CATEGORIE_REVENU_TRAITEMENT_BRUT =   1
CATEGORIE_REVENU_PRIME           =   2
CATEGORIE_REVENU_TRANSPORT       =   4
CATEGORIE_REVENU_PSC             =   8
CATEGORIE_REVENU_AUTRE           =  16
CATEGORIE_REVENU_LIBRE           =  32 # 2 x le dernier de la liste

ASSIETTE_COTISATIONS_PUBLIC = CATEGORIE_REVENU_TRAITEMENT_BRUT
ASSIETTE_COTISATIONS_PRIVE  = CATEGORIE_REVENU_TRAITEMENT_BRUT | CATEGORIE_REVENU_PRIME | CATEGORIE_REVENU_AUTRE
ASSIETTE_CSG_PUBLIC         = CATEGORIE_REVENU_TRAITEMENT_BRUT | CATEGORIE_REVENU_PRIME | CATEGORIE_REVENU_AUTRE | CATEGORIE_REVENU_PSC
ASSIETTE_CSG_PRIVE          = ASSIETTE_CSG_PUBLIC
ASSIETTE_TOUT               = CATEGORIE_REVENU_LIBRE - 1

class Assiette:
    def __init__(self):
        self.clear()

    def clear(self):
        self.traitement_brut = 0.0
        self.prime           = 0.0
        self.transport       = 0.0
        self.psc             = 0.0
        self.autre           = 0.0

    def declare(self, categorie, montant):
        if categorie == CATEGORIE_REVENU_TRAITEMENT_BRUT:
            self.traitement_brut += montant
        elif categorie == CATEGORIE_REVENU_PRIME:
            self.prime += montant
        elif categorie == CATEGORIE_REVENU_TRANSPORT:
            self.transport += montant
        elif categorie == CATEGORIE_REVENU_PSC:
            self.psc += montant
        elif categorie == CATEGORIE_REVENU_AUTRE:
            self.autre += montant
        else:
            raise ValueError(f'Assiette.declare({categorie}, {montant}) non géré.')

    def montant(self, assiette):
        res = 0.0
        if assiette & CATEGORIE_REVENU_TRAITEMENT_BRUT :
            res += self.traitement_brut
        if assiette & CATEGORIE_REVENU_PRIME :
            res += self.prime      
        if assiette & CATEGORIE_REVENU_TRANSPORT :
            res += self.transport    
        if assiette & CATEGORIE_REVENU_PSC :
            res += self.psc          
        if assiette & CATEGORIE_REVENU_AUTRE :
            res += self.autre
        return res
        

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

# calcul retraite publique CRNACL
taux_crnacl_salarial = 0.111
taux_crnacl_patronal = 0.3065

# calcul retraite publique pension civile (PC)
taux_pc_salarial = 0.111
taux_pc_patronal = 0.7428

# calcul retraite complémentaire RAFP
taux_rafp_seuil = .2
taux_rafp_salarial = .05
taux_rafp_patronal = .05
def calcul_assiette_RAFP(traitement_brut, autres_revenus):
    return min(taux_rafp_seuil * traitement_brut, autres_revenus)
    

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

# calcul chomage
taux_chomage_patronal = 0.0405
taux_ags_patronal     = 0.0015
def calcul_assiette_chomage(brut_salarial):
    return min(brut_salarial, 4*plafond_securite_sociale)

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
taux_maladie_patronal_prive_reduit     = .07
taux_maladie_patronal_prive_majoration = .06
taux_maladie_patronal_public           = .097
taux_maladie_salarial_local            = .013
seuil_majoration_maladie               = 2.5 * smic_mensuel_brut

# calcul familial
taux_allocations_familiales_patronal        = .0525
taux_allocations_familiales_patronal_reduit = taux_allocations_familiales_patronal - 0.018
def allocs_fam_reduites(employeur_beneficie_taux_reduit, brut_salarial):
    return employeur_beneficie_taux_reduit and (brut_salarial < 2.5 * smic_mensuel_brut)


# calcul FNAL
seuil_nb_salaries_fnal = 50
def calcul_cotis_fnal(brut_salarial, nb_salaries):
    if nb_salaries < seuil_nb_salaries_fnal:
        return 0.001 * min(brut_salarial, plafond_securite_sociale)
    return 0.005 * brut_salarial

# calcul Solidarité autonomie
taux_cnsa_patronal = 0.003

# Calcul contribution ATI
taux_ati_patronal = 0.0032

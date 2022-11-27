
# Plafond mensuel de la Sécurité sociale (brut salarial)
plafond_securite_sociale = 3428

# La valeur en brut salarial du point d'incice.
valeur_point_indice = 4.85003

# Indemnite pour difficultés administratives
def indemnite_difficultes_administratives(indice):
    if indice <= 341:
        return 1.83
    if indice <= 770:
        return 2.28
    return 3.05

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

# Assiettes

class Assiettes:
    def __init__(self):
        self.securite_sociale = 0.0
        self.csg              = 0.0
        
    def cotisation_traitement_brut(self, montant, mode):
        self.securite_sociale += montant
        self.csg              += montant
        
    def cotisation_psc(self, montant, mode):
        pass
        
        

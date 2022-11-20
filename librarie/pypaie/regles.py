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
pss = 3428

# calcul retraite privé
def calcul_tranches_cotisation_vieillesse(brut_salarial):
    tranche_1 = min(brut_salarial, pps)
    tranche_2 = min(max(0, brut_salarial - tranche1), 7*pps)
    tranche_3 = brut_salarial - tranche1 - tranche2
    return tranche_1, tranche_2, tranche_3


    
    

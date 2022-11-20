import pypaie as pp

mon_indice = 1059

# je crée un bulletin de paie
bulletin_paie = pp.bulletin.Bulletin()
print(bulletin_paie)

# J'y ajoute les revenus.
bulletin_paie += pp.revenus.traitement_brut(indice=mon_indice)
bulletin_paie += pp.revenus.indemnite_de_residence(51.36) 
bulletin_paie += pp.revenus.indemnite_pour_difficultes_administratives(mon_indice)
bulletin_paie += pp.revenus.indemnite_hausse_CSG(1.94)
bulletin_paie += pp.revenus.remboursement_psc()

# Je mentionne les cotisations.

print(bulletin_paie.bruts_salariaux)
print(bulletin_paie.brut_salarial)
                      

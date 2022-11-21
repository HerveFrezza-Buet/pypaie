import pypaie as pp

mon_indice = 1059

# je crée un bulletin de paie
bulletin_paie = pp.bulletin.Bulletin()

# J'y ajoute les revenus.
bulletin_paie += pp.revenus.traitement_brut(indice=mon_indice)
bulletin_paie += pp.revenus.indemnite_de_residence(51.36) 
bulletin_paie += pp.revenus.indemnite_pour_difficultes_administratives(mon_indice)
bulletin_paie += pp.revenus.indemnite_hausse_CSG(1.94)
bulletin_paie += pp.revenus.remboursement_psc()

# Je mentionne les cotisations.
bulletin_paie -= pp.cotisations.VIEILLESSE_PRIVE
# bulletin_paie -= pp.cotisations.AGIRC_ARRCO_PRIVE
bulletin_paie -= pp.cotisations.IRCANTEC

# Je montre le résultat
filename = 'contractuel_CS.xlsx'
bulletin_paie.to_excel(filename)
print(f'fichier "{filename}" généré.')

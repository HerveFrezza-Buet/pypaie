import pypaie as pp

mon_indice = 1059

# je crée un bulletin de paie
bulletin_paie = pp.bulletin.Bulletin(allocation_maladie_taux_reduit = False,
                                     taux_accidents_travail = 1.07,
                                     taux_versement_mobilite = 2.00)

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
bulletin_paie -= pp.cotisations.CHOMAGE
bulletin_paie -= pp.cotisations.MALADIE_REGIME_LOCAL
bulletin_paie -= pp.cotisations.ALLOCATIONS_FAMILIALES
bulletin_paie -= pp.cotisations.ACCIDENTS_TRAVAIL
bulletin_paie -= pp.cotisations.FNAL
bulletin_paie -= pp.cotisations.CNSA
bulletin_paie -= pp.cotisations.CSG_CRDS
bulletin_paie -= pp.cotisations.MOBILITE

# Je montre le résultat
filename = 'contractuel_CS.xlsx'
bulletin_paie.to_excel(filename)
print(f'fichier "{filename}" généré.')

import pypaie as pp

indice = 1059

bulletin_paie  = pp.bulletin.Bulletin()
tb = pp.revenus.TraitementIndiciaireBrut(indice)
bulletin_paie += tb
bulletin_paie += pp.revenus.IndemniteResidence(1.00, tb)
bulletin_paie += pp.revenus.IndemniteDifficultesAdministratives(indice)
bulletin_paie += pp.revenus.IndemniteCompensationHausseCSG(1.94)
bulletin_paie += pp.revenus.RemboursementPSC()

bulletin_paie -= pp.cotisations.CSG_CRDS()
bulletin_paie -= pp.cotisations.Maladie(pp.regles.REGIME_LOCAL)
#bulletin_paie -= pp.cotisations.Chomage()
bulletin_paie -= pp.cotisations.Vieillesse()
bulletin_paie -= pp.cotisations.IRCANTEC()

bulletin_paie(pp.regles.MODE_PRIVE) # On fait les calculs

filename = 'EC-contractuel-CS.xlsx'
bulletin_paie.to_excel(filename)
print(f'fichier "{filename}" généré.')

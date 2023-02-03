import pypaie as pp

indice = 700

bulletin_paie  = pp.bulletin.Bulletin(title = 'Psychologue Education Nationale')
tb = pp.revenus.TraitementIndiciaireBrut(indice)
bulletin_paie += tb
bulletin_paie += pp.revenus.IndemniteResidence(1.00, tb)
bulletin_paie += pp.revenus.IndemniteDifficultesAdministratives(indice)
bulletin_paie += pp.revenus.IndemniteFonctions(170.35)
bulletin_paie += pp.revenus.IndemniteCompensationHausseCSG(25.13)
bulletin_paie += pp.revenus.RemboursementPSC()
bulletin_paie += pp.revenus.TransfertPrimesPoints(32.42)

bulletin_paie -= pp.cotisations.CSG_CRDS()
bulletin_paie -= pp.cotisations.Maladie()
bulletin_paie -= pp.cotisations.AllocationsFamiliales()
bulletin_paie -= pp.cotisations.FNAL()
bulletin_paie -= pp.cotisations.CNSA()
bulletin_paie -= pp.cotisations.ATI()
bulletin_paie -= pp.cotisations.CNRACL()
bulletin_paie -= pp.cotisations.RAFP()


bulletin_paie(pp.regles.MODE_PUBLIC) # On fait les calculs

filename = 'psy-fonctionnaire-EN.xlsx'
bulletin_paie.to_excel(filename)
print(f'fichier "{filename}" généré.')

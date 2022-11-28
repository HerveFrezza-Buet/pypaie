import pypaie as pp

indice = 361

bulletin_paie  = pp.bulletin.Bulletin()
tb = pp.revenus.TraitementIndiciaireBrut(indice)
bulletin_paie += tb
bulletin_paie += pp.revenus.IndemniteResidence(3.00, tb)
bulletin_paie += pp.revenus.RemboursementTransport(34.46)
bulletin_paie += pp.revenus.IndemniteFonctions(266.67)
bulletin_paie += pp.revenus.TransfertPrimesPoints(23.17)

bulletin_paie -= pp.cotisations.CSG_CRDS()
bulletin_paie -= pp.cotisations.Maladie()
bulletin_paie -= pp.cotisations.AllocationsFamiliales()
bulletin_paie -= pp.cotisations.FNAL()
bulletin_paie -= pp.cotisations.CNSA()
bulletin_paie -= pp.cotisations.ATI()
bulletin_paie -= pp.cotisations.PensionCivile()
bulletin_paie -= pp.cotisations.RAFP()


bulletin_paie(pp.regles.MODE_PUBLIC) # On fait les calculs

filename = 'irtf-AB-CS.xlsx'
bulletin_paie.to_excel(filename)
print(f'fichier "{filename}" généré.')

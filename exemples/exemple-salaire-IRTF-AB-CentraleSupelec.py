import pypaie as pp


bulletin_paie  = pp.bulletin.Bulletin(title = 'IRTF A/B CentraleSupélec')

cas = 2

if cas == 1:
    indice = 350
    tb = pp.revenus.TraitementIndiciaireBrut(indice)
    bulletin_paie += tb
    bulletin_paie += pp.revenus.IndemniteResidence(3.00, tb)
    bulletin_paie += pp.revenus.RemboursementTransport(34.46)
    bulletin_paie += pp.revenus.IndemniteFonctions(266.67)
    bulletin_paie += pp.revenus.TransfertPrimesPoints(23.17)

if cas == 2:
    indice = 700
    tb = pp.revenus.TraitementIndiciaireBrut(indice)
    bulletin_paie += tb
    bulletin_paie += pp.revenus.IndemniteResidence(3.00, tb)
    bulletin_paie += pp.revenus.SupplementFamilial(2.29)
    bulletin_paie += pp.revenus.IndemniteFonctions(419.17)
    bulletin_paie += pp.revenus.IndemniteCompensationHausseCSG(34.32)
    bulletin_paie += pp.revenus.RemboursementPSC()
    bulletin_paie += pp.revenus.TransfertPrimesPoints(32.42)
    
    bulletin_paie -= pp.cotisations.Prefon(38.00)

    

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

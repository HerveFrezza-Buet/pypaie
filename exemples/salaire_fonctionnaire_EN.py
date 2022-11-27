import pypaie as pp

mon_indice = 715

# je crée un bulletin de paie
bulletin_paie = pp.bulletin.Bulletin(fonctionnaire=True)

# J'y ajoute les revenus.
bulletin_paie += pp.revenus.traitement_brut(indice=mon_indice)
bulletin_paie += pp.revenus.indemnite_de_residence() 
bulletin_paie += pp.revenus.indemnite_pour_difficultes_administratives(mon_indice)
bulletin_paie += pp.revenus.prime(170.35, 'indemnité de fonction')
bulletin_paie += pp.revenus.indemnite_hausse_CSG(25.13)
bulletin_paie += pp.revenus.remboursement_psc()

# Je mentionne les cotisations.
bulletin_paie -= pp.cotisations.CSG_CRDS
bulletin_paie -= pp.cotisations.CRNACL
bulletin_paie -= pp.cotisations.RAFP
bulletin_paie -= pp.cotisations.MALADIE_REGIME_GENERAL
bulletin_paie -= pp.cotisations.ALLOCATIONS_FAMILIALES
bulletin_paie -= pp.cotisations.FNAL
bulletin_paie -= pp.cotisations.CNSA
bulletin_paie.transfert_primes_points = 32.42
bulletin_paie -= pp.cotisations.TRANSFERT_PRIMES_POINTS
bulletin_paie -= pp.cotisations.ATI

# Je montre le résultat
filename = 'fonctionnaire_EN.xlsx'
bulletin_paie.to_excel(filename)
print(f'fichier "{filename}" généré.')

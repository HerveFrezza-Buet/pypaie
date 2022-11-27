import pypaie as pp

mon_indice = 361

bulletin_paie = pp.bulletin.Bulletin(fonctionnaire=True,
                                     taux_versement_mobilite = 2.00,
                                     taux_indemnite_residence = 3.00)

bulletin_paie += pp.revenus.traitement_brut(indice=mon_indice)
bulletin_paie += pp.revenus.indemnite_de_residence() 
bulletin_paie += pp.revenus.remboursement_transport(34.46) 
bulletin_paie += pp.revenus.prime(266.67, 'I.F.S.E.')

bulletin_paie -= pp.cotisations.CSG_CRDS
bulletin_paie -= pp.cotisations.PC
bulletin_paie -= pp.cotisations.RAFP
bulletin_paie -= pp.cotisations.MALADIE_REGIME_GENERAL
bulletin_paie -= pp.cotisations.ALLOCATIONS_FAMILIALES
bulletin_paie -= pp.cotisations.FNAL
bulletin_paie -= pp.cotisations.ATI
bulletin_paie -= pp.cotisations.MOBILITE
bulletin_paie.transfert_primes_points = 23.17
bulletin_paie -= pp.cotisations.TRANSFERT_PRIMES_POINTS

filename = 'fonctionnaire_IRFT_B.xlsx'
bulletin_paie.to_excel(filename)
print(f'fichier "{filename}" généré.')

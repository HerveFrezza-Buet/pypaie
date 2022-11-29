# Ce script python documente tout les éléments que pypaie sait ajouter
# à une fiche de paie.

import pypaie as pp

bulletin_paie = pp.bulletin.Bulletin()

###########
#         #
# Revenus #
#         #
###########

bulletin_paie += pp.revenus.TraitementBrut(1000)                    # Traitement brut de 1000 euros.
bulletin_paie += pp.revenus.TraitementIndiciaireBrut(500)           # Traitement brut d'indice 500.     
bulletin_paie += pp.revenus.PrimePublic(200)                        # Prime d'un fonctionnaire de 200 euros.
bulletin_paie += pp.revenus.PrimePrive(200)                         # Prime d'un contractuel / salarié du privé de 200 euros.
bulletin_paie += pp.revenus.TransfertPrimesPoints(200)              # Transfert primes/points (fonctionnaires) de 200 euros.
bulletin_paie += pp.revenus.IndemniteResidence(20)                  # Indemnité de résidence de 20 euros.
bulletin_paie += pp.revenus.SupplementFamilial(20)                  # Supplément familial de traitement de 20 euros.               
bulletin_paie += pp.revenus.IndemniteDifficultesAdministratives(10) # Indemnités diff. admin de 10 euros.
bulletin_paie += pp.revenus.IndemniteCompensationHausseCSG(10)      # Indemnités compensatrices CSG de 10 euros.
bulletin_paie += pp.revenus.RemboursementPSC()                      # Remboursement forfaitaire PSC.
bulletin_paie += pp.revenus.RemboursementTransport(100)             # Remboursement transport domicile-travail de 100 euros.





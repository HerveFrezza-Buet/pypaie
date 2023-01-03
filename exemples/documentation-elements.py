# Ce script python documente tout les éléments que pypaie sait ajouter
# à une fiche de paie.

import pypaie as pp

bulletin_paie = pp.bulletin.Bulletin()

tb = pp.revenus.TraitementBrut(1000)

###########
#         #
# Revenus #
#         #
###########

bulletin_paie += pp.revenus.TraitementBrut(1000)                    # Traitement brut de 1000 euros.
bulletin_paie += pp.revenus.TraitementIndiciaireBrut(500)           # Traitement brut d'indice 500.     
bulletin_paie += pp.revenus.HeuresSupBrut(500)                      # Heures sup 500 euros.     
bulletin_paie += pp.revenus.PrimePublic('nom', 200)                 # Prime d'un fonctionnaire de 200 euros.
bulletin_paie += pp.revenus.PrimePrive('nom', 200)                  # Prime d'un contractuel / salarié du privé de 200 euros.
bulletin_paie += pp.revenus.IndemniteFonctions(200)                 # Prime d'un fonctionnaire de 200 euros.
bulletin_paie += pp.revenus.TransfertPrimesPoints(200)              # Transfert primes/points (fonctionnaires) de 200 euros.
bulletin_paie += pp.revenus.IndemniteResidence(2.0, tb)             # Indemnité de résidence de 2% du traitement tb.
bulletin_paie += pp.revenus.SupplementFamilial(20)                  # Supplément familial de traitement de 20 euros.               
bulletin_paie += pp.revenus.IndemniteDifficultesAdministratives(10) # Indemnités diff. admin de 10 euros.
bulletin_paie += pp.revenus.IndemniteCompensationHausseCSG(10)      # Indemnités compensatrices CSG de 10 euros.
bulletin_paie += pp.revenus.RemboursementPSC()                      # Remboursement forfaitaire PSC.
bulletin_paie += pp.revenus.RemboursementTransport(100)             # Remboursement transport domicile-travail de 100 euros.


###############
#             #
# Cotisations #
#             #
###############

bulletin_paie -= pp.cotisations.CSG_CRDS()
bulletin_paie -= pp.cotisations.Maladie()                                 # Cotisation maladie au régime général.
bulletin_paie -= pp.cotisations.Maladie(regime = pp.regles.REGIME_LOCAL)  # Cotisation maladie au régime Alsace-Moselle.
bulletin_paie -= pp.cotisations.Chomage()
bulletin_paie -= pp.cotisations.AllocationsFamiliales()                   # Cotisation alloc. fam., employeur à taux plein.
bulletin_paie -= pp.cotisations.AllocationsFamiliales(taux_reduit = True) # Cotisation alloc. fam., employeur à taux réduit.
bulletin_paie -= pp.cotisations.FNAL()                                    # Cotisation logement, entreprise au dessus du seuil.
bulletin_paie -= pp.cotisations.FNAL(100)                                 # Cotisation logement, entreprise de 100 salariés.
bulletin_paie -= pp.cotisations.AccidentsTravail(1.07)                    # Cotisation accident du travail, entreprise à 1.07%.
bulletin_paie -= pp.cotisations.Mobilite(1.0)                             # Cotisation mobilité, entreprise à 1%.
bulletin_paie -= pp.cotisations.CNSA()

# Retraites 
bulletin_paie -= pp.cotisations.Prefon(50)
bulletin_paie -= pp.cotisations.ATI()
bulletin_paie -= pp.cotisations.CNRACL()
bulletin_paie -= pp.cotisations.RAFP()
bulletin_paie -= pp.cotisations.PensionCivile()
bulletin_paie -= pp.cotisations.Vieillesse()
bulletin_paie -= pp.cotisations.IRCANTEC()
bulletin_paie -= pp.cotisations.AGIRC_ARRCO()


##############
#            #
# Autres cas #
#            #
##############

bulletin_paie != pp.evenements.RegularisationAccompte(500) # Regularisation d'un accompte de salaire sur la fiche de paie.

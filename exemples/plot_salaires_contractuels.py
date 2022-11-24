import sys
import numpy as np
import matplotlib.pyplot as plt
import pypaie as pp

if len(sys.argv) != 2:
    print(f'usage : {sys.argv[0]} <chomage|pas_chomage>')
    sys.exit(0)

bulletin_paie = pp.bulletin.Bulletin(employeur_beneficie_taux_reduit_alloc_familiales = False,
                                     taux_accidents_travail = 1.07,
                                     taux_versement_mobilite = 2.00,
                                     nb_salaries = 100)

indices = np.arange(200, 2000)
bruts = []
nets = []
for indice in indices:
    bulletin_paie.clear()
    bulletin_paie += pp.revenus.traitement_brut(indice=indice)
    bulletin_paie += pp.revenus.indemnite_de_residence() 
    bulletin_paie += pp.revenus.indemnite_pour_difficultes_administratives(indice)
    bulletin_paie += pp.revenus.indemnite_hausse_CSG(2.00)
    bulletin_paie += pp.revenus.remboursement_psc()
    bulletin_paie -= pp.cotisations.VIEILLESSE_PRIVE
    bulletin_paie -= pp.cotisations.IRCANTEC
    bulletin_paie -= pp.cotisations.MALADIE_REGIME_GENERAL
    bulletin_paie -= pp.cotisations.ALLOCATIONS_FAMILIALES
    bulletin_paie -= pp.cotisations.ACCIDENTS_TRAVAIL
    if sys.argv[1] == 'chomage':
        bulletin_paie -= pp.cotisations.CHOMAGE
    bulletin_paie -= pp.cotisations.FNAL
    bulletin_paie -= pp.cotisations.CNSA
    bulletin_paie -= pp.cotisations.CSG_CRDS
    bulletin_paie -= pp.cotisations.MOBILITE

    if indice == 800:
        filename = f'salaire_contractuel_{sys.argv[1]}.xlsx'
        bulletin_paie.to_excel(filename)
        print(f'fichier "{filename}" généré.')

    bruts.append(bulletin_paie.brut_patronal())
    nets.append(bulletin_paie.net_avant_impots())

bruts = np.array(bruts)
nets  = np.array(nets)

fig = plt.figure(figsize=(8,8))
gs  = fig.add_gridspec(2, 1,
                       wspace=0.2, hspace=0.2)



ax = fig.add_subplot(gs[0, 0])
ax.set_xlabel('indice')
ax.set_ylabel('salaire')
ax.plot(indices, bruts, label='salaire total')
ax.plot(indices, nets, label='salaire net')
ax.legend()

ax = fig.add_subplot(gs[1, 0])
ax.set_ylim(0, 1)
ax.set_xlabel('indice')
ax.set_ylabel('Pourcentage')
ax.plot(indices, np.ones_like(indices), label='salaire total')
ax.plot(indices, nets/bruts, label='salaire net')
ax.legend()

filename = f'net_et_brut_contractuel_{sys.argv[1]}.pdf'
plt.savefig(filename, bbox_inches = 'tight')
print(f'figure "{filename}" generated.')

        

    

        
        

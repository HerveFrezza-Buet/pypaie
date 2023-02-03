import pypaie as pp
import matplotlib.pyplot as plt

def revenus(bulletin_paie, indice):
    tb = pp.revenus.TraitementIndiciaireBrut(indice)
    bulletin_paie += tb
    bulletin_paie += pp.revenus.IndemniteResidence(1.00, tb)
    bulletin_paie += pp.revenus.IndemniteDifficultesAdministratives(indice)
    bulletin_paie += pp.revenus.IndemniteCompensationHausseCSG(1.94)
    bulletin_paie += pp.revenus.RemboursementPSC()
    
def cotisation_communes(bulletin_paie):
    bulletin_paie -= pp.cotisations.CSG_CRDS()
    bulletin_paie -= pp.cotisations.Maladie()
    bulletin_paie -= pp.cotisations.AllocationsFamiliales(taux_reduit = False)
    bulletin_paie -= pp.cotisations.FNAL(nb_salaries = 1000)
    bulletin_paie -= pp.cotisations.CNSA()
    
def cotisation_fonctionnaire(bulletin_paie):
    bulletin_paie -= pp.cotisations.ATI()
    bulletin_paie -= pp.cotisations.PensionCivile()
    bulletin_paie -= pp.cotisations.RAFP()
    
def cotisation_contractuel(bulletin_paie):
    bulletin_paie -= pp.cotisations.Vieillesse()
    bulletin_paie -= pp.cotisations.IRCANTEC()
    bulletin_paie -= pp.cotisations.AccidentsTravail(taux=1.07)
    bulletin_paie -= pp.cotisations.Mobilite(taux=2.00)

contractuel   = pp.bulletin.Bulletin(title = 'EC-contractuel-CS')
fonctionnaire = pp.bulletin.Bulletin(title = 'EC-fonctionnaire-CS')
bulletins     = [contractuel, fonctionnaire]

for b in bulletins:
    revenus(b, 1000)
    cotisation_communes(b)
cotisation_fonctionnaire(fonctionnaire)
cotisation_contractuel(contractuel)

contractuel(pp.regles.MODE_CONTRACTUEL)
fonctionnaire(pp.regles.MODE_PUBLIC)

bilans = [b.bilan for b in bulletins]

for b in bulletins:
    filename = f'{b.bilan.title}.xlsx'
    b.to_excel(filename)
    print(f'fichier "{filename}" généré.')


plt.figure(figsize=(10,10))
pp.bulletin.barplot(plt.gca(), bilans, 'Comparaison fonctionnaire/contractuel')
plt.savefig('comparaison.pdf', bbox_inches='tight')
print('fichier "comparaison.pdf" généré.')
    





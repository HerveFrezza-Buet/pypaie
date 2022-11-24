from . import revenus
from . import cotisations
from . import regles

import xlsxwriter

class Bulletin:
    def __init__(self,
                 fonctionnaire = True,
                 employeur_beneficie_taux_reduit_alloc_familiales = False,
                 taux_accidents_travail = 0.0,
                 taux_versement_mobilite = 0.0,
                 taux_indemnite_residence = 1.00,
                 nb_salaries = 100):
        self.clear()

        self.fonctionnaire = fonctionnaire
        self.allocations_familiales_taux_reduit = employeur_beneficie_taux_reduit_alloc_familiales
        self.taux_accidents_travail = taux_accidents_travail * .01
        self.nb_salaries = nb_salaries
        self.taux_mobilite = taux_versement_mobilite*.01
        self.taux_indemnite_residence = taux_indemnite_residence * .01

    def clear(self):
        self.assiette = regles.Assiette()
        self.revenus = []
        self.cotisations = []
        self.cotisations_salariales = 0.
        self.cotisations_patronales = 0.
        
    def brut_patronal(self):
        return self.assiette.montant(regles.ASSIETTE_TOUT) + self.cotisations_patronales

    def net_avant_impots(self):
        return self.assiette.montant(regles.ASSIETTE_TOUT) - self.cotisations_salariales
    
    def percoit(self, revenu):
        """
        Ajoute un revenu
        """

        # Pre-traitements:
        if revenu['libelle'] == revenus.TAG_INDEMNITE_RESIDENCE:
            if self.assiette.traitement_brut == 0:
                raise ValueError("Renseigner le traitement brut avant l'indemnité de résidence")
            revenu['montant'] = self.assiette.traitement_brut * self.taux_indemnite_residence
        
        self.revenus.append(revenu)
        self.assiette.declare(revenu['categorie'], revenu['montant'])

    def cotise(self, cotisation):
        if cotisation not in cotisations.cotisations:
            raise ValueError(f'Bulletin.cotise (-=) : type de cotisation -- {cotisation} -- non géré, devrait être dans {cotisations.cotisations}.')
        if cotisation == cotisations.CHOMAGE:
            cotis = cotisations.chomage(self.assiette.montant(regles.ASSIETTE_COTISATIONS_PRIVE))
        elif cotisation == cotisations.VIEILLESSE_PRIVE:
            cotis = cotisations.vieillesse_prive(self.assiette.montant(regles.ASSIETTE_COTISATIONS_PRIVE))
        elif cotisation == cotisations.CRNACL:
            cotis = cotisations.crnacl(self.assiette.montant(regles.ASSIETTE_COTISATIONS_PUBLIC))
        elif cotisation == cotisations.RAFP:
            traitement = self.assiette.traitement_brut
            cotis = cotisations.rafp(traitement, self.assiette.montant(regles.ASSIETTE_TOUT) - traitement)
        elif cotisation == cotisations.ATI:
            cotis = cotisations.ati(self.assiette.montant(regles.ASSIETTE_COTISATIONS_PUBLIC))
        elif cotisation == cotisations.TRANSFERT_PRIMES_POINTS:
            cotis = cotisations.transfert_primes_points(self.transfert_primes_points)
        elif cotisation == cotisations.AGIRC_ARRCO:
            cotis = cotisations.agirc_arrco(self.assiette.montant(regles.ASSIETTE_COTISATIONS_PRIVE))
        elif cotisation == cotisations.IRCANTEC:
            cotis = cotisations.ircantec(self.assiette.montant(regles.ASSIETTE_COTISATIONS_PRIVE))
        elif cotisation == cotisations.CSG_CRDS:
            if self.fonctionnaire:
                cotis = cotisations.csg_crds(self.assiette.montant(regles.ASSIETTE_CSG_PUBLIC))
            else:
                cotis = cotisations.csg_crds(self.assiette.montant(regles.ASSIETTE_CSG_PRIVE))
        elif cotisation == cotisations.MALADIE_REGIME_GENERAL:
            if self.fonctionnaire:
                cotis = cotisations.maladie_regime_general(self.assiette.montant(regles.ASSIETTE_COTISATIONS_PUBLIC), True)
            else:
                cotis = cotisations.maladie_regime_general(self.assiette.montant(regles.ASSIETTE_COTISATIONS_PRIVE), False)
        elif cotisation == cotisations.MALADIE_REGIME_LOCAL:
            cotis = cotisations.maladie_regime_local(self.assiette.montant(regles.ASSIETTE_COTISATIONS_PRIVE))
        elif cotisation == cotisations.ALLOCATIONS_FAMILIALES:
            if self.fonctionnaire:
                assiette = self.assiette.montant(regles.ASSIETTE_COTISATIONS_PUBLIC)
            else:
                assiette = self.assiette.montant(regles.ASSIETTE_COTISATIONS_PRIVE)
            cotis = cotisations.allocations_familiales(assiette, regles.allocs_fam_reduites(self.allocations_familiales_taux_reduit, assiette))
        elif cotisation == cotisations.ACCIDENTS_TRAVAIL:
            if self.fonctionnaire:
                cotis = cotisations.accidents_travail(self.assiette.montant(regles.ASSIETTE_COTISATIONS_PUBLIC), self.taux_accidents_travail)
            else:
                cotis = cotisations.accidents_travail(self.assiette.montant(regles.ASSIETTE_COTISATIONS_PRIVE), self.taux_accidents_travail)
        elif cotisation == cotisations.FNAL:
            if self.fonctionnaire:
                cotis = cotisations.fnal(self.assiette.montant(regles.ASSIETTE_COTISATIONS_PUBLIC), self.nb_salaries)
            else:
                cotis = cotisations.fnal(self.assiette.montant(regles.ASSIETTE_COTISATIONS_PRIVE), self.nb_salaries)
        elif cotisation == cotisations.CNSA:
            if self.fonctionnaire:
                cotis = cotisations.cnsa(self.assiette.montant(regles.ASSIETTE_COTISATIONS_PUBLIC))
            else:
                cotis = cotisations.cnsa(self.assiette.montant(regles.ASSIETTE_COTISATIONS_PRIVE))
        elif cotisation == cotisations.MOBILITE:
            if self.fonctionnaire:
                cotis = cotisations.mobilite(self.assiette.montant(regles.ASSIETTE_COTISATIONS_PUBLIC), self.taux_mobilite)
            else:
                cotis = cotisations.mobilite(self.assiette.montant(regles.ASSIETTE_COTISATIONS_PRIVE), self.taux_mobilite)
        else:
            raise ValueError(f'Bug : cotisation {cotisation} non traîtée.')
        
        for cot in cotis:
            self.cotisations_salariales += cot['salarial']
            self.cotisations_patronales += cot['patronal']
        self.cotisations += cotis
            

    def __iadd__(self, revenu):
        self.percoit(revenu)
        return self
    
    def __isub__(self, cotisation):
        self.cotise(cotisation)
        return self

    def to_excel(self, file_name):
        workbook = xlsxwriter.Workbook(file_name)
        title_fmt = workbook.add_format({'bg_color' : '#eeeeee', 'bold' : True, 'align' : 'center'})
        label_fmt = workbook.add_format({'align' : 'left'})
        euro_fmt  = workbook.add_format({'num_format' : '0.00', 'align' : 'right'})
        Label_fmt = workbook.add_format({'bold' : True, 'align' : 'left'})
        Euro_fmt  = workbook.add_format({'bold' : True, 'num_format' : '0.00', 'align' : 'right'})
        worksheet = workbook.add_worksheet('Fiche de paie')

        col_label = 1
        col_revenu = col_label+1
        col_cot_sal = col_revenu+1
        col_cot_pat = col_cot_sal+1

        # Header
        ligne = 1
        worksheet.write(ligne, col_revenu, 'Revenu', title_fmt)
        worksheet.write(ligne, col_cot_sal, 'Part salariale', title_fmt)
        worksheet.write(ligne, col_cot_pat, 'Part employeur', title_fmt)
        ligne += 1

        # Revenus
        for revenu in self.revenus:
            worksheet.write(ligne, col_label, revenu['libelle'], label_fmt)
            worksheet.write(ligne, col_revenu, revenu['montant'], euro_fmt)
            ligne += 1

        # Cotisations
        for cotisation in self.cotisations:
            worksheet.write(ligne, col_label, cotisation['libelle'], label_fmt)
            c = cotisation['salarial']
            if c > 0:
                worksheet.write(ligne, col_cot_sal, c, euro_fmt)
            c = cotisation['patronal']
            if c > 0:
                worksheet.write(ligne, col_cot_pat, c, euro_fmt)
            ligne += 1

        # Totaux
        worksheet.write(ligne, col_label, 'Total', Label_fmt)
        worksheet.write(ligne, col_revenu, self.brut_patronal(), Euro_fmt)
        worksheet.write(ligne, col_cot_sal, self.cotisations_salariales, Euro_fmt)
        worksheet.write(ligne, col_cot_pat, self.cotisations_patronales, Euro_fmt)
        ligne += 2
        worksheet.write(ligne, col_label, 'Net avant impôts', Label_fmt)
        worksheet.write(ligne, col_revenu, self.net_avant_impots(), Euro_fmt)

        
        
            
        
        workbook.close()
        
        



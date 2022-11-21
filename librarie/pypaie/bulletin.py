from . import revenus
from . import cotisations

import xlsxwriter

class Bulletin:
    def __init__(self):
        self.revenus = []
        self.brut_salarial = 0.
        self.autres_revenus = 0.

        self.cotisations = []
        self.cotisations_salariales = 0.
        self.cotisations_patronales = 0.


    def brut_patronal(self):
        return self.brut_salarial + self.autres_revenus + self.cotisations_patronales

    def net_avant_impots(self):
        return self.brut_salarial + self.autres_revenus - self.cotisations_salariales
    
    def percoit(self, revenu):
        """
        Ajoute un revenu
        """
        if revenu['type'] == revenus.TYPE_BRUT_SALARIAL:
            self.revenus.append(revenu)
            self.brut_salarial += revenu['montant']
            return
        
        if revenu['type'] == revenus.TYPE_INDEMNITE:
            self.revenus.append(revenu)
            self.autres_revenus += revenu['montant']
            return
        
        raise ValueError(f'Bulletin.percoit (+=) : type de revenu -- {revenu["type"]} -- non géré.')

    def cotise(self, cotisation):
        if cotisation not in cotisations.cotisations:
            raise ValueError(f'Bulletin.cotise (-=) : type de cotisation -- {cotisation} -- non géré, devrait être dans {cotisations.cotisations}.')
        if cotisation == cotisations.VIEILLESSE_PRIVE:
            cotis = cotisations.vieillesse_prive(self.brut_salarial)
        elif cotisation == cotisations.AGIRC_ARRCO:
            cotis = cotisations.agirc_arrco(self.brut_salarial)
        elif cotisation == cotisations.IRCANTEC:
            cotis = cotisations.ircantec(self.brut_salarial)
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
        
        



from . import regles
from . import revenus
from . import ligne

import xlsxwriter

revenus_geres = [revenus.TraitementBrut,
                 revenus.IndemniteResidence,
                 revenus.IndemniteDifficultesAdministratives,
                 revenus.IndemniteCompensationHausseCSG,
                 revenus.RemboursementPSC]

class Bulletin:
    def __init__(self):
        self.clear()

    def _verifie_revenu(self, revenu):
        for class_revenu in revenus_geres:
            if isinstance(revenu, class_revenu):
                return True
        raise ValueError(f'Bug : Bulletin : Revenu "{revenu.label}" non géré.')

    def clear(self):
        self.revenus     = []
        self.cotisations = []
        self.assiettes   = regles.Assiettes()

    def __call__(self, mode):
        self.assiettes = regles.Assiettes()
        for r in self.revenus:
            r.cotise(self.assiettes, mode)
        for c in self.cotisations:
            c.cotise(self.assiettes, mode)
        
        
    def __iadd__(self, revenu):
        self._verifie_revenu(revenu)
        self.revenus.append(revenu)
        return self

    def to_excel(self, file_name):
        workbook  = xlsxwriter.Workbook(file_name)
        title_fmt = workbook.add_format({'bg_color' : '#eeeeee', 'bold' : True, 'align' : 'center'})
        label_fmt = workbook.add_format({'align' : 'left'})
        euro_fmt  = workbook.add_format({'num_format' : '0.00', 'align' : 'right'})
        Label_fmt = workbook.add_format({'bold' : True, 'align' : 'left'})
        Euro_fmt  = workbook.add_format({'bold' : True, 'num_format' : '0.00', 'align' : 'right'})
        worksheet = workbook.add_worksheet('Fiche de paie')

        col_label   = 1
        col_revenu  = col_label+1
        col_cot_sal = col_revenu+1
        col_cot_pat = col_cot_sal+1

        # Header
        l = 1
        worksheet.write(l, col_revenu, 'Revenu', title_fmt)
        worksheet.write(l, col_cot_sal, 'Part salariale', title_fmt)
        worksheet.write(l, col_cot_pat, 'Part employeur', title_fmt)
        l += 1

        content  = []
        for elem in self.revenus:
            content += elem.lignes()
        for elem in self.cotisations:
            content += elem.lignes()

        for ll, elem in enumerate(content):
            if 'label' in elem:
                worksheet.write(ll + l, col_label, elem['label'], label_fmt)
            if 'brut' in elem:
                worksheet.write(ll + l, col_revenu, elem['brut'], euro_fmt)
            if 'salarial' in elem:
                worksheet.write(ll + l, col_cot_sal, elem['salarial'], euro_fmt)
            if 'employeur' in elem:
                worksheet.write(ll + l, col_cot_pat, elem['employeur'], euro_fmt)
                

        
        workbook.close()

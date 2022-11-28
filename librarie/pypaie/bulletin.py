from . import regles
from . import revenus
from . import cotisations
from . import ligne

import xlsxwriter

revenus_geres = [revenus.TraitementBrut,
                 revenus.IndemniteResidence,
                 revenus.IndemniteDifficultesAdministratives,
                 revenus.IndemniteCompensationHausseCSG,
                 revenus.RemboursementPSC,
                 revenus.PrimePublic,
                 revenus.TransfertPrimesPoints]

cotisations_gerees = [cotisations.CSG_CRDS,
                      cotisations.Maladie,
                      cotisations.AllocationsFamiliales,
                      cotisations.FNAL,
                      cotisations.AccidentsTravail,
                      cotisations.Mobilite,
                      cotisations.CNSA,
                      cotisations.Chomage,
                      cotisations.Vieillesse,
                      cotisations.AGIRC_ARRCO,
                      cotisations.IRCANTEC,
                      cotisations.ATI,
                      cotisations.RAFP,
                      cotisations.CNRACL,
                      cotisations.PensionCivile]

class Bulletin:
    def __init__(self):
        self.clear()

    def _verifie_revenu(self, revenu):
        for class_revenu in revenus_geres:
            if isinstance(revenu, class_revenu):
                return True
        raise ValueError(f'Bug : Bulletin : Revenu "{revenu.label}" non géré.')

    def _verifie_cotisation(self, cotisation):
        for class_cotisation in cotisations_gerees:
            if isinstance(cotisation, class_cotisation):
                return True
        raise ValueError(f'Bug : Bulletin : Cotisation "{cotisation.label}" non gérée.')

    def clear(self):
        self.revenus     = []
        self.cotisations = []
        self.assiettes   = regles.Assiettes()

    def __call__(self, mode):
        self.assiettes = regles.Assiettes()
        self.total_revenu    = 0.0
        self.total_salarial  = 0.0
        self.total_employeur = 0.0
        for elem in self.revenus + self.cotisations:
            elem.cotise(self.assiettes, mode)
            c = elem._brut()
            if c is not None:
                self.total_revenu    += c
            c = elem._cotisation_salariale()
            if c is not None:
                self.total_salarial  += c
            c = elem._cotisation_employeur()
            if c is not None:
                self.total_employeur += c
        
        
    def __iadd__(self, revenu):
        self._verifie_revenu(revenu)
        self.revenus.append(revenu)
        return self
    
    def __isub__(self, cotisation):
        self._verifie_cotisation(cotisation)
        self.cotisations.append(cotisation)
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
                
        l += ll + 2
        worksheet.write(l, col_label,   'Total',                                  Label_fmt)
        worksheet.write(l, col_revenu,  self.total_revenu + self.total_employeur, Euro_fmt)
        worksheet.write(l, col_cot_sal, self.total_salarial,                      Euro_fmt)
        worksheet.write(l, col_cot_pat, self.total_employeur,                     Euro_fmt)
        l += 1
        worksheet.write(l, col_label,   'Net',                                    Label_fmt)
        worksheet.write(l, col_revenu,  self.total_revenu - self.total_salarial,  Euro_fmt)
        
                

        
        workbook.close()

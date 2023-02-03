from . import regles
from . import revenus
from . import cotisations
from . import evenements
from . import ligne

import xlsxwriter

revenus_geres = [revenus.TraitementBrut,
                 revenus.HeuresSupBrut,
                 revenus.IndemniteResidence,
                 revenus.SupplementFamilial,
                 revenus.IndemniteDifficultesAdministratives,
                 revenus.IndemniteCompensationHausseCSG,
                 revenus.RemboursementPSC,
                 revenus.RemboursementTransport,
                 revenus.PrimePublic,
                 revenus.PrimePrive,
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
                      cotisations.PensionCivile,
                      cotisations.Prefon]

evenements_geres = [evenements.RegularisationAccompte]


class Bilan:
    def __init__(self, title):
        self.clear()
        self.title = title

    def clear(self):
        self.brut = 0.0
        self.salarial = 0.0
        self.employeur = 0.0
        self.retraite = 0.0
        self.chomage = 0.0
        self.maladie = 0.0
        self.divers = 0.0

    def salaire(self):
        return self.employeur + self.brut

    def net(self):
        return self.brut - self.salarial

    def __iadd__(self, elem):
        c = elem._brut()
        if c is not None:
            self.brut += c
        c = elem._cotisation_salariale()
        if c is not None:
            self.salarial  += c
        c = elem._cotisation_employeur()
        if c is not None:
            self.employeur += c
        return self
    
class Bulletin:
    def __init__(self, title = None):
        self.bilan = Bilan(title)
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

    def _verifie_evenement(self, evenement):
        for class_evenement in evenements_geres:
            if isinstance(evenement, class_evenement):
                return True
        raise ValueError(f'Bug : Bulletin : Evenement "{evenement.label}" non gérée.')

    def clear(self):
        self.elements = []
        self.bilan.clear()

    def __call__(self, mode):
        self.assiettes = regles.Assiettes()
        
        for elem in self.elements:
            elem.cotise(self.assiettes, mode)
            self.bilan += elem
        self._calcule_reduction_heures_sup()

    def _calcule_reduction_heures_sup(self):
        cotisation_salariale_hs = 0
        for elem in self.elements:
            if isinstance(elem, cotisations.ExonerableHeureSup):
                cotisation_salariale_hs += elem._cotisation_salariale_via_heures_sup()
        print('TO DO : réduction heures sup : gérer les seuils ici !!!')
        cot = cotisations.ReductionHeureSup(cotisation_salariale_hs)
        self.elements.append(cot)
        self.bilan += cot
        
    def __iadd__(self, revenu):
        self._verifie_revenu(revenu)
        self.elements.append(revenu)
        return self
    
    def __isub__(self, cotisation):
        self._verifie_cotisation(cotisation)
        self.elements.append(cotisation)
        return self
    
    def __ne__(self, evenement):
        self._verifie_evenement(evenement)
        self.elements.append(evenement)

    def to_excel(self, file_name):
        workbook  = xlsxwriter.Workbook(file_name)
        Title_fmt = workbook.add_format({'bg_color' : '#555555', 'color' : '#ffffff', 'bold' : True, 'align' : 'center'})
        title_fmt = workbook.add_format({'bg_color' : '#eeeeee', 'bold' : True, 'align' : 'center'})
        label_fmt = workbook.add_format({'align' : 'left'})
        euro_fmt  = workbook.add_format({'num_format' : '0.00', 'align' : 'right'})
        Label_fmt = workbook.add_format({'bold' : True, 'align' : 'left'})
        Euro_fmt  = workbook.add_format({'bold' : True, 'num_format' : '0.00', 'align' : 'right'})
        worksheet = workbook.add_worksheet('Fiche de paie')

        col_label   = 0
        col_revenu  = col_label+1
        col_cot_sal = col_revenu+1
        col_cot_pat = col_cot_sal+1

        # Header
        l = 0
        if self.bilan.title != None:
            worksheet.merge_range(l, col_label, l, col_cot_pat, self.bilan.title, Title_fmt)
            l += 1
        worksheet.write(l, col_revenu, 'Revenu', title_fmt)
        worksheet.write(l, col_cot_sal, 'Part salariale', title_fmt)
        worksheet.write(l, col_cot_pat, 'Part employeur', title_fmt)
        l += 1

        content  = []
        for elem in self.elements:
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
        worksheet.write(l, col_revenu,  self.bilan.salaire(),                     Euro_fmt)
        worksheet.write(l, col_cot_sal, self.bilan.salarial,                      Euro_fmt)
        worksheet.write(l, col_cot_pat, self.bilan.employeur,                     Euro_fmt)
        l += 1
        worksheet.write(l, col_label,   'Net',                                    Label_fmt)
        worksheet.write(l, col_revenu,  self.bilan.net(),  Euro_fmt)
        
                

        
        workbook.close()

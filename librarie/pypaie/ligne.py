import xlsxwriter

class Ligne:
    def __init__(self, label):
        self.label = label

    def _brut(self):
        """
        Renvoie le contenu de la colonne "à payer". None si inapproprié.
        """
        return None

    def _cotisation_salariale(self):
        """
        Renvoie le contenu de la colonne "à déduire". None si inapproprié.
        """
        return None

    def _cotisation_employeur(self):
        """
        Renvoie le contenu de la colonne "pour information". None si inapproprié.
        """
        return None

    def montants(self):
        return self._brut(), self._cotisation_salariale(), self._cotisation_employeur()

    def to_excel(self, worksheet, l,
                 label_fmt, euro_fmt
                 col_revenu, col_cot_sal, col_cot_pat):
        
        worksheet.write(l, col_label, self.label, label_fmt)
        b, s, p = self.montants()
        if b != None:
            worksheet.write(l, col_revenu, b, euro_fmt)
        if s != None:
            worksheet.write(l, col_cot_sal, s, euro_fmt)
        if p != None:
            worksheet.write(l, col_cot_pst, p, euro_fmt)
        
    

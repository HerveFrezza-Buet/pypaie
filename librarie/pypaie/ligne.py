
    

        
class Ligne:
    def __init__(self, label):
        self.label = label # Description de la ligne

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

    def lignes(self):
        """
        Renvoie une liste de lignes. Une ligne est dictionnaire avec les
        informations apparaissant sur une ligne de fiche de paie.
        Les clés sont, si la valeur en est définie : 'label', 'brut', 'salarial', 'employeur'.
        """
        res = {'label' : self.label}
        b, s, e = self._brut(), self._cotisation_salariale(), self._cotisation_employeur()
        if b is not None:
            res['brut'] = b
        if s is not None:
            res['salarial'] = s
        if e is not None:
            res['employeur'] = e
        return [res]

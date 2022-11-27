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

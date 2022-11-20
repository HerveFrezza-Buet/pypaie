from . import revenus

class Bulletin:
    def __init__(self):
        self.bruts_salariaux = []
        self.brut_salariual = 0.

    def percoit(self, revenu):
        """
        Ajoute un revenu
        """
        if revenu['type'] == revenus.TYPE_BRUT_SALARIAL:
            self.bruts_salariaux.append(revenu)
            self.brut_salarial += renevu['montant']
            return

        raise ValueError(f'Bulletin.percoit (+=) : type de revenu {revenu["type"]} non géré.')

    def __iadd__(self, revenu):
        self.percoit(revenu)


